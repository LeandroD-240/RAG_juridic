# MEMORY.md — RAG jurídico
Memoria del proyecto entre sesiones. Máximo ~50 líneas: resume o elimina lo que ya no aporte.

## Estado actual
- Spec 001 (prueba de preparación del proveedor) completada y validada; veredicto del revisor: APROBADO para T1–T7.
- Creados: `model_probe.py`, `tests/test_model_probe.py` (13 pruebas), `requirements.txt`, `.env.example`, `docs/constitution.md` y `specs/001-model-probe/{spec,plan,tasks}.md`.
- `python3 -m unittest discover -s tests` → 13 pruebas, OK, sin skipped. Salida revisada: `CODIGO=0`, `STDOUT_REPR='RESPUESTA_DE_PRUEBA\n'`, `STDERR_REPR=''`.
- T7 (cierre documental) completada; `AGENTS.md` y `MEMORY.md` reflejan el estado final.
- Sigue sin existir `app/`, FastAPI, FAISS, LangGraph, UI ni CI: el quickstart del README continúa siendo plan.

## Decisiones (y por qué)
- SDD con aprobación explícita de spec, plan y tareas, y una tarea por llamada: controla el alcance y evita cambios fuera de la tarea.
- `docs/constitution.md` con seis principios verificables: constitución aprobada antes de implementar.
- Alias `google|gemini` y `meta|llama`, comparación exacta tras `strip()`: `" google "` vale; `GOOGLE`, `Gemini` y espacios internos no.
- Presencia de `GEMINI_API_KEY` y `LLAMA_API_KEY` por recorte, sin validación de red: fallar temprano sin consultar ni exponer credenciales.
- RF-11 aprobado: `GEMINI_MODEL` o `LLAMA_MODEL`/`LLAMA_BASE_URL` se exigen antes del envío; par proveedor/modelo y base URL entregados al cliente.
- Proveedor canónico `Google`/`Meta` en stderr y mensajes literales: RF-08 exige nombres canónicos y textos exactos.
- Imports perezosos de `google-genai` y `openai` dentro de las fábricas: el módulo arranca sin SDKs instalados.
- Pruebas con dobles de `unittest.mock` y `unittest` (no pytest, no `node --test`): determinismo, sin red ni credenciales reales.
- `.env` se carga con `override=False`: prevalecen las variables exportadas (RF-01).

## Aprendizajes y errores a evitar
- No asumir que el quickstart planeado equivale a código; comprobar el árbol real antes de dar pasos por existentes.
- No usar `node --test`: este proyecto se verifica con `python3 -m unittest discover -s tests`.
- No imprimir ni guardar secretos: solo nombres de variables en errores; sin trazas con mensajes de excepción.
- No llamar a APIs reales en tests: siempre dobles; las validaciones de claves son solo de presencia.
- Mantener separados los roles; el revisor no edita y ninguna casilla se marca sin aprobación.

## Próximos pasos
- Instalar `requirements.txt` solo si se quiere ejecución real con SDKs.
- Continuar con la capa RAG/FastAPI/FAISS/LangGraph cuando se especifique y apruebe.
