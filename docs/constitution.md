# Constitución del proyecto (SDD)

1. **Volatilidad y secreto.** Nunca guardar claves, tokens ni datos personales; solo variables de entorno.
   - **Verificación:** revisión de diffs y tests sin secretos.
   - **Fuente:** `AGENTS.md`; `ficha-de-contexto-agente-desarrollo.md`, sección 6.

2. **Dominio acotado.** El sistema es para derecho penal dominicano y usa solo PDF.
   - **Verificación:** casos límite de documentos no penales no etiquetados como especialidad.
   - **Fuente:** `decisiones-tecnicas.md`, sección 3; `Capacidades del proyecto.md`; `AGENTS.md`.

3. **LLM desacoplado.** Proveedor/modelo por entorno; cambiarlos no refactoriza RAG.
   - **Verificación:** cambiar variables sin tocar FAISS/LangGraph.
   - **Fuente:** `decisiones-tecnicas.md`, sección 2; `ficha-de-contexto-agente-desarrollo.md`, secciones 4-5.

4. **Arquitectura obligatoria.** FastAPI, FAISS, LangGraph y HTML/CSS/JS; supervisión humana incluida.
   - **Verificación:** revisión de componentes en cada spec.
   - **Fuente:** `README.md` (arquitectura); `ficha-de-contexto-agente-desarrollo.md`, secciones 3-4 y 6.

5. **SDD con aprobaciones.** Spec, plan y tareas se aprueban por separado; el revisor no edita.
   - **Verificación:** evidencia de aprobación antes de avanzar.
   - **Fuente:** skill `sdd`; `.opencode/agents/*.md`.

6. **Verificación ejecutable.** Nada se marca como hecho sin tests del stack real.
   - **Verificación:** `python3 -m unittest discover -s tests` en verde.
   - **Fuente:** estado real del repo (sin tests ni stack Node) y decisiones aprobadas por el usuario.
