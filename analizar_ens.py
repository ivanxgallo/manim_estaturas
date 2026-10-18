"""Reproduce estadísticos agregados de talla de ENS 2016-2017.

Requiere: python -m pip install numpy pyreadstat==1.3.6
Uso con la copia identificada en FUENTES.md:
    python analizar_ens.py --descargar-copia-publica --salida resultados_ens.json
O con un archivo obtenido de Minsal:
    python analizar_ens.py --archivo /ruta/ENS_F1_2_.sav
No muestra ni guarda registros individuales.
"""

import argparse
import hashlib
import json
from math import erfc, sqrt
from pathlib import Path
import tempfile
import urllib.request

import numpy as np
import pyreadstat


COMMIT_COPIA = "eb5edf9f622654d20bb72ed339ef7e472dae6549"
URL_COPIA = (
    "https://raw.githubusercontent.com/eduardo-vq/ens20162017/"
    + COMMIT_COPIA + "/Datos/Datos%20Originales/ENS_F1_2_.sav"
)
SHA256_COPIA = "9873b421d446190070bfff6495321fb152485c47457692936dbcd18c542eb89a"


def analizar(archivo):
    columnas = ["Sexo", "Edad", "m4p2", "Fexp_F2p_Corr"]
    datos, meta = pyreadstat.read_sav(archivo, usecols=columnas, output_format="dict")
    talla, peso, sexo, edad = [np.asarray(datos[c], dtype=float) for c in
                              ["m4p2", "Fexp_F2p_Corr", "Sexo", "Edad"]]
    if meta.variable_value_labels.get("Sexo", {}).get(1.0, "").upper() != "HOMBRE":
        raise ValueError("El código de sexo no coincide con el libro de códigos.")
    validos = (np.isfinite(talla) & (talla > 0) & np.isfinite(peso) & (peso > 0)
               & np.isfinite(edad) & (edad >= 15) & (sexo == 1))
    h, w = talla[validos], peso[validos]
    if len(h) < 2:
        raise ValueError("No hay suficientes mediciones válidas.")
    media = float(np.average(h, weights=w))
    desviacion = float(np.sqrt(np.average((h - media) ** 2, weights=w)))
    if desviacion <= 0:
        raise ValueError("La desviación debe ser positiva.")
    probabilidad_normal = 0.5 * erfc((190 - media) / (desviacion * sqrt(2)))
    return {
        "encuesta": "Encuesta Nacional de Salud 2016-2017, Chile",
        "poblacion": "Hombres de 15 años y más con medición válida de talla",
        "fuente_del_calculo": "Microdatos, no tabla de resultados publicada",
        "archivo_sha256": hashlib.sha256(Path(archivo).read_bytes()).hexdigest(),
        "coincide_con_copia_publica_documentada": hashlib.sha256(Path(archivo).read_bytes()).hexdigest() == SHA256_COPIA,
        "variable_talla_cm": "m4p2",
        "ponderador": "Fexp_F2p_Corr",
        "n_mediciones": int(len(h)),
        "media_cm": media,
        "desviacion_descriptiva_ponderada_cm": desviacion,
        "definicion_varianza": "sum(w * (h - media)**2) / sum(w)",
        "umbral_cm": 190,
        "probabilidad_normal": probabilidad_normal,
        "proporcion_observada_ponderada": float(np.average(h > 190, weights=w)),
        "n_mediciones_sobre_190": int(np.sum(h > 190)),
        "advertencia": "Estimación descriptiva; no calcula errores estándar ni IC del diseño complejo.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    opciones = parser.add_mutually_exclusive_group(required=True)
    opciones.add_argument("--archivo", type=Path)
    opciones.add_argument("--descargar-copia-publica", action="store_true")
    parser.add_argument("--salida", type=Path)
    args = parser.parse_args()
    if args.descargar_copia_publica:
        with tempfile.TemporaryDirectory(prefix="ens_microdatos_") as carpeta:
            archivo = Path(carpeta) / "ENS_F1_2_.sav"
            urllib.request.urlretrieve(URL_COPIA, archivo)
            if hashlib.sha256(archivo.read_bytes()).hexdigest() != SHA256_COPIA:
                raise ValueError("La copia descargada no coincide con el SHA-256 documentado.")
            resultado = analizar(archivo)
    else:
        resultado = analizar(args.archivo)
    contenido = json.dumps(resultado, ensure_ascii=False, indent=2) + "\n"
    print(contenido, end="")
    if args.salida:
        args.salida.write_text(contenido, encoding="utf-8")


if __name__ == "__main__":
    main()
