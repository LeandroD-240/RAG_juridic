---
description: Convierte un plan SDD aprobado en tareas trazables con casillas y espera autorización
---

Genera las tareas SDD para: $ARGUMENTS

1. Lee `AGENTS.md`, `MEMORY.md`, la spec aprobada, `plan.md` aprobado y los resultados de clarificación/revisión.
2. Comprueba que tanto la spec como el plan tienen aprobación explícita. Si falta alguna, detente y pide la aprobación correspondiente; no escribas `tasks.md`.
3. Encarga al `planner` que cree o actualice solo `specs/NNN-nombre/tasks.md`, respetando el plan aprobado. El planificador no implementa código ni cambia la spec o el plan.
4. Produce una lista ordenada de máximo 10 tareas. Cada tarea debe tener:
   - Una casilla Markdown sin marcar (`- [ ]`) y un identificador estable (por ejemplo, `T1`).
   - RF que cubre.
   - Alcance acotado y archivos previstos, consistentes con `plan.md`.
   - Criterio observable que empiece por **Hecho cuando:**.
   - Dependencias explícitas respecto a otras tareas, si las hay.
5. No marques tareas completas al generarlas. Si el trabajo no puede dividirse en tareas verificables o el plan no basta para decidirlas sin suposiciones, detente y solicita clarificación.
6. Pide al `reviewer` que compruebe la trazabilidad de las tareas frente a la spec y el plan, sin modificar archivos. Presenta el resultado junto con la lista de tareas.
7. Espera la aprobación explícita del usuario de `tasks.md`. No inicies implementación con este comando.

Solicitud: $ARGUMENTS
