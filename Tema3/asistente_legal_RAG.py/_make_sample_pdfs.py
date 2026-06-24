"""
Genera PDFs de ejemplo (contratos de arrendamiento ficticios) en ./documentos
para poder probar el Asistente Legal RAG.

Uso:  uv run --with reportlab python _make_sample_pdfs.py
"""

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

DOCS_DIR = "./documentos"

styles = getSampleStyleSheet()
h = ParagraphStyle("h", parent=styles["Heading1"], fontSize=14, spaceAfter=10)
sub = ParagraphStyle("sub", parent=styles["Heading2"], fontSize=11, spaceAfter=6)
body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=10, leading=15)


def build(filename, titulo, clausulas):
    path = os.path.join(DOCS_DIR, filename)
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)
    flow = [Paragraph(titulo, h), Spacer(1, 6)]
    for sub_titulo, texto in clausulas:
        flow.append(Paragraph(sub_titulo, sub))
        flow.append(Paragraph(texto, body))
        flow.append(Spacer(1, 8))
    doc.build(flow)
    print(f"Creado: {path}")


CONTRATO_1 = (
    "CONTRATO DE ARRENDAMIENTO DE VIVIENDA",
    [
        ("PRIMERA. Partes",
         "De una parte D. Carlos Méndez Ruiz, con DNI 12345678A, como ARRENDADOR; "
         "y de otra Dña. Laura Gómez Pérez, con DNI 87654321B, como ARRENDATARIA."),
        ("SEGUNDA. Objeto e inmueble",
         "El inmueble objeto del contrato es la vivienda sita en Calle Larios nº 10, "
         "3º B, 29005 Málaga, con referencia catastral 1234567AB. Se destina "
         "exclusivamente a vivienda habitual de la arrendataria."),
        ("TERCERA. Duración",
         "El contrato tendrá una duración de cinco (5) años, con inicio el 1 de "
         "enero de 2025 y finalización el 31 de diciembre de 2029, prorrogable "
         "conforme a la Ley de Arrendamientos Urbanos."),
        ("CUARTA. Renta",
         "La renta mensual se fija en SETECIENTOS CINCUENTA EUROS (750 €), pagaderos "
         "dentro de los cinco primeros días de cada mes mediante transferencia "
         "bancaria. La renta se actualizará anualmente según el IPC."),
        ("QUINTA. Fianza",
         "La arrendataria entrega en este acto la cantidad de SETECIENTOS CINCUENTA "
         "EUROS (750 €) en concepto de fianza legal, equivalente a una mensualidad."),
        ("SEXTA. Gastos",
         "Serán por cuenta de la arrendataria los gastos de suministros de agua, "
         "luz, gas e internet. El IBI y los gastos de comunidad corresponden al "
         "arrendador."),
        ("SÉPTIMA. Obras y conservación",
         "La arrendataria no podrá realizar obras sin consentimiento escrito del "
         "arrendador. Las reparaciones necesarias para conservar la vivienda en "
         "condiciones de habitabilidad corresponden al arrendador."),
    ],
)

CONTRATO_2 = (
    "CONTRATO DE ARRENDAMIENTO DE LOCAL COMERCIAL",
    [
        ("PRIMERA. Partes",
         "De una parte Inversiones Sur S.L., con CIF B11223344, como ARRENDADORA; "
         "y de otra D. Javier Torres Lima, con DNI 11223344C, como ARRENDATARIO."),
        ("SEGUNDA. Objeto e inmueble",
         "Local comercial situado en Avenida de Andalucía nº 25, planta baja, "
         "28010 Madrid, de 80 m². Se destinará a la actividad de cafetería."),
        ("TERCERA. Duración",
         "La duración pactada es de tres (3) años, desde el 1 de marzo de 2025 "
         "hasta el 28 de febrero de 2028."),
        ("CUARTA. Renta",
         "La renta mensual asciende a MIL DOSCIENTOS EUROS (1.200 €) más el IVA "
         "correspondiente, pagaderos por mensualidades anticipadas."),
        ("QUINTA. Fianza",
         "El arrendatario deposita una fianza equivalente a dos (2) mensualidades, "
         "es decir, DOS MIL CUATROCIENTOS EUROS (2.400 €)."),
        ("SEXTA. Cesión y subarriendo",
         "Queda prohibida la cesión del contrato o el subarriendo del local sin "
         "autorización expresa y por escrito de la arrendadora."),
        ("SÉPTIMA. Resolución",
         "El impago de dos mensualidades consecutivas será causa de resolución "
         "del contrato, así como el cambio de la actividad pactada."),
    ],
)


def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    build("contrato_vivienda.pdf", *CONTRATO_1)
    build("contrato_local_comercial.pdf", *CONTRATO_2)
    print("\nListo. Ahora ejecuta:  uv run python ingest.py")


if __name__ == "__main__":
    main()
