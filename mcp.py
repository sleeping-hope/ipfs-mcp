import os

from mcp.server import MCPServer
from ipfs.client import IPFSClient
from hila.adapter import HilaAdapter
from bacalhau.client import BacalhauClient
from runtime import update as runtime_update

mcp = MCPServer(
    "ipfs-mcp",
    description="Generic MCP interface for IPFS/Kubo with Hila and Bacalhau adapters.",
)
ipfs = IPFSClient(os.getenv("IPFS_API_URL", "http://127.0.0.1:5001"))
hila = HilaAdapter(os.getenv("HILA_API_URL"))
bacalhau = BacalhauClient(os.getenv("BACALHAU_API_URL"))

@mcp.tool()
def ipfs_add(path: str, pin: bool = False) -> dict:
    """Add a local file to IPFS and return its CID."""
    return ipfs.add(path, pin=pin)

@mcp.tool()
def ipfs_get(cid: str, output_path: str) -> dict:
    """Write an IPFS object to a local output path."""
    return ipfs.get(cid, output_path)

@mcp.tool()
def ipfs_cat(cid: str) -> str:
    """Read an IPFS object as UTF-8 text."""
    return ipfs.cat(cid)

@mcp.tool()
def ipfs_pin(cid: str, recursive: bool = True, name: str | None = None) -> dict:
    """Pin a CID on the connected Kubo node."""
    return ipfs.pin(cid, recursive=recursive, name=name)

@mcp.tool()
def ipfs_stat(cid: str) -> dict:
    """Return block statistics for a CID."""
    return ipfs.stat(cid)

@mcp.tool()
def hila_send(cid: str, operation: str = "send", payload: dict | None = None) -> dict:
    """Pass a CID to the Hila adapter."""
    return hila.send(cid, operation=operation, payload=payload or {})

@mcp.tool()
def hila_status() -> dict:
    """Return Hila adapter connection status."""
    return hila.status()

@mcp.tool()
def bacalhau_submit(cid: str, command: str, parameters: dict | None = None) -> dict:
    """Submit a compute request through the Bacalhau adapter boundary."""
    return bacalhau.submit(cid, command, parameters or {})

@mcp.tool()
def bacalhau_status(job_id: str) -> dict:
    """Return Bacalhau job status."""
    return bacalhau.status(job_id)

@mcp.tool()
def bacalhau_output(job_id: str) -> dict:
    """Return the output descriptor for a Bacalhau job."""
    return bacalhau.output(job_id)

@mcp.tool()
def update_status() -> dict:
    """Check the latest repository revision for runtime updating."""
    return runtime_update.update_status()

@mcp.tool()
def connection_status() -> dict:
    """Return connection status and runtime update status."""
    return {
        "ipfs": ipfs.health(),
        "hila": hila.status(),
        "bacalhau": bacalhau.status(),
        "update": runtime_update.update_status(),
        "version": "0.1.0",
    }

if __name__ == "__main__":
    mcp.run()
