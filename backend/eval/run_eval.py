"""
Evaluation harness: runs both scenarios through the pipeline and checks
the verdict against the expected_verdict baked into the mock data.
Run with: python eval/run_eval.py  (from inside backend/)
"""
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from agent.orchestrator import run_pipeline

MOCK_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "mock_data")


def run_eval():
    results = []
    for name in ["a", "b", "c"]:
        with open(os.path.join(MOCK_DIR, f"scenario_{name}.json"), encoding="utf-8") as f:
            data = json.load(f)

        expected = data["expected_verdict"]
        actual = run_pipeline(data)["verdict"]

        severity_match = actual["severity_after"] == expected["severity_after"]
        status_match = actual["status"] == expected["status"]
        confidence_diff = abs(actual["confidence"] - expected["confidence"])
        confidence_ok = confidence_diff <= 10

        passed = severity_match and status_match and confidence_ok

        results.append({
            "scenario": name.upper(),
            "severity_match": severity_match,
            "status_match": status_match,
            "expected_confidence": expected["confidence"],
            "actual_confidence": actual["confidence"],
            "confidence_diff": confidence_diff,
            "passed": passed,
        })
    return results


if __name__ == "__main__":
    print("=" * 50)
    print("SOCweave Evaluation Report")
    print("=" * 50)

    results = run_eval()
    total_passed = sum(1 for r in results if r["passed"])

    for r in results:
        status_icon = "✅ PASS" if r["passed"] else "❌ FAIL"
        print(f"\n{status_icon} — Scenario {r['scenario']}")
        print(f"  Severity match : {r['severity_match']}")
        print(f"  Status match   : {r['status_match']}")
        print(f"  Confidence     : expected {r['expected_confidence']}%, "
              f"actual {r['actual_confidence']}% (diff: {r['confidence_diff']})")

    print("\n" + "=" * 50)
    print(f"RESULT: {total_passed}/{len(results)} scenarios passed")
    print("=" * 50)