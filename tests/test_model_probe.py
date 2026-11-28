"""Suite en rojo de la especificación 001 — prueba del proveedor de modelo.

T1 crea estas pruebas antes de que exista ``model_probe.py``. Los clientes se
sustituyen siempre por dobles: no hay red ni credenciales reales.

Nota sobre stderr: la spec escribe literalmente ``RESPUESTA_DE_PRUEBA\\n`` para
stdout pero da los mensajes de error sin salto de línea; por eso stderr se
compara con el texto exacto, sin ``\\n`` final.
"""

import io
import os
import re
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

try:
    import model_probe
except ImportError:  # Estado T1: todavía no hay código de producción.
    model_probe = None


RESPUESTA = "RESPUESTA_DE_PRUEBA"
MENSAJE_PRUEBA = "Hola mundo"

PROVEEDOR_INVALIDO = "Proveedor no válido. Alias admitidos: google, gemini, meta, llama"
FALTAN_CLAVES = "Faltan variables de entorno: "
FALTA_MODELO_GOOGLE = "Falta configuración de modelo para Google: GEMINI_MODEL"
FALTA_MODELO_META = "Falta configuración de modelo para Meta: "
FALLO_ENVIO_GOOGLE = "Fallo de envío con Google"
FALLO_ENVIO_META = "Fallo de envío con Meta"

# Credenciales ficticias: ninguna de estas cadenas debe aparecer en stdout/stderr.
CLAVE_GOOGLE = "SECRETO_GOOGLE_PRUEBA"
CLAVE_META = "SECRETO_META_PRUEBA"
MODELO_GOOGLE = "modelo-gemini-de-prueba"
MODELO_META = "modelo-llama-de-prueba"
BASE_URL_META = "https://meta.example.invalid/v1"
VALORES_SENSIBLES = (CLAVE_GOOGLE, CLAVE_META, MODELO_GOOGLE, MODELO_META, BASE_URL_META)

NOMBRES_ENTORNO = (
    "MODEL_PROVIDER",
    "GEMINI_API_KEY",
    "GEMINI_MODEL",
    "LLAMA_API_KEY",
    "LLAMA_MODEL",
    "LLAMA_BASE_URL",
)
DEPENDENCIAS = ("google-genai", "openai", "python-dotenv")
RAIZ = Path(__file__).resolve().parent.parent


class ErrorSdkFicticio(Exception):
    """Simula una excepción del SDK sin importar ningún SDK real."""


class ErrorTimeoutFicticio(TimeoutError):
    """Simula un timeout del envio."""


class ErrorHttpFicticio(Exception):
    """Simula un error HTTP/no 2xx con secretos en el mensaje."""

    def __init__(self, codigo, detalle=""):
        super().__init__(f"HTTP {codigo}: {detalle}")
        self.codigo = codigo
        self.status_code = codigo


class FabricaDoble:
    """Doble de ``client_factories[proveedor]``; nunca abre red."""

    def __init__(self, respuesta=RESPUESTA, error=None):
        self.respuesta = respuesta
        self.error = error
        self.configuraciones = []
        self.prompts = []

    def __call__(self, configuracion=None, **argumentos):
        if configuracion is None:
            configuracion = argumentos
        elif argumentos:
            configuracion = {**configuracion, **argumentos}
        self.configuraciones.append(dict(configuracion))

        def enviar(prompt):
            self.prompts.append(prompt)
            if self.error is not None:
                raise self.error
            return self.respuesta

        return enviar


class CargadorFalso:
    """Simula un ``.env`` que solo asigna variables no exportadas."""

    def __init__(self, valores):
        self.valores = valores
        self.llamadas = 0

    def __call__(self, *args, **kwargs):
        self.llamadas += 1
        for nombre, valor in self.valores.items():
            os.environ.setdefault(nombre, valor)


def _fabricas_dobles(
    *, respuesta_google=RESPUESTA, respuesta_meta=RESPUESTA, error_google=None, error_meta=None
):
    google = FabricaDoble(respuesta_google, error_google)
    meta = FabricaDoble(respuesta_meta, error_meta)
    return google, meta, {"Google": google, "Meta": meta}


