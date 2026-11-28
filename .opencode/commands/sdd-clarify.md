---
description: Clarifica requisitos y riesgos de una solicitud antes de redactar o cambiar una spec SDD
---

Clarifica la solicitud SDD antes de planificar o implementar: $ARGUMENTS

1. Lee `AGENTS.md`, `MEMORY.md` y la spec relacionada si existe; examina el código/documentación afectados cuando sea necesario. No asumas que el estado descrito en README ya está implementado.
2. Identifica solo dudas que puedan cambiar el comportamiento, alcance, privacidad, seguridad, supervisión humana, compatibilidad o criterios de aceptación.
3. Usa el planificador para revisar ambigüedades de la spec y el revisor para detectar contradicciones, casos límite omitidos y conflictos con `docs/constitution.md` si existe. El revisor solo detecta, no prescribe la solución.
4. Presenta la lista de hallazgos dividida exactamente en estos apartados:
   1. **Ambigüedades restantes:** requisitos que no se pueden verificar.
   2. **Contradicciones entre requisitos.**
   3. **Casos límite no cubiertos.**
   4. **Conflictos con `docs/constitution.md`.**
   Si un apartado no tiene hallazgos, indícalo explícitamente.
5. Presenta preguntas concretas en español, de una en una cuando las respuestas dependan entre sí. Si es posible, ofrece opciones y explica brevemente el impacto. No preguntes por cuestiones ya resueltas en fuentes de verdad.
6. Registra las respuestas como decisiones explícitas para la siguiente fase. Si no quedan dudas, resume los supuestos confirmados y criterios observables.

No escribas ni alteres spec, plan, tareas, código ni constitución con este comando. Tras resolver las dudas, solicita aprobación del usuario para continuar al paso correspondiente del flujo SDD.
