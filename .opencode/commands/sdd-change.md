---
description: Gestiona un cambio de requisitos en una spec SDD existente con aprobaciones por fase
---

Gestiona este cambio para una spec SDD existente: $ARGUMENTS

1. Lee `AGENTS.md`, `MEMORY.md`, la skill SDD y la spec, el plan y las tareas afectados. Examina el código relevante si ayuda a distinguir estado implementado de lo documentado.
2. Identifica la spec correcta y el impacto del cambio. Si la spec no está indicada o hay más de una posible, pide aclaración antes de editar. No supongas comportamiento ni resuelvas decisiones pendientes.
3. Encarga al `planner` que modifique únicamente `spec.md`: actualizar o agregar RF en EARS, contexto/objetivo si procede, casos límite y criterios de aceptación. No debe tocar `plan.md`, `tasks.md` ni código.
4. Pide al `reviewer` una revisión de clarificación sin editar. Presenta hallazgos separados en: (1) ambigüedades restantes (requisitos no verificables), (2) contradicciones entre requisitos, (3) casos límite no cubiertos y (4) conflictos con `docs/constitution.md`. Indica si alguna categoría no tiene hallazgos.
5. Muestra al usuario el diff y los hallazgos de `spec.md`. No actualices plan/tareas ni implementes hasta recibir aprobación explícita de la spec modificada.
6. Tras esa aprobación, actualiza plan y tareas por medio de `/sdd-plan` y `/sdd-tasks`, siguiendo sus aprobaciones independientes. No conserves tareas obsoletas sin explicar el impacto; mantén trazabilidad RF-tarea.
7. La implementación posterior sigue `/sdd-implement`, una tarea aprobada cada vez, y la validación sigue `/sdd-validate`.

Si el cambio no requiere modificar requisitos, explica por qué y no alteres artefactos SDD sin aprobación.
