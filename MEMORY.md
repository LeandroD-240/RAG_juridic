# MEMORY.md — RAG jurídico
Memoria del proyecto entre sesiones. Máximo ~50 líneas: resume o elimina lo que ya no aporte.
## Estado actual
- Fase de preparación. La skill SDD incluye comandos para constitución, clarificación, planificación, tareas, implementación, validación, cambios y consulta de estado; todavía no se creó `docs/constitution.md`.
## Decisiones (y por qué)
- SDD conserva aprobación explícita de spec, plan y tareas antes de implementar, para mantener el control del alcance.
- Plan, tareas e implementación se ejecutan en comandos separados; `tasks.md` usa casillas y se avanza una tarea por vez.
- Validación y estado son pasos separados: el revisor no edita, y el estado debe basarse en aprobación/evidencia explícita.
- La constitución se propone en seis principios verificables y solo se escribe tras aprobación explícita, como solicita el usuario.
## Aprendizajes y errores a evitar
- No asumir que los quickstarts planeados equivalen a código; comprobar herramientas y pruebas disponibles en el estado real del repo.
- Mantener separados los roles del coordinador, planificador, implementador y revisor; el revisor no edita.
- No marcar una tarea como completada hasta que sus criterios se validen y el revisor la apruebe.
## Próximos pasos
- (vacío por ahora)