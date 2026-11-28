---
description: Implementa la siguiente tarea SDD aprobada y validada, sin avanzar a la siguiente
---

Implementa una tarea SDD para: $ARGUMENTS

## Comprobaciones antes de implementar

1. Lee `AGENTS.md`, `MEMORY.md`, la skill SDD, la spec, `plan.md` y `tasks.md` correspondientes.
2. Verifica que spec, plan y tareas fueron aprobados explícitamente; que existe una tarea pendiente (`- [ ]`); y que sus dependencias están completas (`- [x]`). Si falta aprobación, contexto o dependencia, detente sin modificar archivos.
3. Trabaja únicamente en la primera tarea pendiente, salvo que el usuario identifique explícitamente otra tarea y sus dependencias estén completadas. No combines tareas ni cambies su alcance.
4. Revisa el estado actual del repositorio y los cambios existentes para no sobrescribir trabajo ajeno. Confirma que los archivos y herramientas mencionados en el plan existen o están justificados.

## Ejecución y control

1. Encarga al `implementer` esa única tarea, transmitiéndole la petición original, decisiones aprobadas, identificador y criterio «Hecho cuando:», RF cubiertos, rutas relevantes, dependencias, cambios existentes y validaciones previstas.
2. El implementador sigue el plan, implementa en el orden indicado (pruebas primero cuando corresponda), ejecuta validaciones adecuadas a las herramientas disponibles y se detiene al terminar. No debe empezar otra tarea ni improvisar si plan o tarea son incorrectos.
3. Si no puede cumplir un criterio o falla una validación, detén el flujo, deja la tarea sin marcar y comunica el bloqueo con evidencia. No reportes éxito parcial como tarea terminada.
4. Cuando la tarea esté completa, solicita al `reviewer` una validación contra sus criterios y RF, sin editar archivos. Si solicita cambios, encarga únicamente las correcciones necesarias al `implementer` y vuelve a validar. No superes dos rondas de corrección.
5. Marca la casilla de la tarea como `- [x]` solo cuando el implementador haya completado los criterios y el revisor la haya aprobado. Si el revisor no puede validar o hay cambios necesarios pendientes, consérvala sin marcar.
6. Detente tras una tarea, incluso si hay más tareas listas. Presenta identificador, RF cubiertos, archivos afectados, validaciones y resultados, veredicto del revisor y bloqueos o decisiones pendientes. Espera indicación antes de continuar.

No implementes si los permisos del agente o el estado del repositorio no permiten el flujo descrito. No sustituyas silenciosamente las comprobaciones exigidas por el plan ni afirmes que se ejecutaron herramientas que no existen.