def _entorno_base(**cambios):
    """Entorno completo y determinista; ``None`` elimina la variable."""
    entorno = {
        "MODEL_PROVIDER": "google",
        "GEMINI_API_KEY": CLAVE_GOOGLE,
        "GEMINI_MODEL": MODELO_GOOGLE,
        "LLAMA_API_KEY": CLAVE_META,
        "LLAMA_MODEL": MODELO_META,
        "LLAMA_BASE_URL": BASE_URL_META,
    }
    for nombre, valor in cambios.items():
        if valor is None:
            entorno.pop(nombre, None)
        else:
            entorno[nombre] = valor
    return entorno


def _modos_fallo():
    """Cuatro modos de RF-10, con secretos en los mensajes de excepción."""
    detalle = f"rechazo de {CLAVE_GOOGLE} y {CLAVE_META}"
    return (
        ("excepción del SDK", ErrorSdkFicticio(detalle), RESPUESTA),
        ("timeout", ErrorTimeoutFicticio("tiempo de espera agotado"), RESPUESTA),
        ("error HTTP/no 2xx", ErrorHttpFicticio(500, detalle), RESPUESTA),
        ("respuesta vacía", None, ""),
    )


def _valor_asignado(texto, nombre):
    patron = re.compile(rf"^\s*(?:export\s+)?{re.escape(nombre)}\s*=\s*(.*)$")
    for linea in texto.splitlines():
        coincidencia = patron.match(linea)
        if coincidencia:
            return coincidencia.group(1).strip().strip('"').strip("'")
    return None


def _es_marcador(valor):
    if not valor:
        return True
    normalizado = valor.lower()
    marcas = ("tu-", "tu_", "your", "xxx", "placeholder", "reemplaza", "<", ">", "...", "ejemplo", "example")
    return any(marca in normalizado for marca in marcas)


class PruebaModelProbe(unittest.TestCase):
    """Utilidades compartidas; todas las salidas se capturan en memoria."""

    def setUp(self):
        if model_probe is None:
            self.fail("T1: aún no existe model_probe.py; la suite debe estar en rojo")

    def ejecutar(self, entorno, *, fabricas=None, cargador=None):
        fabricas = fabricas if fabricas is not None else _fabricas_dobles()[2]
        if cargador is None:
            cargador = lambda *args, **kwargs: None
        salida, error = io.StringIO(), io.StringIO()
        with (
            patch.dict(os.environ, entorno, clear=True),
            patch.object(model_probe, "load_environment", cargador),
            patch.dict(model_probe.client_factories, fabricas, clear=True),
            redirect_stdout(salida),
            redirect_stderr(error),
        ):
            codigo = model_probe.main()
        return codigo, salida.getvalue(), error.getvalue()

    def assertSinSecretos(self, salida, error, valores=VALORES_SENSIBLES):
        # Un assertTrue evita que el propio fallo imprima el valor sensible.
        texto = salida + error
        self.assertTrue(all(valor not in texto for valor in valores), "Apareció un valor sensible en la salida")

    def assertSinEnvio(self, *fabricas):
        for fabrica in fabricas:
            self.assertTrue(not fabrica.configuraciones, "No debió construirse el cliente")
            self.assertTrue(not fabrica.prompts, "No debió enviarse el mensaje")

    def assertFabricaRecibio(self, fabrica, esperado):
        self.assertEqual(len(fabrica.configuraciones), 1, "La fábrica debió recibir una configuración")
        configuracion = fabrica.configuraciones[0]
        self.assertEqual(set(configuracion), set(esperado), "Claves de configuración inesperadas")
        self.assertTrue(
            all(configuracion.get(clave) == valor for clave, valor in esperado.items()),
            "La fábrica recibió valores de configuración incorrectos",
        )


