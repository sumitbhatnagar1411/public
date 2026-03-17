"""
CLI entry: run agentic workflow for a question.
"""
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Run agentic AI workflow")
    parser.add_argument("question", nargs="+", help="Question to answer")
    parser.add_argument("--top-k", type=int, default=3, help="Number of docs to retrieve")
    parser.add_argument("--json", action="store_true", help="Output full result as JSON")
    args = parser.parse_args()
    question = " ".join(args.question)

    from .orchestration import run_workflow
    result = run_workflow(question, top_k=args.top_k)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("Answer:", result["answer"])
        print("\nPlan:", result["plan"]["reasoning"])
        print("Retrieval query:", result["plan"]["retrieval_query"])


if __name__ == "__main__":
    main()
