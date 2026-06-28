"""Run the TaskFlow RAG eval harness."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import EVAL_QUESTIONS_PATH
from app.pipeline import ask

REFUSAL_KEYWORDS = [
    "don't",
    "do not",
    "not documented",
    "not available",
    "not in",
    "no information",
    "cannot find",
    "can't find",
    "doesn't",
    "isn't",
    "i don't have",
]


def load_questions(path: Path = EVAL_QUESTIONS_PATH) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def is_refusal(answer: str) -> bool:
    lower = answer.lower()
    return any(keyword in lower for keyword in REFUSAL_KEYWORDS)


def score_question(item: dict, answer: str) -> bool:
    if item.get("must_refuse"):
        return is_refusal(answer)

    expected = item.get("expected_contains", [])
    lower = answer.lower()
    return all(str(token).lower() in lower for token in expected)


def run_eval(mode: str) -> dict:
    questions = load_questions()
    results: list[dict] = []
    passed = 0

    for item in questions:
        response = ask(item["question"], mode=mode)
        answer = str(response["answer"])
        ok = score_question(item, answer)
        passed += int(ok)
        results.append(
            {
                "id": item["id"],
                "question": item["question"],
                "type": item["type"],
                "passed": ok,
                "answer": answer,
                "sources": response["sources"],
            }
        )

    answerable = [r for r in results if r["type"] == "answerable"]
    unanswerable = [r for r in results if r["type"] == "unanswerable"]

    summary = {
        "mode": mode,
        "overall": f"{passed}/{len(results)}",
        "overall_pct": round(100 * passed / len(results), 1),
        "answerable": f"{sum(r['passed'] for r in answerable)}/{len(answerable)}",
        "unanswerable": f"{sum(r['passed'] for r in unanswerable)}/{len(unanswerable)}",
        "results": results,
    }
    return summary


def print_summary(summary: dict) -> None:
    print(f"\nMode: {summary['mode']}")
    print(f"Overall: {summary['overall']} ({summary['overall_pct']}%)")
    print(f"Answerable: {summary['answerable']}")
    print(f"Unanswerable: {summary['unanswerable']}")
    print("\nDetails:")
    for row in summary["results"]:
        status = "PASS" if row["passed"] else "FAIL"
        print(f"  [{status}] {row['id']}: {row['question']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="TaskFlow RAG eval harness")
    parser.add_argument(
        "--mode",
        choices=["rag", "prompt_only"],
        default="rag",
        help="Evaluation mode",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to save JSON results",
    )
    args = parser.parse_args()

    summary = run_eval(args.mode)
    print_summary(summary)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"\nSaved results to {args.output}")


if __name__ == "__main__":
    main()
