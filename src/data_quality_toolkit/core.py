"""CSV contracts and multiset equality. Standard-library implementation."""
from __future__ import annotations
from collections import Counter
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import csv
import hashlib
import json
import re

FIELDS=("record_id","date","channel","amount","status")
CHANNELS={"Web","Retail","Partner"}
STATUSES={"paid","refunded"}

def load_csv(path: str|Path) -> list[dict[str,str]]:
    with open(path,encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames:raise ValueError("Missing CSV header")
        if len(reader.fieldnames)!=len(set(reader.fieldnames)):raise ValueError("Duplicate CSV header")
        if not set(FIELDS).issubset(reader.fieldnames):raise ValueError("Required columns missing")
        return list(reader)


def validate(rows: list[dict[str,str]]) -> dict:
    """Return all issues, preserving row number for debugging.

    Reject duplicate IDs, invalid ISO dates, unexpected account states, and
    negative/invalid decimals. Uses a strict standalone CSV contract.
    """
    findings=[]; ids=set()
    for index,row in enumerate(rows,start=2):
        rid=(row.get("record_id") or "").strip()
        if not re.fullmatch(r"SYN-[0-9]{5}",rid):findings.append({"row":index,"column":"record_id","rule":"format"})
        if rid in ids:findings.append({"row":index,"column":"record_id","rule":"unique"})
        ids.add(rid)
        try:
            d=date.fromisoformat(row.get("date") or "")
            if d.isoformat()!=row["date"]:raise ValueError("non-canonical date")
        except (ValueError,TypeError):findings.append({"row":index,"column":"date","rule":"iso_date"})
        if row.get("channel") not in CHANNELS:findings.append({"row":index,"column":"channel","rule":"accepted_values"})
        if row.get("status") not in STATUSES:findings.append({"row":index,"column":"status","rule":"accepted_values"})
        try:
            a=Decimal(row.get("amount") or "")
            if not a.is_finite() or a<0:raise InvalidOperation()
        except (InvalidOperation,ValueError,TypeError):findings.append({"row":index,"column":"amount","rule":"nonnegative_decimal"})
    return {"records":len(rows),"failures":len(findings),"pass":len(findings)==0,"findings":findings}


def fingerprint(row:dict,columns:tuple[str,...]=FIELDS) -> str:
    """Hash a canonical JSON array; hashes are integrity fingerprints, not anonymity."""
    payload=json.dumps([row.get(k) for k in columns],ensure_ascii=False,separators=(",",":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def reconcile(left:list[dict],right:list[dict],columns:tuple[str,...]=FIELDS) -> dict:
    """Compare row multiplicity (bag semantics); order does not matter.

    Extra/changed columns outside `columns` are intentionally ignored.
    """
    a=Counter(fingerprint(x,columns) for x in left)
    b=Counter(fingerprint(x,columns) for x in right)
    missing=a-b;extra=b-a
    return {"equal":not missing and not extra,"left_rows":len(left),"right_rows":len(right),
            "missing_rows":sum(missing.values()),"unexpected_rows":sum(extra.values()),
            "missing_hashes":dict(missing),"unexpected_hashes":dict(extra)}


def save_csv(path: str|Path,rows:list[dict]) -> None:
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader();writer.writerows(rows)


def sample_rows() -> tuple[list[dict],list[dict]]:
    """Artificial input and deliberately dirty snapshot with predictable defects."""
    clean=[{"record_id":f"SYN-{i:05d}","date":f"2026-01-{i:02d}","channel":["Web","Retail","Partner"][i%3],"amount":str(100+i*7),"status":"paid"} for i in range(1,21)]
    dirty=[x.copy() for x in clean]
    dirty[1]["record_id"]=dirty[0]["record_id"]
    dirty[2]["date"]="2026-02-30"
    dirty[3]["status"]="unknown"
    dirty[4]["amount"]="-42"
    dirty[5]["channel"]="Unauthorised"
    return clean,dirty