class TestAliasYEnvio(PruebaModelProbe):
    """RF-02, RF-06, RF-08 y RF-09."""

    def test_google_envia_hola_mundo_y_solo_imprime_respuesta(self):
        for alias in ("google", "gemini", " google "):
            with self.subTest(alias=alias):
                google, meta, fabricas = _fabricas_dobles()
                codigo, salida, error = self.ejecutar(
                    _entorno_base(MODEL_PROVIDER=alias), fabricas=fabricas
                )
                self.assertEqual(codigo, 0)
                self.assertEqual(salida, RESPUESTA + "\n")
                self.assertEqual(error, "")
                self.assertEqual(google.prompts, [MENSAJE_PRUEBA])
                self.assertFabricaRecibio(
                    google,
                    {"provider": "Google", "api_key": CLAVE_GOOGLE, "model": MODELO_GOOGLE},
                )
                self.assertSinEnvio(meta)
                self.assertSinSecretos(salida, error)

    def test_meta_envia_hola_mundo_y_solo_imprime_respuesta(self):
        for alias in ("meta", "llama", " llama "):
            with self.subTest(alias=alias):
                google, meta, fabricas = _fabricas_dobles()
                codigo, salida, error = self.ejecutar(
                    _entorno_base(MODEL_PROVIDER=alias), fabricas=fabricas
                )
                self.assertEqual(codigo, 0)
                self.assertEqual(salida, RESPUESTA + "\n")
                self.assertEqual(error, "")
                self.assertEqual(meta.prompts, [MENSAJE_PRUEBA])
                self.assertFabricaRecibio(
                    meta,
                    {
                        "provider": "Meta",
                        "api_key": CLAVE_META,
                        "model": MODELO_META,
                        "base_url": BASE_URL_META,
                    },
                )
                self.assertSinEnvio(google)
                self.assertSinSecretos(salida, error)


class TestValidacionesPrevias(PruebaModelProbe):
    """RF-03, RF-04, RF-05 y RF-11."""

    def test_claves_ausentes_vacias_o_solo_espacios(self):
        casos = (
            ("google", {"GEMINI_API_KEY": None}, FALTAN_CLAVES + "GEMINI_API_KEY"),
            ("google", {"GEMINI_API_KEY": ""}, FALTAN_CLAVES + "GEMINI_API_KEY"),
            ("google", {"GEMINI_API_KEY": "   "}, FALTAN_CLAVES + "GEMINI_API_KEY"),
            ("meta", {"LLAMA_API_KEY": None}, FALTAN_CLAVES + "LLAMA_API_KEY"),
            ("meta", {"LLAMA_API_KEY": ""}, FALTAN_CLAVES + "LLAMA_API_KEY"),
            ("meta", {"LLAMA_API_KEY": "   "}, FALTAN_CLAVES + "LLAMA_API_KEY"),
            (
                "google",
                {"GEMINI_API_KEY": None, "LLAMA_API_KEY": None},
                FALTAN_CLAVES + "GEMINI_API_KEY, LLAMA_API_KEY",
            ),
            (
                "google",
                {"GEMINI_API_KEY": "   ", "LLAMA_API_KEY": "   "},
                FALTAN_CLAVES + "GEMINI_API_KEY, LLAMA_API_KEY",
            ),
        )
        for proveedor, cambios, esperado in casos:
            with self.subTest(proveedor=proveedor, cambios=cambios):
                google, meta, fabricas = _fabricas_dobles()
                codigo, salida, error = self.ejecutar(
                    _entorno_base(MODEL_PROVIDER=proveedor, **cambios), fabricas=fabricas
                )
                self.assertEqual(codigo, 1)
                self.assertEqual(salida, "")
                self.assertEqual(error, esperado)
                self.assertSinSecretos(salida, error)
                self.assertSinEnvio(google, meta)

    def test_proveedor_no_admitido_aun_con_claves_ausentes(self):
        valores = (None, "openai", "GOOGLE", "Gemini", "goo gle", MODELO_GOOGLE, "", "   ")
        for valor in valores:
            with self.subTest(valor=valor):
                google, meta, fabricas = _fabricas_dobles()
                cambios = {"MODEL_PROVIDER": valor}
                cambios.update({nombre: None for nombre in NOMBRES_ENTORNO[1:]})
                codigo, salida, error = self.ejecutar(
                    _entorno_base(**cambios), fabricas=fabricas
                )
                self.assertEqual(codigo, 1)
                self.assertEqual(salida, "")
                self.assertEqual(error, PROVEEDOR_INVALIDO)
                self.assertSinSecretos(salida, error)
                self.assertSinEnvio(google, meta)

    def test_rf11_falta_gemini_model(self):
        google, meta, fabricas = _fabricas_dobles()
        codigo, salida, error = self.ejecutar(
            _entorno_base(MODEL_PROVIDER="google", GEMINI_MODEL=None), fabricas=fabricas
        )
        self.assertEqual(codigo, 1)
        self.assertEqual(salida, "")
        self.assertEqual(error, FALTA_MODELO_GOOGLE)
        self.assertSinSecretos(salida, error)
        self.assertSinEnvio(google, meta)

    def test_rf11_falta_configuracion_de_modelo_de_meta(self):
        casos = (
            (
                {"LLAMA_BASE_URL": None, "LLAMA_MODEL": None},
                FALTA_MODELO_META + "LLAMA_BASE_URL, LLAMA_MODEL",
            ),
            ({"LLAMA_MODEL": None}, FALTA_MODELO_META + "LLAMA_MODEL"),
            ({"LLAMA_BASE_URL": None}, FALTA_MODELO_META + "LLAMA_BASE_URL"),
        )
        for cambios, esperado in casos:
            with self.subTest(cambios=cambios):
                google, meta, fabricas = _fabricas_dobles()
                codigo, salida, error = self.ejecutar(
                    _entorno_base(MODEL_PROVIDER="meta", **cambios), fabricas=fabricas
                )
                self.assertEqual(codigo, 1)
                self.assertEqual(salida, "")
                self.assertEqual(error, esperado)
                self.assertSinSecretos(salida, error)
                self.assertSinEnvio(google, meta)

    def test_precedencia_proveedor_invalido_antes_de_claves_y_modelo(self):
        google, meta, fabricas = _fabricas_dobles()
        cambios = {"MODEL_PROVIDER": "openai"}
        cambios.update({nombre: None for nombre in NOMBRES_ENTORNO[1:]})
        codigo, salida, error = self.ejecutar(_entorno_base(**cambios), fabricas=fabricas)
        self.assertEqual(codigo, 1)
        self.assertEqual(salida, "")
        self.assertEqual(error, PROVEEDOR_INVALIDO)
        self.assertTrue(
            "Faltan" not in error and "configuración" not in error and "Fallo de envío" not in error,
            "Solo debe informarse el error de proveedor",
        )
        self.assertSinSecretos(salida, error)
        self.assertSinEnvio(google, meta)


