import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

os.chdir(r"C:\\FileTransferFTP\\eDoc")
out_folder = os.curdir
print(os.path.abspath(out_folder))


def write_text(pdf, t):
    pdf.drawString(0, 0, t)

for i in range(5000):

    text = 'This document is index number {}'.format(i)
    c = canvas.Canvas("DemoDocument{}.pdf".format(i), pagesize=letter)
    c.translate(1*inch, 10.5*inch)
    write_text(c, text)
    c.showPage()
    c.save()
    if not i % 100:
        print(i)
