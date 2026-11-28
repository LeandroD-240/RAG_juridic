# Especificación 001 — Prueba de preparación del proveedor de modelo

**Estado:** aprobada

## Contexto

El repositorio contiene hoy solo documentación, PDFs legales e imágenes. El quickstart descrito en el README (`requirements.txt`, estructura `app/`, servidor) corresponde a un estado planeado: no hay código ejecutable, dependencias instaladas, plantilla de entorno, pruebas ni integración continua. Python 3.14.2 está disponible y ningún SDK de proveedor está instalado.

Antes de construir la capa RAG conviene comprobar, de forma aislada, que la selección del modelo y las credenciales se gobiernan por configuración de entorno y no por valores fijos. La petición original pide un mensaje «Hola mundo» y revisar las claves de Gemini (Google) y Llama (Meta). El README usa `MODEL_PROVIDER=google`, mientras la petición nombra a los proveedores y modelos; por eso se aceptan los alias `google|gemini` y `meta|llama` para una sola selección.

La revisión de claves es únicamente de presencia. No se trata de validar credenciales contra los proveedores, sino de fallar temprano y con claridad cuando falte configuración, sin exponer secretos. Esto respeta el compromiso de privacidad del proyecto: sin cuentas de usuario, sin historial persistente y sin guardar credenciales. La salida impresa debe revisarse manualmente antes de dar por válida la prueba, como materialización de la supervisión humana exigida por el proyecto.

## Objetivo

Obtener una comprobación ejecutable y verificable que, con la configuración correcta, envíe «Hola mundo» al proveedor seleccionado, muestre solo la respuesta recibida y termine con éxito; y que, ante configuración ausente o inválida, termine con un error claro y sin revelar ninguna credencial. El resultado es la base de la futura capa de modelo desacoplada: cambiar de proveedor o de credenciales no debe obligar a modificar el resto del sistema.

## Fuera de alcance

- Canal RAG completo: recuperación vectorial FAISS, orquestación LangGraph, indexación de leyes y carga de PDF.
- Servicios HTTP con FastAPI, endpoints o servidor de aplicación.
- Interfaz de usuario (HTML/CSS/JS), visor de documentos o despliegue en GitHub Pages.
- Ingestión, extracción o procesamiento de PDF; tampoco la distinción Abogado/Cliente, que es documentación y no una rama funcional.
- Validación real de credenciales: no se consulta a ningún proveedor con el propósito de comprobar si una clave es válida. El único envío previsto es el mensaje de prueba al proveedor seleccionado; las pruebas automatizadas lo sustituyen por una vía sin red.
- Fine-tuning, entrenamiento o ajuste de modelos.
- Métricas cuantitativas y dataset de evaluación, pendientes de la fase de depuración.
- Elección entre Mermaid.js y Markdown para diagramas, también pendiente.
- Autenticación de usuarios, base de datos de usuarios, historial de conversación o persistencia de datos personales.

## Requisitos funcionales

**RF-01 — Carga de configuración local con precedencia.**
Cuando se inicie la prueba, el sistema deberá cargar los valores de entorno desde el archivo local de configuración (`.env`) sin sobrescribir ninguna variable ya exportada en el entorno, de modo que el valor exportado prevalezca sobre el del archivo.

**RF-02 — Aliases de selección de proveedor.**
Cuando el valor de `MODEL_PROVIDER`, después de quitar solo los espacios circundantes, sea exactamente `google` o `gemini` en minúsculas, el sistema deberá tratarlo como selección del proveedor Google; cuando sea exactamente `meta` o `llama` en minúsculas, deberá tratarlo como selección del proveedor Meta. No se aplicará conversión de mayúsculas/minúsculas ni eliminación de espacios internos.

**RF-03 — Proveedor no seleccionable.**
Si `MODEL_PROVIDER` está ausente o, tras quitar solo espacios circundantes, no es exactamente uno de los cuatro alias en minúsculas, el sistema deberá evaluar esta condición antes que la presencia de claves (RF-04/RF-05), terminar con código de salida 1 y escribir en stderr exactamente `Proveedor no válido. Alias admitidos: google, gemini, meta, llama`, sin mostrar valores de credencial.

**RF-04 — Comprobación de presencia de claves.**
Después de superar RF-03 y antes de cualquier envío, el sistema deberá comprobar únicamente que `GEMINI_API_KEY` y `LLAMA_API_KEY` están definidas y que, tras quitar solo espacios circundantes, contienen al menos un carácter; no realizará comunicación alguna para validar su autenticidad. Solo la clave del proveedor seleccionado se utilizará para el envío; la otra se comprobará pero no se empleará.

