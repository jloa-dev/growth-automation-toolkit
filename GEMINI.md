# Regla de Workspace: Registro Continuo y Sincronización en Vivo de Tareas

En este espacio de trabajo (`C:\Users\Loa\Downloads\GOAL`):

1. **Registro Continuo de Cada Tarea**: Toda tarea completada, PR enviado, commit realizado o propuesta técnica publicada debe registrarse inmediatamente en `TASK_LEDGER.md` y persistirse en Git (`jloa-dev/growth-automation-toolkit`).
2. **Actualización Automática al Preguntar Novedades**: Cada vez que el usuario pregunte por "novedades", "¿cómo van las tareas?", "estado", "avance", "¿me pagaron?" o similar:
   - Se debe ejecutar OBLIGATORIAMENTE la skill `continuous-task-reporter`:
     `python C:/Users/Loa/.gemini/config/skills/continuous-task-reporter/scripts/sync_report.py`
   - **Escaneo Dual en Vivo**:
     1. **GitHub Live**: Monitoreo de PRs, issues, aprobaciones y comentarios de mantenedores (Expensify, Omi, tscircuit, Crystal-PDF).
     2. **Gmail Inbox Live**: Lectura por IMAP seguro de `jloa.dev@gmail.com` para depósitos de PayPal, tickets de Helpdesk de Omi, invitaciones/contratos de Upwork y notificaciones de Expensify.
   - Se actualiza `TASK_LEDGER.md` con el estado en vivo y se realiza commit y push automático.
   - Se responde al usuario con el estado consolidado de novedades y balance financiero sin pérdida de contexto.
