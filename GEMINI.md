# Regla de Workspace: Registro Continuo y Sincronización en Vivo de Tareas

En este espacio de trabajo (`C:\Users\Loa\Downloads\GOAL`):

1. **Registro Continuo de Cada Tarea**: Toda tarea completada, PR enviado, commit realizado o propuesta técnica publicada debe registrarse inmediatamente en `TASK_LEDGER.md` y persistirse en Git (`jloa-dev/growth-automation-toolkit`).
2. **Actualización Automática al Preguntar Novedades**: Cada vez que el usuario pregunte por "novedades", "¿cómo van las tareas?", "estado", "avance" o similar:
   - Se debe ejecutar OBLIGATORIAMENTE la skill `continuous-task-reporter`:
     `python C:/Users/Loa/.gemini/config/skills/continuous-task-reporter/scripts/sync_report.py`
   - Se actualiza `TASK_LEDGER.md` con el estado en vivo de los 36 tickets (GitHub / Expensify / Omi / Algora).
   - Se realiza commit y push automático del reporte.
   - Se responde al usuario con el estado consolidado de novedades y balance financiero sin pérdida de contexto.
