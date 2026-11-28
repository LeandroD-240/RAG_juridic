---
description: Resume el estado actual de una spec SDD y sus aprobaciones, tareas y bloqueos sin modificar archivos
---

Consulta el estado SDD para: $ARGUMENTS

1. Lee `AGENTS.md`, `MEMORY.md` y los artefactos SDD pertinentes. Si no se especifica una spec, lista las carpetas bajo `specs/` y resume las existentes; si hay varias y no se puede inferir cuál interesa, pregunta cuál consultar.
2. Basa el estado en los archivos actuales y evidencias disponibles. No infieras una aprobación a partir de la existencia del archivo: requiere evidencia explícita en la conversación o registro verificable.
3. Resume en español:
   - Spec y estado de aprobación; requisitos RF y hallazgos pendientes de clarificación.
   - Presencia/estado de `plan.md` y su aprobación.
   - Presencia/estado de `tasks.md`, usando casillas: completadas (`- [x]`), pendientes (`- [ ]`) y dependencias bloqueadas.
   - Cambios de implementación y última validación disponible, distinguiendo lo comprobado de lo reportado.
   - Bloqueos, decisiones pendientes y siguiente paso del flujo.
4. Si faltan artefactos o evidencias, indícalo expresamente como «desconocido» o «no registrado». No crees ni modifiques specs, planes, tareas, código, constitución ni memoria con este comando.
