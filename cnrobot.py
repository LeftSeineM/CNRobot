"""Validate one CNRobot episode receipt. This CLI makes no model calls."""
import json
import sys
from pathlib import Path

MODELS = {"qwen3.8-flash-next", "deepseek-v4.1-flash"}

def summarize(record):
    if record["kind"] not in {"fixture", "native"}:
        raise ValueError("unknown receipt type")
    if not record["models"] or any(m not in MODELS for m in record["models"]):
        raise ValueError("unapproved model")
    if record["observation"] not in {"privileged", "geometry", "rgb"}:
        raise ValueError("unknown observation condition")
    if type(record["native_success"]) is not bool:
        raise ValueError("missing boolean terminal verdict")
    if record["kind"] == "native" and not all(record.get(k) for k in
            ("job", "revision", "action_receipt", "terminal_receipt")):
        raise ValueError("missing native evidence references")
    if type(record["steps"]) is not int or record["steps"] < 1:
        raise ValueError("expected positive action count")
    return f'{record["kind"]} {int(record["native_success"])}/1 first_failure={record["first_failure"]}'

if __name__ == "__main__":
    print(summarize(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))))
