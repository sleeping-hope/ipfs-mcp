import json
from pathlib import Path
from urllib.parse import urljoin

import httpx

class IPFSClient:
    def __init__(self, api_url: str, timeout: float = 60.0):
        self.api_url = api_url.rstrip("/") + "/"
        self.timeout = timeout

    def _post(self, endpoint: str, **kwargs) -> httpx.Response:
        url = urljoin(self.api_url, "api/v0/" + endpoint.lstrip("/"))
        response = httpx.post(url, timeout=self.timeout, **kwargs)
        response.raise_for_status()
        return response

    def health(self) -> dict:
        try:
            response = self._post("version")
            return {"connected": True, "response": response.json()}
        except Exception as exc:
            return {"connected": False, "error": str(exc)}

    def add(self, path: str, pin: bool = False) -> dict:
        file_path = Path(path)
        if not file_path.is_file():
            raise FileNotFoundError(path)
        with file_path.open("rb") as handle:
            response = self._post(
                "add",
                params={"pin": str(pin).lower(), "quiet": "true"},
                files={"file": (file_path.name, handle)},
            )
        lines = [line for line in response.text.splitlines() if line.strip()]
        if not lines:
            raise RuntimeError("Kubo returned no add result")
        data = json.loads(lines[-1])
        return {"cid": data.get("Hash"), "name": data.get("Name"), "size": data.get("Size")}

    def get(self, cid: str, output_path: str) -> dict:
        response = self._post("cat", params={"arg": cid})
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(response.content)
        return {"cid": cid, "output_path": str(target), "size": len(response.content)}

    def cat(self, cid: str) -> str:
        response = self._post("cat", params={"arg": cid})
        return response.content.decode("utf-8")

    def pin(self, cid: str, recursive: bool = True, name: str | None = None) -> dict:
        params = {"arg": cid, "recursive": str(recursive).lower()}
        if name:
            params["name"] = name
        response = self._post("pin/add", params=params)
        return response.json() if response.text else {"cid": cid}

    def stat(self, cid: str) -> dict:
        response = self._post("block/stat", params={"arg": cid, "encoding": "json"})
        return response.json()
