"""Reviewed, stdin/stdout based coding exercises with private test cases."""
CODING_PROBLEMS = {
    "two_sum": {
        "_id": "two_sum", "title": "Two Sum — Indices", "difficulty": "Easy",
        "description": "Read n, then n space-separated integers, then target from standard input. Print the two zero-based indices in increasing order, separated by a space. Exactly one solution exists.\nExample input:\n4\n2 7 11 15\n9\nExample output:\n0 1",
        "starter_code": "import sys\ndef main():\n    n = int(input())\n    nums = list(map(int, input().split()))\n    target = int(input())\n    # Print two indices in increasing order\n\nif __name__ == '__main__':\n    main()\n",
        "test_cases": [
            {"id": 1, "label": "Sample 1", "stdin": "4\n2 7 11 15\n9\n", "expected": "0 1", "hidden": False},
            {"id": 2, "label": "Hidden 1", "stdin": "3\n3 2 4\n6\n", "expected": "1 2", "hidden": True},
            {"id": 3, "label": "Hidden 2", "stdin": "2\n3 3\n6\n", "expected": "0 1", "hidden": True},
            {"id": 4, "label": "Hidden 3", "stdin": "5\n-8 4 7 12 0\n4\n", "expected": "0 3", "hidden": True},
        ]
    }
}

def get_problem(key):
    return CODING_PROBLEMS[key]

def get_public_problem(key):
    problem = get_problem(key)
    return {k:v for k,v in problem.items() if k != "test_cases"} | {
        "test_cases": [{k:v for k,v in tc.items() if k not in ("expected", "stdin") or not tc["hidden"]} for tc in problem["test_cases"]]
    }
