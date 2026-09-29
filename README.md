# ipfs-mcp

Generic Model Context Protocol (MCP) interface for IPFS/Kubo.

## Project goal

Keep the project source in GitHub and connect runtime execution to a current
repository revision rather than requiring a permanent local installation.

```text
AI / MCP Client
      |
      v
   ipfs-mcp
      |
      v
 Generic Interface
      |
      v
   IPFS / Kubo
      |
      +---- CID ----> Hila adapter
      |
      +---- CID ----> Bacalhau adapter
                         |
                         v
                  Compute Over Data
                         |
                         v
                     Output CID
```

## Repository

This repository is the source of truth for the project.

- Repository: `sleeping-hope/ipfs-mcp`
- Default branch: `main`
- Version: `0.1.0`
- Runtime model: pull the current GitHub revision when execution is required
- Local installation: intentionally not required

## Structure

```text
ipfs-mcp/
├── mcp.py                 # MCP server and exposed tools
├── mcp.json               # runtime/provider configuration
├── VERSION                # project version
├── requirements.txt       # Python dependencies
├── ipfs/
│   └── client.py          # Kubo RPC client
├── hila/
│   └── adapter.py         # provider-neutral Hila boundary
└── bacalhau/
    └── client.py          # provider-neutral Bacalhau boundary
```

## MCP tools

The server exposes:

- `ipfs_add`
- `ipfs_get`
- `ipfs_cat`
- `ipfs_pin`
- `ipfs_stat`
- `hila_send`
- `hila_status`
- `bacalhau_submit`
- `bacalhau_status`
- `bacalhau_output`
- `connection_status`

## Providers

### IPFS / Kubo

The IPFS layer uses the Kubo HTTP RPC API. The default endpoint is:

`http://127.0.0.1:5001`

The RPC endpoint should remain private or protected by appropriate network
controls and authentication when used remotely.

### Hila

Hila is represented by an adapter boundary. Its concrete transport is not
assumed until the exact provider API contract is configured.

### Bacalhau

Bacalhau is represented by an adapter boundary. Its concrete API/CLI
semantics are not assumed until the exact provider contract is configured.

This prevents provider-specific behavior from being invented inside the
generic MCP layer.

## Configuration

Environment variables:

- `IPFS_API_URL`
- `HILA_API_URL`
- `BACALHAU_API_URL`

Example:

```text
IPFS_API_URL=http://127.0.0.1:5001
HILA_API_URL=<configured Hila endpoint>
BACALHAU_API_URL=<configured Bacalhau endpoint>
```

## Design principles

1. GitHub is the source of truth for source code.
2. IPFS is the content-addressed data layer.
3. MCP is the generic interface layer.
4. Provider adapters stay separate from the generic interface.
5. No SQL database is required by the core project.
6. Hila and Bacalhau contracts are not guessed.
7. Runtime state and credentials are not committed to the repository.
8. CID is the hand-off identifier between data and compute layers.

## Status

**Project initialized and stored in GitHub.**

Next implementation stages:

1. Define provider contracts for Hila and Bacalhau.
2. Add validation and integration tests.
3. Add runtime pull/update workflow.
4. Add Compute Over Data execution flow.
5. Add security and provenance controls.
