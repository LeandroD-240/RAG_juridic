# Documento de Decisiones Técnicas Aclaradas y Especificaciones del Proyecto

Este documento consolida las decisiones técnicas oficiales, las aclaraciones de arquitectura y los acuerdos de diseño establecidos para el desarrollo del chatbot de asistencia jurídica en derecho penal para la República Dominicana.

---

## 1. Arquitectura del Sistema, Lógica y Hosting

* **Backend y Lógica de Negocio**: El "cerebro" y la lógica del sistema se desarrollarán enteramente en **Python** utilizando el framework **FastAPI**, integrando **FAISS** para la recuperación vectorial y **LangGraph** para la orquestación del flujo RAG.
* **Interfaz de Usuario (UI)**: La interfaz visual y sus conexiones interactivas se construirán utilizando el kit web estándar (**HTML, CSS y JavaScript**), manteniendo la línea visual inspirada en plataformas como ChatGPT, Claude, Gemini o DeepSeek.
* **Estrategia de Despliegue y Fallback**:
  * **Objetivo principal**: Alojamiento del prototipo en **GitHub Pages**.
  * **Plan alternativo (Notebook)**: En caso de contratiempos de implementación, aproximación a la fecha límite (*deadline*) o limitaciones de recursos (como disponibilidad del modelo), el entregable podrá migrarse a un **Jupyter/Colab Notebook** interactivo como simulación o prueba de concepto. El motivo de dicho cambio será debidamente documentado.

---

## 2. Abstracción y Configuración del Modelo de Lenguaje (LLM)

* **Independencia de la Arquitectura**: La arquitectura del RAG se diseñará para cubrir al menos el 90% de su estructura independientemente del modelo de lenguaje seleccionado (modelos abiertos de proveedores como Google o Meta, sin *fine-tuning*).
* **Flexibilidad de API Keys**: La aplicación se preparará para permitir cambiar entre diferentes modelos o proveedores de manera ágil mediante el uso de **variables de entorno** (`ENV`), evitando acoplamientos rígidos en el código.

---

## 3. Gestión de Documentos, Formatos y Estado Volátil

* **Documentos Base Iniciales**: El vectorstore incorporará como colección principal los documentos oficiales y públicos de las leyes penales de la República Dominicana, los cuales serán integrados durante la fase de construcción del RAG.
* **Formato Único Soportado**: Tanto los archivos legislativos iniciales como los documentos cargados por los usuarios serán aceptados exclusivamente en formato **PDF**.
* **Manejo de Sesión y Volatilidad**: Los archivos subidos por el usuario se mantendrán almacenados de forma temporal únicamente mientras la sesión permanezca activa en la página. Al recargar la página o salir de ella, los documentos del usuario se eliminarán de inmediato y la sesión se reiniciará a su estado inicial.

---

## 4. Clasificación de Usuarios y Documentación

* **Definición de Perfiles**: Las diferencias entre el perfil de **Abogado** (síntesis e investigación) y **Cliente** (información preventiva y concientización) no constituyen una diferenciación técnica en el motor del chat, sino la definición del público objetivo.
* **Documentación**: Esta distinción se abordará de manera explicativa en la documentación general del proyecto (como en el archivo `README.md` y en el informe técnico final).

---

## 5. Puntos Pendientes por Confirmar (Fases Posteriores)

* **Generación de Elementos Gráficos**: Se evaluará como opción principal el uso de **Mermaid.js** para el renderizado dinámico de diagramas y líneas de tiempo penal. Como alternativa secundaria más simple, se considerará el formateo nativo en **Markdown**.
* **Métricas de Evaluación y Dataset de Prueba**: La definición formal de métricas (precisión, hall embedding, etc.) y la creación del dataset de evaluación se realizarán tras completar la implementación inicial, integrándose en la fase de depuración (*debugging*) y validación.
