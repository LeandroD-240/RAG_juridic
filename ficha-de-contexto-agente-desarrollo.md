# Ficha de Contexto de Implementación para Agente de Desarrollo

**Proyecto**: Chatbot RAG de Asistencia en Derecho Penal (República Dominicana)  
**Documento**: Especificación Técnica y Ficha de Contexto para Desarrollo  

---

## 1. Objetivo de la Funcionalidad

El objetivo de esta funcionalidad es desarrollar un asistente conversacional inteligente basado en arquitectura de Generación Aumentada por Recuperación (RAG) especializado en el ámbito del derecho penal de la República Dominicana. 

El sistema debe consultar documentos judiciales e información legislativa interna para asistir a dos públicos objetivos principales:
* **Abogados**: Facilita la investigación jurídica, la síntesis de casos y la optimización del análisis legal.
* **Clientes / Ciudadanos**: Brinda información preventiva y concientización sobre sus acciones y derechos antes, durante y después del proceso penal.

El propósito final es desplegar un prototipo interactivo público alojado en la web que demuestre la viabilidad técnica y efectividad del enfoque RAG con supervisión humana.

---

## 2. Comportamiento Esperado

1. **Generación de Respuestas Adaptadas**:
   * El sistema debe procesar peticiones en lenguaje natural (*prompts*) y responder mediante resúmenes, respuestas directas a preguntas (*Q&A*) y análisis jurídicos fundamentados.
2. **Generación de Elementos Visuales y Estructurados**:
   * Debe construir automáticamente diagramas, tablas descriptivas y líneas de tiempo penal (por ejemplo, secuencias de eventos en cadena asociadas a delitos, infracciones o incumplimientos).
3. **Ingestión y Consulta de Documentos**:
   * Debe incorporar una colección pre-indexada con los documentos oficiales y públicos de las leyes penales de República Dominicana.
   * Debe permitir al usuario subir sus propios expedientes en formato PDF para realizar consultas específicas.
4. **Manejo Volátil de Sesión**:
   * Los archivos subidos por el usuario se mantendrán almacenados de forma temporal únicamente mientras la sesión permanezca activa.
   * Al recargar la página o cerrar la pestaña, el almacenamiento temporal se borrará de inmediato y la sesión se reiniciará a su estado inicial.

---

## 3. Componentes del Proyecto Afectados

* **Servicios API Backend (FastAPI en Python)**: Módulo encargado de gestionar las peticiones HTTP, el procesamiento de documentos PDF y la comunicación con el flujo RAG.
* **Orquestador RAG (LangGraph)**: Componente que gestiona la lógica de razonamiento del agente, el enrutamiento de consultas, el uso de herramientas y la interacción con el modelo.
* **Base de Datos Vectorial (FAISS)**: Almacenamiento vectorial encargado de indexar y recuperar fragmentos relevantes de las leyes penales y los expedientes subidos.
* **Capa de Abstracción del Modelo (LLM)**: Conector desacoplado mediante variables de entorno para enviar peticiones al modelo de lenguaje abierto seleccionado.
* **Interfaz de Usuario (HTML/CSS/JS)**: Capa de cliente web que renderiza la conversación, el cargador de PDF y las visualizaciones.
* **Módulo de Supervisión Humana y Evaluación**: Capa de control requerida en la arquitectura para supervisar y auditar las respuestas del agente.

---

## 4. Restricciones Técnicas y de Arquitectura

* **Lenguaje del Backend**: El desarrollo de la lógica de negocio y del servidor backend se realizará exclusivamente en **Python** (utilizando el framework **FastAPI**).
* **Tecnología Frontend**: La interfaz visual se desarrollará utilizando el kit web estándar (**HTML, CSS y JavaScript**).
* **Framework y Almacenamiento RAG**: Es obligatorio utilizar **FAISS** para la búsqueda vectorial y **LangGraph** para la orquestación del flujo conversacional.
* **Modelo de Lenguaje**: Utilización de un modelo de código abierto (de proveedores como Google o Meta) **sin fine-tuning**, optimizando el tiempo y consumo de recursos.
* **Infraestructura de Hosting**:
  * **Objetivo Primario**: Despliegue en la plataforma pública **GitHub Pages**.
  * **Plan de Contingencia (Notebook)**: En caso de contratiempos de implementación, aproximación a la fecha límite (*deadline*) o limitaciones de recursos del modelo, el entregable podrá migrarse a un **Jupyter/Colab Notebook** interactivo, justificando adecuadamente el cambio.
* **Formato de Archivo Único**: El pipeline de procesamiento aceptará exclusivamente documentos en formato **PDF**.

---

