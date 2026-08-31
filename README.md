# Quick PDF — CTF Web Challenge

A web application CTF challenge demonstrating an SSRF → IDOR vulnerability chain.

## Requirements

- Docker
- Docker Compose

## Running the Challenge

```bash
docker compose up --build
```

The challenge will be available at `http://<host>:5000`

To stop and remove all containers/volumes (clean reset):
```bash
docker compose down -v
```

## Configuring the Flag

**If you want to change the default flag in `docker-compose.yml`:

```yaml
  internal-api:
    environment:
      - CTF_FLAG=YOUR_UNIQUE_FLAG_HERE
```

Then rebuild:
```bash
docker compose down -v
docker compose up --build
```

The flag is generated into the internal database at container build time — it is never committed to this repository and does not persist outside the running container.

## Verifying Network Isolation

This challenge depends on `internal-api` being unreachable from outside the Docker network. **Before the event, confirm this on your actual hosting environment:**

```bash
curl http://<host>:8000/internal/health
```

This **must fail to connect**. Only port 5000 (the `web` service) should be externally reachable. If port 8000 responds, check that `docker-compose.yml` has no `ports:` entry under the `internal-api` service, and that no firewall rule is unexpectedly exposing it.

## Architecture


- `web/` — public-facing Flask app (PDF conversion tool)
- `internal-api/` — internal-only Flask service (not reachable from outside Docker network)
- Both services communicate over a private Docker network (`ctf-net`)

## Resetting Between Events / Teams

To generate a completely fresh instance with a new flag:
```bash
docker compose down -v
# update CTF_FLAG in docker-compose.yml
docker compose up --build
```

## Troubleshooting

**Container `internal-api` exits immediately after starting:**
Check logs for a Python error:
```bash
docker compose logs internal-api
```

**`web` cannot resolve `internal-api`:**
Confirm both services are running:
```bash
docker compose ps -a
```
If `internal-api` shows `Exited`, see the logs command above.

**Port already in use:**
Something else on the host is using port 5000. Either stop that process or change the host-side port mapping in `docker-compose.yml` (e.g. `"5001:5000"`).