**RF-05 — Clave ausente.**
Si falta `GEMINI_API_KEY` o `LLAMA_API_KEY`, o si alguna queda sin caracteres después de quitar solo espacios circundantes (por ejemplo `GEMINI_API_KEY="   "`), el sistema deberá terminar con código de salida 1, escribir en stderr exactamente `Faltan variables de entorno: ` seguido de los nombres de las variables ausentes en este orden fijo: `GEMINI_API_KEY`, `LLAMA_API_KEY` (si solo falta una, se escribe únicamente esa), y no continuar con RF-11 ni iniciar RF-06.

**RF-06 — Envío del mensaje de prueba.**
Cuando RF-03, RF-04, RF-05 y RF-11 hayan terminado correctamente, el sistema deberá enviar el mensaje «Hola mundo» al proveedor seleccionado usando la credencial correspondiente a ese proveedor.

**RF-07 — Confidencialidad de credenciales.**
Mientras la prueba se ejecuta, el sistema no deberá imprimir, registrar ni guardar los valores de `GEMINI_API_KEY`, `LLAMA_API_KEY` ni cualquier valor de credencial entregado al cliente del proveedor, incluso en mensajes de error, trazas y resultados de pruebas. Los nombres de esas variables pueden aparecer en los mensajes de error, pero sus valores nunca.

**RF-08 — Salida observable.**
Cuando el proveedor seleccionado devuelva una respuesta, el sistema deberá escribir en stdout únicamente esa respuesta. En la prueba automatizada, el doble de prueba devuelve el texto literal `RESPUESTA_DE_PRUEBA` y la ejecución deberá escribir en stdout exactamente `RESPUESTA_DE_PRUEBA\n`, sin prefijos ni otros textos; los mensajes de error deberán escribirse en stderr. En todos los mensajes de stderr, el proveedor se identifica con su nombre canónico `Google` o `Meta`, nunca con el alias introducido.

**RF-09 — Éxito.**
Si el mensaje de prueba se envió y su respuesta se imprimió conforme a RF-07 y RF-08, el sistema deberá terminar con código de salida 0.

**RF-10 — Fallo del envío.**
Si el envío al proveedor seleccionado falla por excepción del SDK, timeout, error HTTP o respuesta no 2xx, o respuesta vacía, el sistema deberá terminar con código de salida 1 y escribir en stderr exactamente `Fallo de envío con Google` o `Fallo de envío con Meta` según el proveedor seleccionado, sin incluir claves ni secretos.

**RF-11 — Configuración del modelo antes del envío (aprobado).**
Después de RF-03, RF-04 y RF-05 y antes de RF-06, el sistema deberá exigir los valores de configuración del modelo: `GEMINI_MODEL` para Google; `LLAMA_MODEL` y `LLAMA_BASE_URL` para Meta. Si falta alguno, el sistema deberá terminar con código de salida 1 y escribir en stderr exactamente `Falta configuración de modelo para Google: GEMINI_MODEL` para Google, o `Falta configuración de modelo para Meta: ` seguido de los nombres ausentes en este orden fijo: `LLAMA_BASE_URL`, `LLAMA_MODEL`, para Meta (si solo falta una, se escribe únicamente esa), sin mostrar valores de credencial ni secretos. En la ejecución real, el cliente del proveedor recibe el par proveedor/modelo y, para Meta, la base URL; en la prueba automatizada ese par se verifica mediante el doble de prueba, conforme a la precedencia de RF-01. Ese dato no se imprimirá ni se guardará.

## Casos límite

- **Archivo de configuración ausente:** si no existe el archivo local de entorno, la prueba no deberá fallar por ese hecho; continuará con las variables exportadas y aplicará RF-05 o RF-11 según corresponda.
- **Clave con solo espacios:** una variable exportada que, tras quitar solo espacios circundantes, no contiene caracteres (por ejemplo `GEMINI_API_KEY="   "`) no satisface RF-04: se trata como ausente (RF-05), no continúa a RF-11 ni dispara RF-06, aunque el archivo local contenga un valor válido, porque las exportadas prevalecen (RF-01).
- **Valores divergentes:** si `.env` y el entorno exportado definen la misma variable con valores distintos, se usará el exportado; en la ejecución real lo recibe el cliente del proveedor y en la automatización se observa mediante el doble de prueba, sin imprimir ni guardar credenciales.
- **Alias equivalentes:** `google` y `gemini` deben producir la misma selección; `meta` y `llama` deben producir la misma selección.
- **Normalización exacta:** tras quitar solo espacios circundantes, `" google "` se acepta como `google` (RF-02); `"GOOGLE"`, `"Gemini"`, `"goo gle"` y los nombres de modelo son inválidos (RF-03). No se convierten mayúsculas ni se eliminan espacios internos.
- **Precedencia de fallos:** con `MODEL_PROVIDER=openai` y claves ausentes, se informa solo el proveedor inválido (RF-03), con código 1 y sin secretos; no se evalúan RF-05 ni RF-11.
- **Clave no utilizada:** con proveedor Google, la clave de Llama puede estar presente y no se usará para el envío; con proveedor Meta ocurre lo inverso. En ambos casos se comprueban las dos y no se imprime ninguna.
- **Proveedor sin credencial propia:** si la clave del proveedor seleccionado falta pero la del otro proveedor está presente, se aplica RF-05 igualmente; la presencia de la otra clave no compensa la ausencia.

