---
name: sdd
description: Flujo de desarrollo guiado por especificaciones (SDD): contexto, requisitos EARS, revisión, plan, tareas e implementación controlada.
---

# SDD: desarrollo guiado por especificaciones

Usa este flujo para cambios que necesiten requisitos explícitos, aprobación y trazabilidad. Para cambios pequeños que no justifiquen una spec, usa `/feature`. Habla y escribe en español.

## Fuentes de verdad

Antes de proponer o modificar artefactos:

1. Lee `AGENTS.md` y `MEMORY.md`.
2. Lee las fuentes de alcance indicadas por `AGENTS.md` y examina el código y los archivos afectados que existan.
3. Si la documentación contradice el código existente, prevalece el código. Distingue claramente los hechos del repositorio de los planes aún no implementados.
4. No inventes decisiones pendientes ni requisitos. Señala vacíos y pregunta al usuario.
5. Respeta privacidad, supervisión humana y evaluación de riesgos como partes obligatorias del proyecto jurídico.

## Artefactos y trazabilidad

Una spec vive en `specs/NNN-nombre/spec.md` y contiene:

- **Contexto:** problema, usuarios afectados y estado actual demostrado por las fuentes.
- **Objetivo:** resultado observable, sin prescribir cómo implementarlo.
- **Fuera de alcance:** exclusiones necesarias para evitar interpretaciones amplias.
- **Requisitos funcionales (RF):** identificadores estables y enunciados EARS verificables.
- **Casos límite y criterios de aceptación:** comportamientos esperados, incluyendo errores y privacidad.

Escribe requisitos EARS como condiciones comprobables, por ejemplo:

- «Cuando [evento], el sistema deberá [respuesta]».
- «Mientras [estado], el sistema deberá [comportamiento]».
- «Si [condición de error], el sistema deberá [respuesta observable]».

Evita requisitos vagos («rápido», «fácil», «seguro») sin un criterio observable. Cada requisito debe poder vincularse con casos de prueba y tareas.

El plan aprobado identifica archivos reales a modificar, decisiones técnicas y alternativas descartadas, riesgos, estrategia de validación y RF cubiertos. No des por existentes archivos, comandos, paquetes, servicios o tests que no estén en el árbol actual. La lista de tareas contiene como máximo 10 tareas ordenadas; cada tarea indica sus RF, alcance acotado y «Hecho cuando:» con condiciones verificables.

## Flujo y aprobaciones

1. **Preparar la spec.** El coordinador transmite la solicitud y el contexto al planificador. Si faltan datos que cambien el comportamiento, el planificador devuelve hasta cinco preguntas concretas; el coordinador las presenta al usuario, sin adivinar.
2. **Clarificar.** El revisor busca ambigüedades, contradicciones, casos límite omitidos y conflictos con `docs/constitution.md` si existe. El revisor solo detecta; no edita ni decide la solución. El planificador corrige la spec y se repite la revisión cuando haga falta.
3. **Aprobar la spec.** Presenta la spec y observaciones al usuario. No generes plan ni código hasta que el usuario apruebe explícitamente la spec.
4. **Planificar.** Con `/sdd-plan`, el planificador redacta solo `plan.md` basándose en la spec aprobada. El revisor comprueba su consistencia; presenta el plan y espera la aprobación explícita del usuario antes de continuar.
5. **Desglosar tareas.** Con `/sdd-tasks`, el planificador crea `tasks.md` desde la spec y el plan aprobados. Usa casillas Markdown sin marcar, hasta 10 tareas con RF y criterios verificables. El revisor comprueba la trazabilidad; presenta las tareas y espera aprobación explícita antes de implementar.
6. **Implementar por tarea.** Con `/sdd-implement`, el coordinador llama al implementador una sola vez por tarea aprobada, en orden. El implementador no rediseña el plan, implementa solo esa tarea, valida con herramientas pertinentes al stack existente y se detiene al terminarla.
7. **Validar.** Con `/sdd-validate`, el revisor contrasta cada RF con los cambios y pruebas relevantes, comprueba criterios de finalización y constitución existente. No modifica archivos. Si encuentra incumplimientos, devuelve referencias precisas; el implementador corrige solo esos puntos. Marca una casilla como completada solo tras validación aprobada.
8. **Cambiar requisitos.** Con `/sdd-change`, el planificador actualiza primero solo la spec. Revisa, presenta diff y espera aprobación antes de volver a generar plan y tareas; cada artefacto conserva su aprobación independiente.
9. **Consultar estado.** Con `/sdd-status`, resume estado y bloqueos basándose en artefactos y aprobaciones comprobables, sin modificarlos.
10. **Cerrar.** Informa RF implementados, pruebas ejecutadas y resultado, veredicto, archivos afectados y pendientes. Actualiza `MEMORY.md` brevemente al cerrar la última tarea de una spec, sin guardar secretos ni datos personales.

En cada fase, informa al usuario brevemente. Nunca saltes aprobaciones, empieces una tarea siguiente antes de cerrar la actual ni conviertas una sugerencia opcional del revisor en un requisito sin aprobación.

## Responsabilidades de los cuatro agentes

- **coordinator:** único interlocutor con el usuario; transmite contexto completo, dirige fases y aprobaciones. No escribe código ni edita archivos.
- **planner:** escribe únicamente specs, planes y tareas dentro de `specs/`; no escribe código. Usa preguntas cuando falten decisiones.
- **reviewer:** revisa y valida sin editar; distingue incumplimientos bloqueantes de observaciones opcionales.
- **implementer:** ejecuta exactamente una tarea aprobada; no cambia el alcance ni comienza la siguiente.

Los agentes no comparten automáticamente esta conversación. En cada delegación incluye la fase, petición original, decisiones del usuario, rutas de lectura/escritura permitidas, RF afectados y resultado de la fase anterior. Si el agente no está disponible, no finjas que se delegó: informa al usuario y pide orientación antes de saltarte sus controles.

## Cambios sobre una spec existente

Primero solicita al planificador que actualice solo `spec.md` con RF nuevos o revisados y casos límite. Presenta el diff y espera aprobación. Después actualiza plan y tareas, vuelve a esperar aprobación y solo entonces continúa la implementación.

## Límites del proyecto

Aplica las restricciones actuales del repositorio, no un quickstart planeado como si fuera código. En particular, no cambies las decisiones técnicas ni los compromisos de privacidad por conveniencia; procesa solo PDF y no presentes documentos ajenos a la especialidad como contenido especializado. Abogado/Cliente describe públicos, no ramas de implementación. No resuelvas decisiones expresamente postergadas sin aprobación.
