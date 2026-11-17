from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_report(content, filename="business_report.pdf"):

    pdf = canvas.Canvas(filename, pagesize=A4)

    width, height = A4

    y = height - 60

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(
        50,
        y,
        "RetailOps AI - Business Report"
    )

    y -= 40

    pdf.setFont("Helvetica", 10)

    for line in content.split("\n"):

        if y < 50:

            pdf.showPage()

            y = height - 50

            pdf.setFont("Helvetica", 10)

        pdf.drawString(
            50,
            y,
            line[:110]
        )

        y -= 18

    pdf.save()

    return filename