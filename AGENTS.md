# AGENTS.md

- **Estado real del repo:** existen `model_probe.py`, `tests/test_model_probe.py`, `requirements.txt`, `.env.example`, `docs/constitution.md` y `specs/001-model-probe/{spec,plan,tasks}.md`; la prueba SDD 001 está completada y validada. Siguen sin existir `app/`, FastAPI, FAISS, LangGraph, UI, CI ni configs de build: el quickstart del `README.md` (`pip install -r requirements.txt`, `uvicorn app.main:app`) continúa siendo **planeado**.
- Comando exacto de pruebas: `python3 -m unittest discover -s tests` (13 pruebas, sin red ni credenciales reales).
- `model_probe.py`: usa `MODEL_PROVIDER` (`google|gemini` o `meta|llama`), comprueba presencia de `GEMINI_API_KEY` y `LLAMA_API_KEY` sin validarlas por red, y exige `GEMINI_MODEL` o `LLAMA_MODEL`/`LLAMA_BASE_URL` según proveedor.
- Trabaja en **español**: es el idioma de todos los documentos y del dominio del proyecto.
- Fuentes de verdad para alcance y restricciones: `ficha-de-contexto-agente-desarrollo.md` y `decisiones-tecnicas.md`. `README.md` es resumen/estado; `Objetivos.md`, `Capacidades del proyecto.md` y `Especificaciones del proyecto.md` definen el alcance. Si aparece código, prevalecen los archivos ejecutables sobre la prosa.
- El corpus base ya presente está en **`Leyes oficiales/`**, no en el `data/base_penal/` planeado del README. El pipeline acepta **solo PDF**: un PDF no penal debe procesarse sin fallar, pero sin presentarlo como especialidad del sistema.
- Decisiones técnicas obligatorias: backend **Python/FastAPI**, RAG con **FAISS + LangGraph**, frontend **HTML/CSS/JS sin framework**, LLM abierto (Google/Meta) sin fine-tuning, seleccionado por variables de entorno (`API_KEY`, proveedor/modelo). Cambiar proveedor o credenciales no debe obligar a refactorizar FAISS ni LangGraph.
- Privacidad/volatilidad: sin login, base de datos de usuarios ni historial persistente. Los PDF subidos y sus rastros en memoria/FAISS deben eliminarse al recargar o cerrar la página, volviendo al vectorstore base de leyes.
- La distinción **Abogado/Cliente** es público objetivo y documentación, **no una rama de código ni un motor distinto**.
- La arquitectura debe incluir **supervisión humana**, políticas de privacidad y evaluación de riesgos; no son accesorios opcionales.
- Despliegue objetivo: **GitHub Pages**. El notebook Jupyter/Colab es solo plan de contingencia y requiere justificar el cambio en el informe final.
- Aun no decidido: **Mermaid.js vs Markdown** para diagramas/líneas de tiempo, y métricas/dataset de evaluación (postergados a la fase de depuración). No los des por resueltos.
- Entregable académico: informe técnico **APA 7 de 6–8 páginas**, diagrama de arquitectura con supervisión humana y rúbrica. La estructura está en `Estructura_del_proyecto.png` y `Estructura_del_trabajo.png`.
- **MEMORY.md**: Al empezar, lee `MEMORY.md` para conocer el estado del proyecto y las decisiones tomadas. Al terminar una tarea, actualízalo en estado actual, deciciones importantes (con su porqué) y errores a evitar. Mantenlo breve y nunca guardes datos sensibles (claves, tokens, datos personales).
