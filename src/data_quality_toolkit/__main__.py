"""CLI for generated fictitious fixtures, validation, and reconciliation."""
import argparse
import json
from pathlib import Path
from .core import load_csv,validate,reconcile,save_csv,sample_rows

def main(argv=None):
    parser=argparse.ArgumentParser(description="Synthetic data contracts and bag reconciliation")
    sub=parser.add_subparsers(dest="command",required=True)
    demo=sub.add_parser("demo");demo.add_argument("--out-dir",default="build/demo")
    audit=sub.add_parser("audit");audit.add_argument("csv")
    compare=sub.add_parser("reconcile");compare.add_argument("left");compare.add_argument("right")
    args=parser.parse_args(argv)
    if args.command=="demo":
        d=Path(args.out_dir);d.mkdir(parents=True,exist_ok=True)
        clean,dirty=sample_rows()
        save_csv(d/"clean.csv",clean);save_csv(d/"dirty.csv",dirty)
        output={"audit_clean":validate(clean),"audit_dirty":validate(dirty),"reconciliation":reconcile(clean,dirty)}
        (d/"quality_report.json").write_text(json.dumps(output,indent=2),encoding="utf-8")
        print(f"Generated fictional QA scenarios in {d}")
        return 0
    if args.command=="audit":
        report=validate(load_csv(args.csv));print(json.dumps(report,indent=2));return 0 if report["pass"] else 2
    report=reconcile(load_csv(args.left),load_csv(args.right))
    print(json.dumps(report,indent=2));return 0 if report["equal"] else 2

if __name__=="__main__":raise SystemExit(main())
