# Plan de implementación — 001 Prueba de preparación del proveedor de modelo

**Basado en:** `specs/001-model-probe/spec.md` (aprobada explícitamente por el usuario).

## Estado previo (YA HECHOS, no tareas)

- `docs/constitution.md`: creada y aprobada con los seis principios; no se vuelve a escribir en esta spec.
- `.opencode/agents/*.md`: ya ajustados al comando exacto `python3 -m unittest discover -s tests`.
- `specs/001-model-probe/spec.md`: aprobada; RF-11 y la regla de nombre canónico quedan congelados.

## Archivos reales a modificar o crear

| Ruta | Acción | Alcance |
| :--- | :--- | :--- |
| `model_probe.py` | Crear | Script raíz de la prueba. **No** es la futura capa `app/core/llm.py`; no se crea `app/`. |
| `requirements.txt` | Crear | `google-genai`, `openai`, `python-dotenv`. |
| `.env.example` | Crear | Solo nombres: `MODEL_PROVIDER`, `GEMINI_API_KEY`, `GEMINI_MODEL`, `LLAMA_API_KEY`, `LLAMA_MODEL`, `LLAMA_BASE_URL`. Sin valores reales de credenciales. |
| `tests/test_model_probe.py` | Crear | Dobles de prueba y aserciones de RF-01 a RF-11, sin red ni credenciales reales. |
| `AGENTS.md` | Modificar al cierre | Quitar la afirmación de que no existe `requirements.txt` y documentar el comando exacto de tests. |
| `MEMORY.md` | Modificar solo al cierre | Estado, decisiones con su porqué y errores a evitar; sin secretos ni datos personales. |

## Decisiones técnicas (con alternativa descartada)

| Decisión | Alternativa descartada | Por qué |
| :--- | :--- | :--- |
| Cargar `.env` con `python-dotenv` respetando las variables ya exportadas. | Parseo manual del archivo. | Evita reimplementar precedencia y reduce riesgo de sobreescribir secretos del entorno. |
| Usar `google-genai` y `openai` como clientes detrás de una única selección por entorno. | SDKs acoplados por proveedor dentro de la lógica de la prueba. | Cambiar `MODEL_PROVIDER` no debe obligar a reestructurar la lógica ni anticipar la futura capa desacoplada. |
| Pruebas con dobles de `unittest.mock` para los clientes. | Llamadas reales a los proveedores. | No hay credenciales reales, no se valida credenciales por red y el resultado debe ser determinista. |
| Normalizar alias solo con `strip()` de espacios circundantes, sin convertir a minúsculas. | Comparación case-insensitive. | La spec exige que `GOOGLE` y `Gemini` sean inválidos; `" google "` sí es válido. |
| stdout y stderr literales, sin prefijos ni marcas de tiempo. | Logs con prefijos. | Los criterios de aceptación comparan textos exactos y prohíben exponer secretos. |

**Patrón «funciones puras con hoy como parámetro»:** no aplica. Esta prueba no calcula fechas, no consulta el reloj y sus mensajes son literales; introducir un parámetro de fecha sería inventar una decisión ausente de la spec.

## Estrategia de validación

- Comando exacto: `python3 -m unittest discover -s tests`.
- Los clientes de Google y Meta se sustituyen por dobles de prueba: no hay red y no se usan credenciales reales.
- Cobertura RF-01 a RF-11, con aserciones de códigos de salida 0/1, stdout exacto `RESPUESTA_DE_PRUEBA\n`, los cuatro textos exactos de stderr, precedencia de `.env` y ausencia de valores secretos en salidas y archivos.
- Revisión manual de la salida impresa antes de dar por válida la prueba (supervisión humana, principio 4 de la constitución).
- El revisor valida RF por RF sin editar; ninguna casilla se marca antes de su aprobación.

## Riesgos

- **SDKs no instalados:** el entorno actual no tiene `google-genai` ni `openai`; la instalación puede fallar o hacer que el script no arranque. Mitigación: dependencias declaradas en `requirements.txt` y pruebas que sustituyen los clientes por dobles.
- **Valores de modelo/base URL dependientes del entorno:** `GEMINI_MODEL`, `LLAMA_MODEL` y `LLAMA_BASE_URL` pueden variar por máquina. Mitigación: no fijarlos en código; verificarlos por variables y comprobar su entrega al cliente simulado.
- **Fuga de secretos:** una clave podría aparecer en stdout, stderr, trazas o archivos. Mitigación: mensajes literales sin valores, nombres de variable permitidos y aserciones de no fuga.
- **Precedencia de variables exportadas sobre `.env`:** un valor exportado podría ser sobrescrito. Mitigación: carga sin sobrescritura y prueba explícita con valores divergentes.

## Mapa RF → parte del plan

| RF | Cobertura en el plan |
| :--- | :--- |
| RF-01 | T2 (carga de entorno sin sobrescribir) + T5 (`.env.example`) + prueba de divergencia en T1. |
| RF-02 | T2 (recorte de espacios y comparación exacta de alias). |
| RF-03 | T2 (validación de proveedor primero y stderr literal). |
| RF-04 | T2 (presencia de ambas claves con al menos un carácter tras recortar). |
| RF-05 | T2 (mensaje exacto de variables ausentes, sin envío). |
| RF-06 | T3 (envío de «Hola mundo» al proveedor seleccionado). |
| RF-07 | T4 (no impresión, registro ni guardado de valores de credencial). |
| RF-08 | T3 y T4 (stdout exacto, errores en stderr, nombre canónico `Google`/`Meta`). |
| RF-09 | T3 (código 0 tras respuesta impresa). |
| RF-10 | T3 (textos exactos `Fallo de envío con Google`/`con Meta`). |
| RF-11 | T2 (variables obligatorias y mensajes exactos) + T3 (par proveedor/modelo y base URL entregados al cliente). |
