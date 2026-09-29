class BacalhauClient:
    """Provider-neutral Bacalhau adapter.

    Concrete Bacalhau API/CLI semantics are intentionally not guessed here.
    """

    def __init__(self, endpoint: str | None):
        self.endpoint = endpoint.rstrip("/") if endpoint else None

    def status(self, job_id: str | None = None) -> dict:
        return {
            "configured": bool(self.endpoint),
            "endpoint": self.endpoint,
            "adapter": "bacalhau",
            "job_id": job_id,
            "transport_ready": False,
            "reason": "Concrete Bacalhau API/CLI contract not configured",
        }

    def submit(self, cid: str, command: str, parameters: dict) -> dict:
        return {
            "accepted": False,
            "configured": bool(self.endpoint),
            "input_cid": cid,
            "command": command,
            "parameters": parameters,
            "reason": "Concrete Bacalhau API/CLI contract must be defined before transport execution",
        }

    def output(self, job_id: str) -> dict:
        return {
            "job_id": job_id,
            "configured": bool(self.endpoint),
            "transport_ready": False,
            "reason": "Concrete Bacalhau API/CLI contract not configured",
        }
