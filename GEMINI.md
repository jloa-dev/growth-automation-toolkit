# Regla de Workspace: Registro Continuo, Protocolo Anti-Estafas y Lote de 10 Tareas Diarias

En este espacio de trabajo (`C:\Users\Loa\Downloads\GOAL`):

1. **Registro Continuo de Cada Tarea**: Toda tarea completada, PR enviado, commit realizado o propuesta técnica publicada debe registrarse inmediatamente en `TASK_LEDGER.md` y persistirse en Git (`jloa-dev/growth-automation-toolkit`).
2. **Actualización Automática al Preguntar Novedades**: Cada vez que el usuario pregunte por "novedades", "¿cómo van las tareas?", "estado", "avance", "¿me pagaron?" o similar:
   - Se debe ejecutar OBLIGATORIAMENTE la skill `continuous-task-reporter`:
     `python C:/Users/Loa/.gemini/config/skills/continuous-task-reporter/scripts/sync_report.py`
   - **Escaneo Dual en Vivo**:
     1. **GitHub Live**: Monitoreo de PRs, issues, aprobaciones y comentarios de mantenedores (Expensify, tscircuit).
     2. **Gmail Inbox Live**: Lectura por IMAP seguro de `jloa.dev@gmail.com` para depósitos de PayPal/Stripe, invitaciones/contratos de Upwork y notificaciones de Expensify.
   - Se actualiza `TASK_LEDGER.md` con el estado en vivo y se realiza commit y push automático.
   - Se responde al usuario con el estado consolidado de novedades y balance financiero sin pérdida de contexto.
3. **Protocolo Estricto Anti-Estafas (Zero-Scam Protocol)**:
   - Solo se trabaja en proyectos con fondos en custodia previa (**Escrow** bancario verificado):
     - **Expensify / App**: Upwork Escrow directo por empresa cotizada (NASDAQ: EXFY) con retiro a Interbank CCI `00389801350050828245`.
     - **tscircuit Organigrama**: Bounties de Algora / Stripe Express con liquidación automática al commit de merge a Interbank PEN `••••8245`.
   - **Lista Negra Explícita**: Prohibido trabajar o enviar PRs a `BasedHardware / omi` (cierre masivo sin merge en triage, tickets de discord sin escrow), `Crystal-PDF`, `Escaro` o plataformas sin contrato de custodia.
4. **Régimen de 10 Tareas / PRs Diarios (Baja Competencia)**:
   - Cuando el usuario solicite *"haz las 10 tareas diarias"*, *"tareas del día"* o similar, Antigravity debe ejecutar de forma inmediata y autónoma un lote completo de **10 tareas de alta probabilidad**:
     - Criterio de selección: **0 a 3 competidores humanos máximo** (prioridad a issues con 0 propuestas o con propuestas genéricas/slop).
     - Ejecución hermética: Diagnóstico de causa raíz en el código fuente local, tests unitarios, registro de propuesta formal con perfil Upwork/Stripe y persistencia inmediata en el ledger y Git.
