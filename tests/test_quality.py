import json
from data_quality_toolkit.core import sample_rows,validate,reconcile,load_csv,save_csv,fingerprint
from data_quality_toolkit.__main__ import main

def test_clean_fixture_passes():
    assert validate(sample_rows()[0])["pass"]

def test_dirty_fixture_detects_expected_five_rules():
    report=validate(sample_rows()[1]);assert report["failures"]==5
    assert {x["rule"] for x in report["findings"]}=={"unique","iso_date","accepted_values","nonnegative_decimal"}

def test_row_order_does_not_change_equivalence():
    a=sample_rows()[0];assert reconcile(a,list(reversed(a)))["equal"]

def test_multiplicity_is_not_lost():
    a=sample_rows()[0];r=reconcile(a,a+[a[0].copy()]);assert not r["equal"] and r["unexpected_rows"]==1

def test_missing_row_detected():
    a=sample_rows()[0];assert reconcile(a,a[:-1])["missing_rows"]==1

def test_changed_amount_detected():
    a=sample_rows()[0];b=[x.copy() for x in a];b[0]["amount"]="2"
    assert reconcile(a,b)["missing_rows"]==reconcile(a,b)["unexpected_rows"]==1

def test_hash_is_column_order_sensitive():
    row=sample_rows()[0][0]
    assert fingerprint(row,("date","amount"))!=fingerprint(row,("amount","date"))

def test_bad_headers_rejected(tmp_path):
    file=tmp_path/"invalid.csv";file.write_text("record_id,date,date,channel,amount,status\n",encoding="utf-8")
    import pytest
    with pytest.raises(ValueError,match="Duplicate"):load_csv(file)

def test_round_trip_utf8(tmp_path):
    rows=sample_rows()[0];p=tmp_path/"fixture.csv";save_csv(p,rows)
    assert load_csv(p)==rows

def test_cli_demo(tmp_path):
    assert main(["demo","--out-dir",str(tmp_path)])==0
    report=json.loads((tmp_path/"quality_report.json").read_text())
    assert report["audit_clean"]["pass"] and not report["audit_dirty"]["pass"]

def test_audit_nonzero_exit_for_invalid(tmp_path):
    _,bad=sample_rows();f=tmp_path/"bad.csv";save_csv(f,bad)
    assert main(["audit",str(f)])==2

def test_reconcile_exit_status(tmp_path):
    clean,_=sample_rows();a=tmp_path/"a.csv";b=tmp_path/"b.csv";save_csv(a,clean);save_csv(b,clean[:-1]);assert main(["reconcile",str(a),str(b)])==2
