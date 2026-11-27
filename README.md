# Chatbot RAG de Asistencia en Derecho Penal (República Dominicana)

---

## 📋 Descripción

Este proyecto consiste en el desarrollo de un chatbot inteligente de **Asistencia en Derecho Penal para la República Dominicana**, construido sobre una arquitectura de **Generación Aumentada por Recuperación (RAG)**. El sistema utiliza documentos legislativos oficiales y expedientes judiciales para ofrecer respuestas precisas, resúmenes de casos y análisis jurídicos fundamentados.

La plataforma está diseñada para atender a dos públicos objetivos principales:
* **Abogados y Profesionales del Derecho**: Herramienta orientada a agilizar la investigación jurídica, sintetizar expedientes complejos y optimizar el tiempo de análisis legal.
* **Clientes y Ciudadanos**: Asistente educativo e informativo diseñado para orientar sobre derechos, garantías procesales y las etapas de un proceso penal antes, durante y después del caso.

---

## 🚧 Estado del Proyecto

El proyecto se encuentra en fase de prototipado activo y especificación de arquitectura. A continuación se detalla el estado actual según los componentes del sistema afectados:

| Componente del Sistema | Estado Actual | Descripción / Alcance |
| :--- | :--- | :--- |
| **Servicios API Backend (FastAPI)** | No iniciado | Definición de endpoints HTTP para carga de PDFs y orquestación de consultas RAG. |
| **Orquestador RAG (LangGraph)** | No iniciado | Configuración del flujo de razonamiento del agente, enrutamiento de prompts y herramientas. |
| **Base de Datos Vectorial (FAISS)** | Especificado | Estructuración del índice base con leyes penales de República Dominicana. |
| **Capa de Abstracción LLM** | Especificado | Conector desacoplado mediante variables de entorno para modelos abiertos (Google o Meta). |
| **Interfaz de Usuario (HTML/CSS/JS)** | No iniciado | Diseño de interfaz de chat inspirada en ChatGPT/Claude con soporte para visor de PDF. |
| **Módulo de Supervisión Humana** | Especificado | Definición de mecanismos de control, políticas de privacidad y revisión de respuestas. |

---

## ✨ Funcionalidades

* **Generación de Respuestas Jurídicas**: Procesamiento de peticiones (*prompts*) para responder preguntas complejas (*Q&A*), generar resúmenes ejecutivos y redactar análisis legales penalistas.
* **Generación de Elementos Visuales y Estructurados**: Creación automática de tablas comparativas, diagramas de flujo procesal y líneas de tiempo penal (secuencia de etapas tras una infracción o delito).
* **Ingestión de Documentos PDF**:
  * **Colección Base**: Documentos oficiales y públicos de la legislación penal dominicana pre-indexados en el vectorstore.
  * **Carga de Usuario**: Capacidad de subir expedientes o documentos adicionales en formato **PDF** durante la sesión activa.
* **Gestión Volátil de Sesión**: Operación 100% volátil sin almacenamiento de datos. Los archivos subidos por el usuario se eliminan inmediatamente al reiniciar o salir de la página.
* **Asistencia Orientada al Perfil**: Adaptación del tono y profundidad del contenido según el tipo de consulta (investigación técnica para abogados o concientización preventiva para clientes).

---

## 🏗️ Arquitectura

El sistema implementa una arquitectura desacoplada basada en capas, asegurando flexibilidad y modularidad:

```text
[ Cliente Web (HTML/CSS/JS) ] 
            │ (Peticiones HTTP / JSON)
            ▼
[ API REST (FastAPI en Python) ]
            │
            ├──────► [ Orquestador Agéntico (LangGraph) ]
            │                   │
            │                   ├──────► [ Vectorstore (FAISS) ] ◄── (PDFs Leyes RD / Usuario)
            │                   │
            │                   └──────► [ Modelo Abierto LLM ] ◄── (Vía ENV)
            │
            └──────► [ Capa de Supervisión y Control Humano ]
```

1. **Ingestión y Formateo**: Extracción de texto desde archivos PDF (leyes penales o archivos del usuario).
2. **Indexación Vectorial**: Fragmentación y almacenamiento de *embeddings* en **FAISS**.
3. **Orquestación Conversacional**: **LangGraph** gestiona el ciclo de consulta, recuperación de contexto y decisión del agente.
4. **Inferencia LLM**: Envío de contexto y prompt a un modelo de lenguaje de código abierto (Google o Meta) desacoplado mediante variables de entorno.

