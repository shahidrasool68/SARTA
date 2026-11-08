"""Judge0 CE client. Fail closed when sandbox is unreachable."""
import base64
import os
import httpx
from config import JUDGE0_URL, JUDGE0_API_KEY, JUDGE0_API_HOST

def _decode(value):
    if not value: return ""
    try: return base64.b64decode(value).decode("utf-8", errors="replace")
    except (ValueError, TypeError): return str(value)

async def evaluate_code(language_id: int, source_code: str, expected_output: str, stdin: str = ""):
    payload = {
        "language_id": language_id,
        "source_code": base64.b64encode(source_code.encode()).decode(),
        "stdin": base64.b64encode(stdin.encode()).decode(),
        "expected_output": base64.b64encode(expected_output.encode()).decode(),
        "cpu_time_limit": 2, "wall_time_limit": 5, "memory_limit": 128000
    }
    headers = {
        "Content-Type": "application/json",
    }
    if JUDGE0_API_KEY:
        headers["X-RapidAPI-Key"] = JUDGE0_API_KEY
        headers["X-RapidAPI-Host"] = JUDGE0_API_HOST

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                f"{JUDGE0_URL}/submissions",
                params={"base64_encoded": "true", "wait": "true"},
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        status = data.get("status", {}).get("description", "Unknown")
        return {"success": status == "Accepted", "status": status, "stdout": _decode(data.get("stdout")),
                "stderr": _decode(data.get("stderr")), "time": data.get("time"), "memory": data.get("memory")}
    except (httpx.HTTPError, ValueError, KeyError) as exc:
        return {"success": False, "status": "Sandbox unavailable", "message": str(exc)}
