# Regla de Workspace: Registro Continuo, Protocolo Anti-Estafas y Priorización de Tareas Recientes

En este espacio de trabajo (`C:\Users\Loa\Downloads\GOAL`):

1. **Prioridad Absoluta a Tareas Recientes (Fresh / Same-Day Issues)**:
   - Al buscar o seleccionar tareas en **Expensify/App** o cualquier repositorio soportado, los issues publicados recientemente (hoy o en las últimas 24–48 horas) tienen **prioridad máxima e indiscutible** sobre cualquier ticket antiguo.
   - Si hoy se publicaron tareas nuevas donde podemos intervenir y dejar propuesta, **esas se toman de inmediato antes de mirar tickets de días anteriores**, asegurando la ventaja de orden de llegada (*First-Come, First-Served*).

2. **Criterio de Baja Competencia (0 a 2 Rivales Máximo)**:
   - Prioridad 1: **0 rivales** (cero propuestas de terceros).
   - Prioridad 2: **1 a 2 rivales** (propuestas genéricas o incompletas superables con diagnóstico exacto local).
   - Descarte automático: Issues con 3 o más competidores o con debates de semanas de antigüedad.

3. **Filtro Anti-Bot y Anti-Estafas (Zero-Scam & Zero-Bot Merge)**:
   - **Cero Intervención de Bots**: Prohibido trabajar en issues donde un mantenedor haya llamado a `@MelvinBot implement this` o donde un bot interno ya tenga un PR / Draft PR para resolver el bug (evita que un bot haga merge y nos deje sin cobro).
   - **Custodia Bancaria Verificada (Escrow Previo)**:
     - **Expensify / App**: Upwork Escrow directo por empresa cotizada (NASDAQ: EXFY) con retiro a Interbank CCI `00389801350050828245`. Requiere enlace oficial de trabajo de Upwork.
     - **tscircuit Organigrama**: Bounties de Algora / Stripe Express con liquidación automática al commit de merge a Interbank PEN `••••8245`.
   - **Lista Negra Explícita**: Prohibido trabajar o enviar PRs a `BasedHardware / omi` (cierre masivo sin merge en triage), `Crystal-PDF`, `Escaro` o plataformas sin contrato de custodia.

4. **Regla Financiera (Pago Mínimo de $25 USD - Monto No Priorizable)**:
   - El monto de la recompensa **no es priorizable** (un issue reciente de $175 con 0 rivales tiene más prioridad que uno viejo de $250 con 30 rivales).
   - **Pago Mínimo Obligatorio**: **$25 USD por tarea**, sin excepción alguna, para cualquier proyecto o plataforma.

5. **Registro Continuo de Cada Tarea**: Toda tarea completada, PR enviado, commit realizado o propuesta técnica publicada debe registrarse inmediatamente en `TASK_LEDGER.md` y persistirse en Git (`jloa-dev/growth-automation-toolkit`).

6. **Actualización Automática al Preguntar Novedades**: Cada vez que el usuario pregunte por "novedades", "¿cómo van las tareas?", "estado", "avance", "¿me pagaron?" o similar:
   - Se debe ejecutar OBLIGATORIAMENTE la skill `continuous-task-reporter`:
     `python C:/Users/Loa/.gemini/config/skills/continuous-task-reporter/scripts/sync_report.py`
   - Escaneo dual en vivo (GitHub Live + Gmail Inbox `jloa.dev@gmail.com`).
   - Actualización de `TASK_LEDGER.md` con commit y push automático.
