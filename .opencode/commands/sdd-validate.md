---
description: Valida una implementación SDD contra cada requisito y devuelve un veredicto sin modificar archivos
---

Valida la implementación SDD para: $ARGUMENTS

1. Lee `AGENTS.md`, `MEMORY.md`, la skill SDD y los `spec.md`, `plan.md` y `tasks.md` correspondientes. Revisa los cambios reales del repositorio y confirma el alcance aprobado.
2. Encarga al `reviewer` una validación de la implementación, sin permiso para modificar archivos. Transmítele la petición original, decisiones aprobadas, rutas y límites, resultados de pruebas previas y cambios existentes.
3. El revisor debe recorrer cada RF y criterio de tarea: indicar evidencia concreta, prueba que lo cubre y resultado. Revisar también el cumplimiento del plan, los principios de `docs/constitution.md` si existe, privacidad, supervisión humana y evaluación de riesgos aplicables.
4. Comprueba qué pruebas y herramientas existen en el repositorio. Ejecuta las validaciones pertinentes y disponibles. Si las instrucciones de un agente exigen una herramienta inexistente o incompatible, informa de la discrepancia; no afirmes que la prueba pasó ni que la falta de pruebas equivale a aprobación.
5. El resultado comienza exactamente con uno de estos veredictos:
   - `VEREDICTO: APROBADO`
   - `VEREDICTO: CAMBIOS NECESARIOS`
6. Si hay incumplimientos, enuméralos con archivo y ubicación cuando sea posible, RF/tarea/principio incumplido y condición esperada. Separa observaciones opcionales que no bloquean. No corrijas código ni marques tareas completas.
7. Presenta resumen de cobertura RF, validaciones y resultados, veredicto, pendientes y, si corresponde, siguiente acción recomendada. Espera autorización antes de encargar correcciones o continuar el flujo.
