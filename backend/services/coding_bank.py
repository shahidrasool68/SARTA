"""Reviewed, stdin/stdout based coding exercises with private test cases.

Matches problems directly with company LeetCode frequency data and company tiers.
"""

from typing import Dict, Any, List

CODING_PROBLEMS: Dict[str, Dict[str, Any]] = {
    "two_sum": {
        "_id": "two_sum",
        "title": "Two Sum — Indices",
        "difficulty": "Easy",
        "company_tags": ["Google", "Amazon", "Microsoft", "Apple", "Meta", "tcs", "Bloomberg"],
        "description": (
            "Read n, then n space-separated integers, then target from standard input.\n"
            "Print the two zero-based indices of the numbers that add up to target in increasing order, "
            "separated by a space.\n"
            "Exactly one solution exists. You may not use the same element twice.\n\n"
            "Example input:\n"
            "4\n"
            "2 7 11 15\n"
            "9\n\n"
            "Example output:\n"
            "0 1"
        ),
        "starter_code": (
            "import sys\n\n"
            "def main():\n"
            "    lines = sys.stdin.read().split()\n"
            "    if not lines:\n"
            "        return\n"
            "    n = int(lines[0])\n"
            "    nums = [int(x) for x in lines[1:n+1]]\n"
            "    target = int(lines[n+1])\n"
            "    \n"
            "    seen = {}\n"
            "    for i, num in enumerate(nums):\n"
            "        diff = target - num\n"
            "        if diff in seen:\n"
            "            print(f\"{seen[diff]} {i}\")\n"
            "            return\n"
            "        seen[num] = i\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        ),
        "test_cases": [
            {"id": 1, "label": "Sample 1", "stdin": "4\n2 7 11 15\n9\n", "expected": "0 1", "hidden": False},
            {"id": 2, "label": "Hidden 1", "stdin": "3\n3 2 4\n6\n", "expected": "1 2", "hidden": True},
            {"id": 3, "label": "Hidden 2", "stdin": "2\n3 3\n6\n", "expected": "0 1", "hidden": True},
            {"id": 4, "label": "Hidden 3", "stdin": "5\n-8 4 7 12 0\n4\n", "expected": "0 3", "hidden": True},
        ]
    },

    "palindrome_number": {
        "_id": "palindrome_number",
        "title": "Palindrome Number",
        "difficulty": "Easy",
        "company_tags": ["tcs", "Infosys", "Wipro", "Cognizant", "Amazon", "Microsoft"],
        "description": (
            "Given an integer x from standard input, print true if x is a palindrome, and false otherwise.\n"
            "An integer is a palindrome when it reads the same forward and backward.\n"
            "Negative numbers are not palindromes (e.g. -121 reads as 121-).\n\n"
            "Example 1:\n"
            "Input: 121\n"
            "Output: true\n\n"
            "Example 2:\n"
            "Input: -121\n"
            "Output: false"
        ),
        "starter_code": (
            "import sys\n\n"
            "def main():\n"
            "    s = sys.stdin.read().strip()\n"
            "    if not s:\n"
            "        return\n"
            "    # Output true or false\n"
            "    if s == s[::-1]:\n"
            "        print(\"true\")\n"
            "    else:\n"
            "        print(\"false\")\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        ),
        "test_cases": [
            {"id": 1, "label": "Sample 1", "stdin": "121\n", "expected": "true", "hidden": False},
            {"id": 2, "label": "Hidden 1 (Negative)", "stdin": "-121\n", "expected": "false", "hidden": True},
            {"id": 3, "label": "Hidden 2 (Trailing zero)", "stdin": "10\n", "expected": "false", "hidden": True},
            {"id": 4, "label": "Hidden 3 (Even palindrome)", "stdin": "1221\n", "expected": "true", "hidden": True},
        ]
    },

    "valid_parentheses": {
        "_id": "valid_parentheses",
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "company_tags": ["Meta", "Amazon", "Microsoft", "Google", "Bloomberg", "Uber"],
        "description": (
            "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', "
            "determine if the input string is valid.\n"
            "An input string is valid if:\n"
            "1. Open brackets must be closed by the same type of brackets.\n"
            "2. Open brackets must be closed in the correct order.\n"
            "3. Every close bracket has a corresponding open bracket of the same type.\n\n"
            "Example 1:\n"
            "Input: ()\n"
            "Output: true\n\n"
            "Example 2:\n"
            "Input: ()[]{}\n"
            "Output: true\n\n"
            "Example 3:\n"
            "Input: (]\n"
            "Output: false"
        ),
        "starter_code": (
            "import sys\n\n"
            "def main():\n"
            "    s = sys.stdin.read().strip()\n"
            "    stack = []\n"
            "    mapping = {')': '(', '}': '{', ']': '['}\n"
            "    for char in s:\n"
            "        if char in mapping:\n"
            "            top = stack.pop() if stack else '#'\n"
            "            if mapping[char] != top:\n"
            "                print(\"false\")\n"
            "                return\n"
            "        else:\n"
            "            stack.append(char)\n"
            "    print(\"true\" if not stack else \"false\")\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        ),
        "test_cases": [
            {"id": 1, "label": "Sample 1", "stdin": "()[]{}\n", "expected": "true", "hidden": False},
            {"id": 2, "label": "Hidden 1 (Mismatch)", "stdin": "(]\n", "expected": "false", "hidden": True},
            {"id": 3, "label": "Hidden 2 (Nested)", "stdin": "{[()]}\n", "expected": "true", "hidden": True},
            {"id": 4, "label": "Hidden 3 (Wrong order)", "stdin": "([)]\n", "expected": "false", "hidden": True},
        ]
    },

    "maximum_subarray": {
        "_id": "maximum_subarray",
        "title": "Maximum Subarray (Kadane's Algorithm)",
        "difficulty": "Medium",
        "company_tags": ["Google", "Amazon", "Microsoft", "Apple", "LinkedIn", "Adobe"],
        "description": (
            "Given an integer array nums from standard input, find the subarray with the largest sum, "
            "and print its sum.\n"
            "Input format: First line contains n. Second line contains n space-separated integers.\n\n"
            "Example input:\n"
            "9\n"
            "-2 1 -3 4 -1 2 1 -5 4\n\n"
            "Example output:\n"
            "6\n"
            "(The subarray [4, -1, 2, 1] has the largest sum 6.)"
        ),
        "starter_code": (
            "import sys\n\n"
            "def main():\n"
            "    lines = sys.stdin.read().split()\n"
            "    if not lines:\n"
            "        return\n"
            "    n = int(lines[0])\n"
            "    nums = [int(x) for x in lines[1:n+1]]\n"
            "    \n"
            "    max_so_far = nums[0]\n"
            "    curr_max = nums[0]\n"
            "    for x in nums[1:]:\n"
            "        curr_max = max(x, curr_max + x)\n"
            "        max_so_far = max(max_so_far, curr_max)\n"
            "    print(max_so_far)\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        ),
        "test_cases": [
            {"id": 1, "label": "Sample 1", "stdin": "9\n-2 1 -3 4 -1 2 1 -5 4\n", "expected": "6", "hidden": False},
            {"id": 2, "label": "Hidden 1 (Single item)", "stdin": "1\n1\n", "expected": "1", "hidden": True},
            {"id": 3, "label": "Hidden 2 (All positive)", "stdin": "5\n5 4 -1 7 8\n", "expected": "23", "hidden": True},
            {"id": 4, "label": "Hidden 3 (All negative)", "stdin": "3\n-3 -2 -5\n", "expected": "-2", "hidden": True},
        ]
    }
}


def get_problem(key: str) -> Dict[str, Any]:
    return CODING_PROBLEMS.get(key, CODING_PROBLEMS["two_sum"])


def get_public_problem(key: str) -> Dict[str, Any]:
    problem = get_problem(key)
    return {k: v for k, v in problem.items() if k != "test_cases"} | {
        "test_cases": [
            {k: v for k, v in tc.items() if k not in ("expected", "stdin") or not tc["hidden"]}
            for tc in problem["test_cases"]
        ]
    }


def select_problem_for_company(company_name: str, company_tier: str = "MEDIUM") -> str:
    """Select the most appropriate coding challenge based on target company and tier."""
    if not company_name:
        return "two_sum"

    comp_lower = company_name.strip().lower()

    # 1. Easy tier companies (TCS, Infosys, Wipro, etc.)
    if company_tier == "EASY":
        if comp_lower in ("tcs", "infosys", "wipro", "cognizant"):
            return "palindrome_number"
        return "two_sum"

    # 2. Match company tags
    for prob_id, prob in CODING_PROBLEMS.items():
        tags = [t.lower() for t in prob.get("company_tags", [])]
        if comp_lower in tags:
            # For Hard tier (Google, Meta, Amazon), prefer medium if available
            if company_tier == "HARD" and prob["difficulty"] == "Medium":
                return prob_id

    # 3. If Hard tier, default to Kadane / maximum subarray
    if company_tier == "HARD":
        return "maximum_subarray"

    return "two_sum"