## Criterios de aceptación

1. Con ambas claves de prueba válidas (al menos un carácter tras quitar espacios circundantes), `MODEL_PROVIDER=google` o `gemini` y `GEMINI_MODEL` definida, el doble de prueba devuelve `RESPUESTA_DE_PRUEBA`; la ejecución escribe en stdout exactamente `RESPUESTA_DE_PRUEBA\n`, sin prefijos ni otros textos, y termina con código 0.
2. Con `MODEL_PROVIDER=meta` o `llama`, `LLAMA_MODEL` y `LLAMA_BASE_URL` definidas, el doble de prueba devuelve `RESPUESTA_DE_PRUEBA`; la ejecución escribe en stdout exactamente `RESPUESTA_DE_PRUEBA\n`, sin prefijos ni otros textos, y termina con código 0. La clave de Gemini no se usa para el envío.
3. Al omitir `GEMINI_API_KEY`, dejarla vacía o contener solo espacios, la prueba termina con código 1, stderr es exactamente `Faltan variables de entorno: GEMINI_API_KEY` (o `Faltan variables de entorno: GEMINI_API_KEY, LLAMA_API_KEY` si faltan ambas), no se evalúa RF-11 ni se realiza ningún envío.
4. Al omitir `LLAMA_API_KEY`, dejarla vacía o contener solo espacios, stderr es exactamente `Faltan variables de entorno: LLAMA_API_KEY` y ocurre el resto del comportamiento del criterio 3.
5. Al omitir `MODEL_PROVIDER` o usar un valor no aprobado (por ejemplo `openai`, `GOOGLE`, `Gemini`, `goo gle` o un nombre de modelo), la prueba termina con código 1, stderr es exactamente `Proveedor no válido. Alias admitidos: google, gemini, meta, llama`, no muestra secretos y no se realiza ningún envío, aunque falten claves.
6. La precedencia de RF-01 se verifica en la prueba automatizada comparando el par proveedor/modelo (y la base URL para Meta) entregado al doble de prueba con el valor exportado; ese dato no se imprime ni se guarda, y el valor de la credencial usada nunca se expone.
7. Los nombres de `GEMINI_API_KEY`, `LLAMA_API_KEY`, `GEMINI_MODEL`, `LLAMA_MODEL` y `LLAMA_BASE_URL` pueden aparecer en mensajes de error; sus valores y cualquier valor de credencial entregado al doble de prueba nunca aparecen en stdout, stderr, archivos ni registros. Ninguna ejecución crea o modifica un archivo que contenga credenciales.
8. Sin archivo `.env`, pero con las variables exportadas necesarias, la prueba cumple el criterio 1 o 2 según el proveedor; si falta alguna clave o variable de modelo, cumple el criterio 3, 4 u 11 según corresponda.
9. El comando exacto `python3 -m unittest discover -s tests` ejecuta las pruebas ubicadas en `tests/`, sin acceso a red ni credenciales reales, y cubre RF-01 a RF-11, confirmando los códigos de salida 0 y 1 y los textos exactos de stdout y stderr.
10. Existen `requirements.txt` con `google-genai`, `openai` y `python-dotenv`, y `.env.example` con los nombres `MODEL_PROVIDER`, `GEMINI_API_KEY`, `GEMINI_MODEL`, `LLAMA_API_KEY`, `LLAMA_MODEL` y `LLAMA_BASE_URL`, sin valores reales de credenciales.
11. Si falta `GEMINI_MODEL` para Google, stderr es exactamente `Falta configuración de modelo para Google: GEMINI_MODEL`. Si faltan configuraciones de Meta, stderr es `Falta configuración de modelo para Meta: ` seguido de los nombres ausentes en este orden fijo: `LLAMA_BASE_URL`, `LLAMA_MODEL`; con ambas ausentes: `Falta configuración de modelo para Meta: LLAMA_BASE_URL, LLAMA_MODEL`, y con solo `LLAMA_MODEL` ausente: `Falta configuración de modelo para Meta: LLAMA_MODEL`. En todos los casos hay código 1, no se muestran secretos y no se realiza ningún envío.
12. Si el envío simulado falla por excepción del SDK, timeout, error HTTP/no 2xx o respuesta vacía, la prueba termina con código 1 y stderr es exactamente `Fallo de envío con Google` o `Fallo de envío con Meta` según el proveedor, sin claves ni secretos.
13. En la prueba automatizada, con una clave ficticia exportada y un valor distinto para esa misma variable en `.env`, el cliente del proveedor (doble de prueba) recibe el valor exportado; el valor de ninguna de las dos variantes aparece en stdout ni en stderr y no se guarda en archivo alguno.
