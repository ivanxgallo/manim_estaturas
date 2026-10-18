# Estatura en Chile: fuente, cálculo y límites de la validación

## Parámetros actuales del video

Por indicación del usuario, la animación usa **media 172 cm** y **desviación
estándar 7 cm**. No se ha identificado la encuesta, el año ni el rango de
edad del que proceden. Se documentan como **estimaciones elegidas por el usuario**, no como cifras
de ENS ni como valores contrastados en una fuente oficial. El usuario
indicó que explicará esta condición en su narración; por eso no se muestran
advertencias sobre la estimación en pantalla. La validación de una fuente
queda pendiente, sin bloquear el video con los parámetros solicitados.

Con esos parámetros, el modelo normal da aproximadamente **0,506 %** sobre
190 cm, o **1 de cada 197 personas bajo el modelo**. El video recalcula estos
resultados al editar las constantes; no usa los parámetros de la comparación
ENS que sigue.

## Comparación independiente: encuesta y procedencia

La fuente estadística elegida es la **Encuesta Nacional de Salud (ENS)
2016-2017 de Chile**, del Ministerio de Salud. Su población objetivo es de
15 años y más. Para evitar mezclar distribuciones por sexo, el análisis de comparación siguiente se
refiere exclusivamente a **hombres de 15 años y más**; no a toda la población
chilena ni exclusivamente a mayores de 18 años.

Portal oficial para contrastar la encuesta:
<https://epi.minsal.cl/encuesta-ens/>.

**Validación pendiente:** la política de red de este entorno impidió consultar
Minsal (HTTP 403). No se ha verificado una tabla del informe oficial que
publique la media, ni se ha comparado el archivo con una descarga directa
de Minsal. Los resultados siguientes son cálculos propios de una **copia
pública académica de los microdatos**, no cifras transcritas del informe.
Estos cálculos no validan los parámetros 172 y 7 elegidos por el usuario.

Se consultó el repositorio de un trabajo del Magíster en Ciencias Sociales
de la Universidad de Chile, cuyo README identifica expresamente ENS 2016-2017
como fuente. El repositorio pertenece al autor del trabajo, no a Minsal:

- [Descripción del trabajo y autor](https://github.com/eduardo-vq/ens20162017/tree/eb5edf9f622654d20bb72ed339ef7e472dae6549).
- [Copia de ENS_F1_2_.sav](https://github.com/eduardo-vq/ens20162017/blob/eb5edf9f622654d20bb72ed339ef7e472dae6549/Datos/Datos%20Originales/ENS_F1_2_.sav).
- [Libro de códigos F2](https://github.com/eduardo-vq/ens20162017/blob/eb5edf9f622654d20bb72ed339ef7e472dae6549/Datos/Datos%20Originales/Libros%20de%20C%C3%B3digo/Libro-de-C%C3%B3digos-F2%20.pdf).

La copia se fijó al commit `eb5edf9f622654d20bb72ed339ef7e472dae6549`.
Su SHA-256 es
`9873b421d446190070bfff6495321fb152485c47457692936dbcd18c542eb89a`.
El SHA-256 permite identificar y reproducir el archivo usado; no certifica
su autenticidad frente a Minsal.

## Variables y estimación

El libro de códigos F2 identifica:

- `m4p2`: «Indique medida de Talla (cm)». Reporta 5.495 mediciones válidas
  para ambos sexos; ese recuento coincide con la copia de datos consultada.
- `Sexo`: código `1` para hombre, `2` para mujer.
- `Edad`: se conserva el universo de 15 años y más.
- `Fexp_F2p_Corr`: ponderador postestratificado para F2, truncado al percentil
  99,5. Se usa el de F2 porque la talla corresponde a esta medición.

Se excluyen tallas ausentes, no finitas o no positivas, incluidos los códigos
negativos de rechazo y error, y ponderadores ausentes o no positivos. No se
eliminan observaciones altas o bajas válidas por criterio ad hoc.

Para las **2.012 mediciones válidas de hombres**:

| Estadístico | Cálculo en la copia de los microdatos |
|---|---:|
| Media ponderada | 169,6179385 cm |
| Desviación descriptiva ponderada | 7,2607437 cm |
| Estadísticos de esta copia, redondeados | 169,62 cm y 7,26 cm |
| Cola normal sobre 190 cm, con parámetros sin redondear | 0,2499029 % |
| Proporción ponderada observada sobre 190 cm | 0,4752017 % |
| Observaciones individuales sobre 190 cm | 6 |

La media es `sum(w*h)/sum(w)`. La desviación es la raíz de
`sum(w*(h-media)**2)/sum(w)`: un momento descriptivo ponderado, no el error
estándar de la media ni un intervalo de confianza. No se aplican fórmulas
de muestreo aleatorio simple para inferir precisión: ENS tiene diseño
complejo y se necesitarían estratos, conglomerados y su documentación.

## Modelo normal y cola observada

Si se calcula `P(H>190)` suponiendo una normal con los momentos de esta copia, da aproximadamente **0,25 %, o 1 de cada 400 personas de esa población bajo
el modelo**. No equivale a una frecuencia empírica demostrada. La diferencia
con la proporción ponderada observada (aproximadamente 0,48 %) muestra que
el ajuste de la cola merece análisis; solo seis mediciones superan 190 cm,
y no se ha estimado aquí su incertidumbre con el diseño de encuesta.

El teorema central del límite (**TCL**) explica la convergencia de ciertas
sumas centradas y escaladas. No garantiza que las estaturas sean normales
ni que el modelo describa con precisión una cola extrema.

## Reproducir

El renderizado no descarga ni utiliza registros individuales. Usa los
parámetros propuestos por el usuario en `estaturas.py`. El script de
análisis independiente permite comparar con la copia ENS y no modifica
los parámetros del video.

Para reproducir el cálculo, opcionalmente instala el lector SPSS y ejecuta:

```bash
.venv/bin/python -m pip install pyreadstat==1.3.6
.venv/bin/python analizar_ens.py --descargar-copia-publica --salida resultados_ens.json
```

O utiliza `--archivo /ruta/ENS_F1_2_.sav` con la base que descargues directamente
de Minsal. El script informa el hash usado y guarda únicamente estadísticos
agregados. Un archivo distinto puede producir resultados diferentes: debe
documentarse su versión y comprobarse el diccionario y los ponderadores.