class TestFalloDeEnvio(PruebaModelProbe):
    """RF-10 y nombre canónico del proveedor en stderr (RF-08)."""

    def test_rf10_fallo_de_envio_con_google(self):
        for modo, error_fabricacion, respuesta in _modos_fallo():
            with self.subTest(modo=modo):
                google, meta, fabricas = _fabricas_dobles(
                    respuesta_google=respuesta, error_google=error_fabricacion
                )
                codigo, salida, error = self.ejecutar(
                    _entorno_base(MODEL_PROVIDER="gemini"), fabricas=fabricas
                )
                self.assertEqual(codigo, 1)
                self.assertEqual(salida, "")
                self.assertEqual(error, FALLO_ENVIO_GOOGLE)
                self.assertEqual(google.prompts, [MENSAJE_PRUEBA])
                self.assertSinSecretos(salida, error)
                self.assertSinEnvio(meta)

    def test_rf10_fallo_de_envio_con_meta(self):
        for modo, error_fabricacion, respuesta in _modos_fallo():
            with self.subTest(modo=modo):
                google, meta, fabricas = _fabricas_dobles(
                    respuesta_meta=respuesta, error_meta=error_fabricacion
                )
                codigo, salida, error = self.ejecutar(
                    _entorno_base(MODEL_PROVIDER="llama"), fabricas=fabricas
                )
                self.assertEqual(codigo, 1)
                self.assertEqual(salida, "")
                self.assertEqual(error, FALLO_ENVIO_META)
                self.assertEqual(meta.prompts, [MENSAJE_PRUEBA])
                self.assertSinSecretos(salida, error)
                self.assertSinEnvio(google)