## 5. Decisiones Existentes a Respetar

1. **Desacoplamiento del Modelo**: La arquitectura RAG debe estar diseñada de manera modular, cubriendo al menos el 90% de su estructura independientemente del LLM final.
2. **Configuración por Variables de Entorno**: Las llaves de API (`API_KEY`) y la selección del modelo deben gestionarse de forma flexible mediante variables de entorno (`ENV`).
3. **Carácter Volátil y Sin Login**: La aplicación no manejará registro ni autenticación de usuarios, operando como un demo interactivo sin persistencia a largo plazo.
4. **Diseño e Inspiración Visual**: La interfaz de usuario debe imitar la línea estética y funcional de plataformas de chat líderes (**ChatGPT, Claude, Gemini o DeepSeek**).
5. **Alcance de los Perfiles de Usuario**: La distinción entre "Abogado" y "Cliente" corresponde a la definición del público objetivo del proyecto y se abordará en la documentación general (`README.md`), sin constituir una rama de código o motor técnico diferenciado.

---

## 6. Requisitos de Seguridad, Privacidad y Control

* **Limpieza de Datos Temporales**: Eliminación automática e inmediata de los PDF del usuario al finalizar la sesión (refresco o cierre de página).
* **Ausencia de Persistencia de Datos Personales**: No se almacenará información personal ni historial de conversación en bases de datos externas o disco.
* **Supervisión Humana y Riesgos**: Cumplimiento del marco de control requerido por el proyecto, el cual exige integrar mecanismos de supervisión humana, políticas de privacidad y evaluación de riesgos.

---

## 7. Casos Límite (Edge Cases)

* **Carga de PDF no relacionados con Derecho Penal**:
  * *Comportamiento*: Si el usuario sube un PDF cuyo contenido no corresponda al ámbito penal dominicano, el sistema no debe fallar ni bloquearse. Se procesará la lectura del archivo de forma estándar, aunque el sistema indicará o mantendrá su especialización en derecho penal.
* **Cierre o Recarga Inesperada de la Página**:
  * *Comportamiento*: Se debe asegurar que la memoria temporal en FAISS y el sistema de archivos del servidor eliminen cualquier rastro de los documentos del usuario, retornando al vectorstore base de leyes penales.
* **Cambio Dinámico de Proveedor o Modelo LLM**:
  * *Comportamiento*: La aplicación debe tolerar el cambio de credenciales o proveedor en las variables de entorno sin requerir refactorizaciones en la lógica de LangGraph o FAISS.
* **Migración Justificada del Entregable (GitHub Pages a Notebook)**:
  * *Comportamiento*: El usuario o desarrollador podrá conmutar el objetivo de despliegue hacia un Notebook interactivo si surgen impedimentos técnicos, registrando las causas en el informe final.

---

## 8. Criterios de Aceptación

1. **Prototipo Funcional Operativo**: Demo público desplegado en GitHub Pages (o Notebook de simulación validado con su respectiva justificación).
2. **Pipeline RAG Completo**: Recuperación precisa de información desde leyes penales dominicanas en PDF utilizando FAISS y LangGraph.
3. **Procesamiento de PDF de Usuario**: Capacidad de subir un PDF en tiempo de ejecución, procesarlo y responder preguntas contextualizadas durante la sesión activa.
4. **UI Fiel a Estándares**: Interfaz limpia en HTML/CSS/JS inspirada en chatbots populares (ChatGPT/Claude/Gemini/DeepSeek) que permita interacción fluida.
5. **Limpieza Volátil Efectiva**: Verificación de que la información del usuario no persiste al recargar la aplicación.
6. **Entregables de Proyecto Documentados**: Cobertura de los requisitos académicos del trabajo (informe técnico de 6 a 8 páginas APA 7, diagrama de arquitectura con supervisión humana y rúbrica de evaluación).

---

## 9. Cuestiones Pendientes por Resolver (Puntos a Aclarar)

Antes de iniciar la codificación detallada, se deben confirmar los siguientes dos aspectos técnicos:

1. **Tecnología para el Renderizado de Elementos Gráficos**:
   * *Estado*: Se evalúa **Mermaid.js** como la opción principal para renderizar diagramas y líneas de tiempo dinámicas en el frontend. La alternativa secundaria es el formateo estándar en **Markdown** si resulta más simple de implementar.
2. **Definición de Métricas de Evaluación y Dataset de Prueba**:
   * *Estado*: La selección de métricas cuantitativas (ej. precisión de recuperación, evaluación de alucinaciones) y la creación del dataset de pruebas penales se postergan para la fase de depuración y testing posterior a la implementación inicial.
