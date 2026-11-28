"""Prueba de preparación del proveedor de modelo (especificación 001).

Carga del entorno, validaciones previas al envío y envío del mensaje de prueba.
Los SDK se importan de forma perezosa dentro de las fábricas; los mensajes son
literales y nunca incluyen valores de credenciales ni de configuración.
"""

import os
import sys

MENSAJE_PROVEEDOR_INVALIDO = "Proveedor no válido. Alias admitidos: google, gemini, meta, llama"
MENSAJE_CLAVES_FALTANTES = "Faltan variables de entorno: "
MENSAJE_MODELO_GOOGLE = "Falta configuración de modelo para Google: GEMINI_MODEL"
MENSAJE_MODELO_META = "Falta configuración de modelo para Meta: "
MENSAJE_FALLO_GOOGLE = "Fallo de envío con Google"
MENSAJE_FALLO_META = "Fallo de envío con Meta"
MENSAJE_PRUEBA = "Hola mundo"

ALIASES = {
    "google": "Google",
    "gemini": "Google",
    "meta": "Meta",
    "llama": "Meta",
}
CLAVES = ("GEMINI_API_KEY", "LLAMA_API_KEY")
CONFIGURACION_MODELO = {
    "Google": ("GEMINI_MODEL",),
    "Meta": ("LLAMA_BASE_URL", "LLAMA_MODEL"),
}


def load_environment():
    """Carga ``.env`` sin sobrescribir las variables ya exportadas.

    ``python-dotenv`` se declara en T5; si todavía no está instalado, la prueba
    continúa solo con el entorno exportado y no escribe nada.
    """
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(override=False)


def _fabrica_google(configuracion):
    """Crea un cliente google-genai y devuelve su función de envío."""
    from google import genai

    cliente = genai.Client(api_key=configuracion["api_key"])
    modelo = configuracion["model"]

    def enviar(prompt):
        respuesta = cliente.models.generate_content(model=modelo, contents=prompt)
        return respuesta.text

    return enviar


def _fabrica_meta(configuracion):
    """Crea un cliente OpenAI compatible y devuelve su función de envío."""
    from openai import OpenAI

    cliente = OpenAI(api_key=configuracion["api_key"], base_url=configuracion["base_url"])
    modelo = configuracion["model"]

    def enviar(prompt):
        respuesta = cliente.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt}],
        )
        return respuesta.choices[0].message.content

    return enviar


client_factories = {"Google": _fabrica_google, "Meta": _fabrica_meta}


def _valor(nombre):
    """Devuelve la variable recortada; nunca se imprime su contenido."""
    return os.environ.get(nombre, "").strip()


def _falta(nombre):
    return not _valor(nombre)


def _escribir_error(mensaje):
    sys.stderr.write(mensaje)


def _resolver_proveedor():
    """Devuelve el nombre canónico o ``None`` si el alias no es admitido."""
    return ALIASES.get(_valor("MODEL_PROVIDER"))


def _configuracion(proveedor):
    """Construye el diccionario exacto entregado a la fábrica del proveedor."""
    if proveedor == "Google":
        return {
            "provider": "Google",
            "api_key": _valor("GEMINI_API_KEY"),
            "model": _valor("GEMINI_MODEL"),
        }
    return {
        "provider": "Meta",
        "api_key": _valor("LLAMA_API_KEY"),
        "model": _valor("LLAMA_MODEL"),
        "base_url": _valor("LLAMA_BASE_URL"),
    }


def main() -> int:
    load_environment()

    proveedor = _resolver_proveedor()
    if proveedor is None:
        _escribir_error(MENSAJE_PROVEEDOR_INVALIDO)
        return 1

    claves_faltantes = [nombre for nombre in CLAVES if _falta(nombre)]
    if claves_faltantes:
        _escribir_error(MENSAJE_CLAVES_FALTANTES + ", ".join(claves_faltantes))
        return 1

    modelo_faltante = [nombre for nombre in CONFIGURACION_MODELO[proveedor] if _falta(nombre)]
    if modelo_faltante:
        if proveedor == "Google":
            _escribir_error(MENSAJE_MODELO_GOOGLE)
        else:
            _escribir_error(MENSAJE_MODELO_META + ", ".join(modelo_faltante))
        return 1

    mensaje_fallo = MENSAJE_FALLO_GOOGLE if proveedor == "Google" else MENSAJE_FALLO_META
    try:
        enviar = client_factories[proveedor](_configuracion(proveedor))
        respuesta = enviar(MENSAJE_PRUEBA)
        if not isinstance(respuesta, str) or not respuesta.strip():
            raise ValueError("respuesta vacía")
    except Exception:
        # Sin enlace a la excepción: nunca se imprime su mensaje ni una traza.
        _escribir_error(mensaje_fallo)
        return 1

    sys.stdout.write(respuesta + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
