# AGENTS.md

- **Estado real del repo (verificado en el árbol actual):** solo documentación, PDFs legales e imágenes. No existen `app/`, `requirements.txt`, `.env.example`, tests, CI ni configs de build. El `README.md` y su quickstart (`pip install -r requirements.txt`, `uvicorn app.main:app`) describen un estado **planeado**, no código ejecutable; crea la estructura antes de dar esos pasos por existentes.
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
