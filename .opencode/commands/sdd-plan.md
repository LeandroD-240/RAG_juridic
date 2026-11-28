---
description: Prepara el plan técnico SDD a partir de una spec aprobada y espera su aprobación
---

Prepara el plan técnico SDD para: $ARGUMENTS

1. Lee `AGENTS.md`, `MEMORY.md`, la spec aprobada y el resultado de clarificación/revisión. Confirma que la aprobación de la spec es explícita. Si falta aprobación o la spec está incompleta, detente y pide lo necesario.
2. Encarga al `planner` que cree únicamente `plan.md` bajo `specs/NNN-nombre/`. Debe examinar el código y los archivos afectados existentes; proponer rutas reales o nuevas justificadas; y no escribir código ni `tasks.md`.
3. El plan debe incluir:
   - Alcance técnico y mapa de archivos/cambios a RF.
   - Decisiones, alternativas descartadas y riesgos.
   - Estrategia de pruebas y validación adecuada a las herramientas realmente disponibles.
   - Consideraciones aplicables de privacidad, supervisión humana y evaluación de riesgos.
   - Dependencias y orden sugerido de implementación.
4. No presupongas que existen paquetes, pruebas, comandos ni infraestructura solo porque aparezcan en documentación planeada. Si una validación indicada por las instrucciones de los agentes no corresponde al stack o no está disponible, señala la discrepancia en vez de presentar una ejecución inexistente como satisfactoria.
5. Solicita al `reviewer` que compruebe consistencia del plan frente a la spec, sin editar artefactos.
6. Presenta el plan y los hallazgos al usuario y espera su aprobación explícita. No generes `tasks.md`, no implementes y no escribas código con este comando.

En cambios sobre una spec existente, verifica que `spec.md` fue actualizada y aprobada antes de planificar. Si cambia un requisito tras crear el plan, vuelve primero al paso de actualización y aprobación de la spec.
