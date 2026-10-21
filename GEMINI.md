# Regla de Workspace: Régimen de 50 PRs Diarios (10 Micro-Lotes de 5) con Trigger 'continua'

En este espacio de trabajo (`C:\Users\Loa\Downloads\GOAL`):

1. **Trigger de Avance Secuencial ("continua")**:
   - Cada vez que el usuario envíe el prompt **`continua`** (o con el comando `/boost continua`), Antigravity ejecutará de forma inmediata y autónoma el siguiente **micro-lote de 5 tareas pendientes** del día (hasta completar las 50 tareas / 10 bloques).
   - El orden de los micro-lotes es estricto:
     - **Lote 1 (1–5):** Expensify/App ($175–$250 USD, Upwork Escrow).
     - **Lote 2 (6–10):** Cal.com ($50–$300 USD, Algora / Stripe Express).
     - **Lote 3 (11–15):** Twenty CRM ($100–$500 USD, Algora / Stripe Express).
     - **Lote 4 (16–20):** Dub.co & Formbricks / Novu ($50–$250 USD, Algora / Stripe Express).
     - **Lote 5 (21–25):** Polar.sh Cluster TypeScript ($50–$300 USD, MoR / Stripe Express).
     - **Lote 6 (26–30):** Polar.sh Cluster Python/Rust ($50–$400 USD, MoR / Stripe Express).
     - **Lote 7 (31–35):** Opire Network ($25–$200 USD, Stripe Connect).
     - **Lote 8 (36–40):** BountyHub Network ($50–$250 USD, Stripe Payouts).
     - **Lote 9 (41–45):** OnlyDust & Superteam Earn ($100–$500 USD, USDC / Stripe).
     - **Lote 10 (46–50):** Huntr / Palo Alto Networks ($100–$1,000 USD, Stripe / PayPal).

2. **CERO TAREAS NO REMUNERADAS (Piso Mínimo $25 USD)**:
   - Queda prohibido trabajar en issues que no tengan un bounty formalmente declarado y confirmado ($\ge \$25$ USD).
   - Prohibido trabajar en issues voluntarios de `tscircuit` o repositorios generales sin la etiqueta oficial de recompensa (`bounty: $XX` de Algora, `Polar Funded`, `/reward` de Opire, o URL de Upwork).

3. **Protocolo Anti-Baneo y Preflight Verde**:
   - **Dispersión Multi-Cluster**: Máximo 3 a 5 PRs por repositorio al día.
   - **Throttling y Jitter**: Espaciado deliberado de **5 a 10 minutos** entre envíos.
   - **Preflight 100% Verde**: Linters y tests unitarios locales obligatorios antes del push.

4. **Filtro Anti-Bot y Anti-Estafas**:
   - Prohibido postular en issues donde un bot ya tenga PR / Draft PR o donde se haya llamado a `@MelvinBot implement this`.
   - Lista negra permanente: `BasedHardware / omi`, `Crystal-PDF`, `Escaro` y cualquier repositorio sin pasarela bancaria verificada.

5. **Persistencia Continua**:
   - Cada micro-lote completado se registra inmediatamente en `TASK_LEDGER.md` con commit y push a `jloa-dev/growth-automation-toolkit`.
   - Monitoreo en vivo de respuestas y notificaciones a `jloa.dev@gmail.com`.
