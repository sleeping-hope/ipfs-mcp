import httpx

class BacalhauClient:
    """Provider-neutral Bacalhau adapter."""
    def __init__(self, endpoint: str | None):
        self.endpoint = endpoint.rstrip("/") if endpoint else None

    def status(self, job_id: str | None = None) -> dict:
        if job_id is None:
            return {"configured": bool(self.endpoint), "endpoint": self.endpoint, "adapter": "bacalhau"}
        return self._get(job_id, "status")

    def submit(self, cid: str, command: str, parameters: dict) -> dict:
        if not self.endpoint:
            return {"accepted": False, "configured": False, "input_cid": cid, "command": command, "reason": "BACALHAU_API_URL is not configured"}
        response = httpx.post(
            f"{self.endpoint}/jobs",
            json={"input_cid": cid, "command": command, "parameters": parameters},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()

    def _get(self, job_id: str, suffix: str) -> dict:
        if not self.endpoint:
            return {"configured": False, "job_id": job_id, "reason": "BACALHAU_API_URL is not configured"}
        response = httpx.get(f"{self.endpoint}/jobs/{job_id}/{suffix}", timeout=60)
        response.raise_for_status()
        return response.json()

    def output(self, job_id: str) -> dict:
        return self._get(job_id, "output")