---

## 🌐 Acceso

### Usuarios No Técnicos

Los usuarios pueden acceder a la herramienta de forma directa y sin necesidad de instalación ni registro:
* **Demo Web Principal**: Disponible a través del enlace del prototipo alojado en **GitHub Pages**.
* **Modo Simulación (Plan Alternativo)**: En caso de requerirse como entorno de evaluación, se proporciona un enlace a un **Jupyter / Google Colab Notebook** interactivo ejecutable desde el navegador.

---

### Usuarios Técnicos

#### Quickstart (Desarrollo Local)

1. **Clonar el repositorio e ingresar al directorio**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd rag-derecho-penal-rd
   ```

2. **Crear y activar un entorno virtual de Python**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   Crear un archivo `.env` en la raíz del proyecto basándose en el ejemplo proporcionado:
   ```env
   MODEL_PROVIDER=google
   MODEL_NAME=gemma-2b
   ```

5. **Iniciar el servidor backend (FastAPI)**:
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Abrir la interfaz web**:
   Abrir la aplicación en el navegador desde la dirección del servidor local.

---

#### Estructura del Proyecto

```text
rag-derecho-penal-rd/
├── app/
│   ├── main.py              # Punto de entrada de la aplicación FastAPI
│   ├── core/
│   │   ├── config.py        # Configuración global y variables de entorno
│   │   └── security.py      # Controles de volatilidad y seguridad
│   ├── rag/
│   │   ├── chain.py         # Orquestación del flujo RAG con LangGraph
│   │   ├── vectorstore.py   # Gestión del índice FAISS
│   │   └── loader.py        # Procesamiento e ingestión de archivos PDF
│   └── static/
│       ├── index.html       # Interfaz de usuario (UI)
│       ├── css/             # Estilos de la aplicación
│       └── js/              # Lógica de cliente y conexión con FastAPI
├── data/
│   └── base_penal/          # PDFs con las leyes penales base de Rep. Dom.
├── docs/
│   ├── informe_tecnico.pdf  # Informe técnico en formato APA 7
│   └── arquitectura.png     # Diagrama formal de arquitectura
├── .env.example             # Plantilla de variables de entorno
├── .gitignore               # Archivos excluidos del control de versiones
├── README.md                # Documentación principal del proyecto
└── requirements.txt         # Dependencias de Python
```

---

## 🛠️ Tecnologías

* **Lenguaje Backend**: Python 3.12
* **Framework Backend**: FastAPI y Uvicorn
* **Orquestación RAG**: LangGraph y LangChain
* **Base de Datos Vectorial**: FAISS (Facebook AI Similarity Search)
* **Modelos de Lenguaje**: Modelos abiertos de Google o Meta (vía API sin fine-tuning)
* **Kit Frontend**: HTML5, CSS3, JavaScript ES6 (estándar, sin frameworks)
* **Visualizaciones**: Mermaid.js / Formateo dinámico en Markdown
* **Hosting y Despliegue**: GitHub Pages / Repositorios de GitHub

---

## ⚠️ Limitaciones

De acuerdo con las decisiones técnicas acordadas para la entrega del informe y demo del proyecto:

1. **Dominio Especializado Exclusivo**: El sistema está optimizado para el **Derecho Penal de la República Dominicana**. Los archivos de otras áreas del derecho o dominios no penales serán procesados sin enfoque especializado.
2. **Formato Único Soportado**: El pipeline de carga acepta únicamente archivos en formato **PDF**.
3. **Ausencia de Persistencia y Login**: La aplicación no cuenta con base de datos de usuarios ni sistema de autenticación. Todo el estado es volátil y los documentos del usuario se destruyen al finalizar la sesión.
4. **Modelos Abiertos sin Fine-Tuning**: No se realiza entrenamiento a medida (*fine-tuning*) del modelo, basando la precisión exclusivamente en la técnica RAG.
5. **Métricas de Evaluación Postergadas**: Las métricas cuantitativas y el *dataset* de evaluación se desarrollarán en la fase posterior de depuración (*debugging*).

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Para más detalles, consulta el archivo LICENSE.
