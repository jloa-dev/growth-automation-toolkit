# Cal.com Issue #30351 Technical Solution Proposal

**Issue**: [#30351 - Security: Prisma Studio and Redis Ports Exposed by Default in Docker Compose](https://github.com/calcom/cal.diy/issues/30351)  
**Repository**: `calcom/cal.diy`  
**Bounty / Platform**: $100 USD (Algora / Stripe Express Interbank PEN `••••8245`)  
**Status**: 0 PRs, 0 Bot competition, Ready for PR  
**Contributor**: `jloa-dev` (`jloa.dev@gmail.com`)  

---

## 1. Problem Statement
In `docker-compose.yml`, the service definitions for `studio` (Prisma Studio) and `redis` publish host ports without restricting host IP binding:
```yaml
  redis:
    ports:
      - "${REDIS_PORT:-6379}:6379"
...
  studio:
    ports:
      - 5555:5555
```
By default in Docker, omitting the host IP causes Docker to bind ports to `0.0.0.0` (all network interfaces). On self-hosted servers or cloud VPS instances without external firewall rules:
1. Prisma Studio exposes direct, unauthenticated access to the entire application database.
2. Redis is exposed publicly on port 6379, allowing unauthorized cache manipulation or remote command execution.
3. Redis uses the mutable `redis:latest` tag, introducing supply chain and breaking change risks.

---

## 2. Root Cause & Threat Vector
- Docker daemon modifies `iptables` rules directly, often bypassing host `ufw` firewalls.
- Without explicit loopback binding (`127.0.0.1`), ports are accessible from the public internet.
- Prisma Studio is intended strictly for local development or authenticated administrative debugging via SSH tunnel.

---

## 3. Surgical Implementation
Bind Redis and Prisma Studio to `127.0.0.1` by default while allowing environment variable overrides (`REDIS_BIND_IP`, `PRISMA_STUDIO_BIND_IP`), and pin Redis to `redis:7.2-alpine`:

```diff
--- a/docker-compose.yml
+++ b/docker-compose.yml
@@ -25,14 +25,14 @@ services:
 
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
 
   calcom:
     image: calcom.docker.scarf.sh/calcom/cal.diy
@@ -124,7 +124,7 @@ services:
     networks:
       - stack
     ports:
-      - 5555:5555
+      - "${PRISMA_STUDIO_BIND_IP:-127.0.0.1}:${PRISMA_STUDIO_PORT:-5555}:5555"
     env_file: .env
     environment:
       - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}/${POSTGRES_DB}
```

---

## 4. Verification & Validation
1. **Zero Offsets**: Verified clean patch application against upstream `docker-compose.yml`.
2. **Loopback Default**: Verified that without environment overrides, Docker binds `127.0.0.1:6379` and `127.0.0.1:5555`.
3. **Opt-in Accessibility**: Remote developers can safely expose ports when needed by configuring `REDIS_BIND_IP=0.0.0.0` or `PRISMA_STUDIO_BIND_IP=0.0.0.0` in `.env`.
