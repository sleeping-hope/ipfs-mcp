import httpx

class HilaAdapter:
    """Provider-neutral boundary for Hila."""
    def __init__(self, endpoint: str | None):
        self.endpoint = endpoint.rstrip("/") if endpoint else None

    def status(self) -> dict:
        return {"configured": bool(self.endpoint), "endpoint": self.endpoint, "adapter": "hila"}

    def send(self, cid: str, operation: str, payload: dict) -> dict:
        if not self.endpoint:
            return {"accepted": False, "configured": False, "cid": cid, "operation": operation, "reason": "HILA_API_URL is not configured"}
        response = httpx.post(
            f"{self.endpoint}/send",
            json={"cid": cid, "operation": operation, "payload": payload},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()