class TestConfidencialidad(PruebaModelProbe):
    """RF-01 y RF-07."""

    def test_rf07_clave_ficticia_entregada_no_aparece_en_la_salida(self):
        google, meta, fabricas = _fabricas_dobles()
        codigo, salida, error = self.ejecutar(_entorno_base(), fabricas=fabricas)
        self.assertEqual(codigo, 0)
        self.assertEqual(salida, RESPUESTA + "\n")
        self.assertTrue(
            CLAVE_GOOGLE in google.configuraciones[0].values(),
            "El doble debió recibir la clave ficticia",
        )
        self.assertSinSecretos(salida, error)

    def test_rf07_nombres_permitidos_pero_valores_no(self):
        google, meta, fabricas = _fabricas_dobles()
        codigo, salida, error = self.ejecutar(
            _entorno_base(GEMINI_API_KEY=None), fabricas=fabricas
        )
        self.assertEqual(codigo, 1)
        self.assertEqual(error, FALTAN_CLAVES + "GEMINI_API_KEY")
        self.assertIn("GEMINI_API_KEY", error)
        self.assertSinSecretos(salida, error)
        self.assertSinEnvio(google, meta)

    def test_rf01_precedencia_de_exportadas_sobre_el_archivo_env(self):
        casos = (
            (
                "google",
                {
                    "GEMINI_API_KEY": "SECRETO_EXPORTADO_GOOGLE",
                    "GEMINI_MODEL": "modelo-exportado-gemini",
                },
                {
                    "GEMINI_API_KEY": "SECRETO_ENV_GOOGLE",
                    "GEMINI_MODEL": "modelo-del-env-gemini",
                },
            ),
            (
                "meta",
                {
                    "LLAMA_API_KEY": "SECRETO_EXPORTADO_META",
                    "LLAMA_MODEL": "modelo-exportado-llama",
                    "LLAMA_BASE_URL": "https://exportado.example.invalid/v1",
                },
                {
                    "LLAMA_API_KEY": "SECRETO_ENV_META",
                    "LLAMA_MODEL": "modelo-del-env-llama",
                    "LLAMA_BASE_URL": "https://del-env.example.invalid/v1",
                },
            ),
        )
        for proveedor, exportadas, del_archivo in casos:
            with self.subTest(proveedor=proveedor):
                google, meta, fabricas = _fabricas_dobles()
                cargador = CargadorFalso(del_archivo)
                codigo, salida, error = self.ejecutar(
                    _entorno_base(MODEL_PROVIDER=proveedor, **exportadas),
                    fabricas=fabricas,
                    cargador=cargador,
                )
                self.assertEqual(codigo, 0)
                self.assertEqual(salida, RESPUESTA + "\n")
                self.assertEqual(error, "")
                self.assertEqual(cargador.llamadas, 1, "main debe cargar el entorno una vez")
                if proveedor == "google":
                    fabrica = google
                    esperado = {
                        "provider": "Google",
                        "api_key": exportadas["GEMINI_API_KEY"],
                        "model": exportadas["GEMINI_MODEL"],
                    }
                else:
                    fabrica = meta
                    esperado = {
                        "provider": "Meta",
                        "api_key": exportadas["LLAMA_API_KEY"],
                        "model": exportadas["LLAMA_MODEL"],
                        "base_url": exportadas["LLAMA_BASE_URL"],
                    }
                self.assertFabricaRecibio(fabrica, esperado)
                valores = VALORES_SENSIBLES + tuple(exportadas.values()) + tuple(del_archivo.values())
                self.assertSinSecretos(salida, error, valores=valores)


class TestArtefactos(PruebaModelProbe):
    """CA-10: se activa en T5; en T1-T4 ambos archivos están ausentes."""

    @unittest.skipUnless(
        (RAIZ / "requirements.txt").is_file() and (RAIZ / ".env.example").is_file(),
        "T5: aún no existen requirements.txt ni .env.example",
    )
    def test_ca10_dependencias_y_plantilla_de_entorno(self):
        requisitos = (RAIZ / "requirements.txt").read_text(encoding="utf-8")
        plantilla = (RAIZ / ".env.example").read_text(encoding="utf-8")
        self.assertTrue(
            all(dependencia in requisitos for dependencia in DEPENDENCIAS),
            "Faltan dependencias en requirements.txt",
        )
        self.assertTrue(
            all(nombre in plantilla for nombre in NOMBRES_ENTORNO),
            "Faltan nombres de variables en .env.example",
        )
        for nombre in ("GEMINI_API_KEY", "LLAMA_API_KEY"):
            valor = _valor_asignado(plantilla, nombre)
            if valor is not None:
                self.assertTrue(_es_marcador(valor), "La plantilla no debe incluir credenciales reales")
        self.assertTrue(
            all(marca not in plantilla for marca in ("AIza", "sk-", CLAVE_GOOGLE, CLAVE_META)),
            "La plantilla no debe incluir credenciales reales",
        )


if __name__ == "__main__":
    unittest.main()
