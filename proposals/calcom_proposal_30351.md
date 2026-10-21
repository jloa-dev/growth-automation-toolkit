# Cal.com Issue #30351 Technical Solution Proposal

**Issue**: [#30351 - Security: Prisma Studio and Redis Ports Exposed by Default in Docker Compose](https://github.com/calcom/cal.diy/issues/30351)  
**Repository**: `calcom/cal.diy`  
**Bounty / Platform**: $100 USD (Algora / Stripe Express Interbank PEN `••••8245`)  
**Status**: 0 PRs, 0 Bot competition, Ready for PR  
**Contributor**: `jloa-dev` (`jloa.dev@gmail.com`)  

---

## 1. Problem Statement
The standard `docker-compose.yml` configuration used for self-hosting and local development exposes two critical infrastructure ports on all network interfaces (`0.0.0.0`):
1. **Prisma Studio (`5555:5555`)**: Provides an unauthenticated web GUI with full read, write, and deletion privileges over the production/development PostgreSQL database.
2. **Redis (`${REDIS_PORT:-6379}:6379`)**: Runs the unpinned `redis:latest` image without binding to localhost, allowing external network scanners to inspect cached session tokens, user rates, and queue jobs.

When deploying Cal.com on cloud VPS instances (AWS EC2, DigitalOcean, Hetzner, etc.) without an external firewall, these ports are publicly exposed to the internet by Docker's default iptables manipulation.

---

## 2. Root Cause Analysis
In `docker-compose.yml`:
1. Redis service:
```yaml
  redis:
    container_name: redis
    image: redis:latest
    ports:
      - "${REDIS_PORT:-6379}:6379"
```
2. Studio service:
```yaml
  studio:
    image: calcom.docker.scarf.sh/calcom/cal.diy
    ports:
      - 5555:5555
```
Because no host IP prefix is specified (e.g. `127.0.0.1:`), the Docker daemon binds to `0.0.0.0:<port>`, publishing both services globally. Furthermore, `redis:latest` introduces volatility across Docker pull cycles.

---

## 3. Surgical Implementation
Harden `docker-compose.yml` by:
1. Explicitly binding Prisma Studio and Redis to `127.0.0.1` by default.
2. Allowing configurable bind IPs via environment variables (`PRISMA_STUDIO_BIND_IP`, `REDIS_BIND_IP`) for developers requiring remote reverse proxy access.
3. Pinning Redis to an immutable LTS image (`redis:7.2-alpine`).

```diff
--- a/docker-compose.yml
+++ b/docker-compose.yml
@@ -23,12 +23,12 @@ services:
 
   redis:
     container_name: redis
-    image: redis:latest
+    image: redis:7.2-alpine
     restart: always
     volumes:
       - redis-data:/data
     networks:
       - stack
     ports:
-      - "${REDIS_PORT:-6379}:6379"
+      - "${REDIS_BIND_IP:-127.0.0.1}:${REDIS_PORT:-6379}:6379"
 
@@ -107,7 +107,7 @@ services:
     restart: always
     networks:
       - stack
     ports:
-      - 5555:5555
+      - "${PRISMA_STUDIO_BIND_IP:-127.0.0.1}:${PRISMA_STUDIO_PORT:-5555}:5555"
     env_file: .env
     environment:
       - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}/${POSTGRES_DB}
```

Update `.env.example`:
```diff
--- a/.env.example
+++ b/.env.example
@@ -12,3 +12,7 @@
+# Security: Local loopback port bindings for development services
+REDIS_BIND_IP="127.0.0.1"
+PRISMA_STUDIO_BIND_IP="127.0.0.1"
```

---

## 4. Verification & Security Testing
- **Local Verification**:
  1. Ran `docker compose config` to validate syntax.
  2. Verified port mappings resolve to `127.0.0.1:5555:5555` and `127.0.0.1:6379:6379`.
  3. Confirmed external interface (`curl <public_ip>:5555`) returns connection refused.
  4. Confirmed local interface (`curl 127.0.0.1:5555`) successfully connects to Prisma Studio.
