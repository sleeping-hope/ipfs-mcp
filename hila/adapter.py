class HilaAdapter:
    """Provider-neutral boundary for Hila.

    The concrete Hila transport is intentionally not assumed until its exact
    API contract is configured.
    """

    def __init__(self, endpoint: str | None):
        self.endpoint = endpoint.rstrip("/") if endpoint else None

    def status(self) -> dict:
        return {
            "configured": bool(self.endpoint),
            "endpoint": self.endpoint,
            "adapter": "hila",
            "transport_ready": False,
            "reason": "Concrete Hila API contract not configured",
        }

    def send(self, cid: str, operation: str, payload: dict) -> dict:
        return {
            "accepted": False,
            "configured": bool(self.endpoint),
            "cid": cid,
            "operation": operation,
            "payload": payload,
            "reason": "Concrete Hila API contract must be defined before transport execution",
        }
