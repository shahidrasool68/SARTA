import httpx
import base64

JUDGE0_URL = "http://localhost:2358"

async def evaluate_code(language_id: int, source_code: str, expected_output: str, stdin: str = ""):
    """
    Submit code to the self-hosted Judge0 CE instance and wait for evaluation.
    """
    encoded_source = base64.b64encode(source_code.encode()).decode()
    encoded_expected = base64.b64encode(expected_output.encode()).decode() if expected_output else ""
    encoded_stdin = base64.b64encode(stdin.encode()).decode() if stdin else ""
    
    payload = {
        "language_id": language_id,
        "source_code": encoded_source,
        "expected_output": encoded_expected,
        "stdin": encoded_stdin,
        "base64_encoded": True
    }
    
    async with httpx.AsyncClient() as client:
        # Submit submission
        response = await client.post(f"{JUDGE0_URL}/submissions?base64_encoded=true&wait=true", json=payload)
        
        if response.status_code == 201 or response.status_code == 200:
            result = response.json()
            status = result.get("status", {}).get("description")
            # Decode output if present
            stdout = base64.b64decode(result.get("stdout", "") or "").decode()
            stderr = base64.b64decode(result.get("stderr", "") or "").decode()
            
            return {
                "success": status == "Accepted",
                "status": status,
                "stdout": stdout,
                "stderr": stderr,
                "time": result.get("time"),
                "memory": result.get("memory")
            }
        else:
            return {"success": False, "status": "Error", "message": response.text}
