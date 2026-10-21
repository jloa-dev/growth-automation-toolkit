# Regla de Workspace: Régimen de 50 PRs Diarios, Expansión Multi-Ecosistema y Protocolo Anti-Baneo

En este espacio de trabajo (`C:\Users\Loa\Downloads\GOAL`):

1. **Prioridad Absoluta a Tareas Recientes y Remuneradas**:
   - Todo issue debe ser reciente (del día o últimas 24–48h) para ganar la ventaja FCFS (*First-Come, First-Served*).
   - **CERO TAREAS NO REMUNERADAS**: Queda prohibido trabajar en issues que no tengan un bounty formalmente declarado y confirmado ($\ge \$25$ USD). Prohibido trabajar en issues voluntarios de `tscircuit` o cualquier otro repo sin la etiqueta oficial de recompensa de Algora/Polar.

2. **Régimen de 50 Pull Requests / Propuestas Diarias**:
   - Cuando el usuario indique *"haz las 50 tareas diarias"*, *"lote de 50"* o similar, Antigravity ejecutará un portafolio de 50 contribuciones remuneradas aplicando el **Protocolo Anti-Baneo**:
     - **Distribución Multi-Cluster (10 Ecosistemas)**: Máximo 3 a 5 PRs por repositorio para no saturar mantenedores ni activar defensas de spam de GitHub. Repartir entre Expensify, Algora (Cal.com, Twenty, Dub, Formbricks), Polar.sh, Opire, BountyHub, OnlyDust, Superteam y Huntr.
     - **Throttling y Jitter**: Espaciado deliberado de **5 a 10 minutos** entre cada envío de PR para imitar el ritmo de un programador senior y evitar límites de tasa (*Abuse Rate Limits*).
     - **Preflight 100% Verde**: Cero PRs rotos. Todo código debe pasar linters y tests unitarios locales antes del push.

3. **Filtro Anti-Bot y Anti-Estafas (Zero-Scam & Zero-Bot Merge)**:
   - Prohibido trabajar en issues donde un bot ya tenga un PR / Draft PR o donde se haya llamado a `@MelvinBot implement this`.
   - Custodia bancaria verificada en todas las plataformas: Upwork Escrow (Expensify), Stripe Express (Algora, Polar.sh, Opire, BountyHub), PayPal/Stripe (Huntr).
   - Lista negra permanente: `BasedHardware / omi`, `Crystal-PDF`, `Escaro` y cualquier plataforma sin pasarela bancaria.

4. **Regla Financiera (Pago Mínimo de $25 USD - Monto No Priorizable)**:
   - **Pago Mínimo Obligatorio**: **$25 USD por tarea**, sin excepción alguna.
   - Monto no priorizable: se prioriza baja competencia (0 a 2 rivales) y rapidez sobre montos gigantescos saturados.

5. **Registro Continuo de Cada Tarea**: Toda tarea completada, PR enviado, commit realizado o propuesta técnica publicada debe registrarse inmediatamente en `TASK_LEDGER.md` y persistirse en Git (`jloa-dev/growth-automation-toolkit`).

6. **Actualización Automática al Preguntar Novedades**: Cada vez que el usuario pregunte por "novedades", "¿cómo van las tareas?", "estado", "avance", "¿me pagaron?" o similar:
   - Se debe ejecutar OBLIGATORIAMENTE la skill `continuous-task-reporter`:
     `python C:/Users/Loa/.gemini/config/skills/continuous-task-reporter/scripts/sync_report.py`
   - Escaneo dual en vivo (GitHub Live + Gmail Inbox `jloa.dev@gmail.com`).
   - Actualización de `TASK_LEDGER.md` con commit y push automático.
