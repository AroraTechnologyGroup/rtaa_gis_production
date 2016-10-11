import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

fixture_folder = "data"
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), fixture_folder)

try:
    os.mkdir(out_path)
    os.chdir(out_path)
except OSError:
    if os.path.exists(out_path):
        print("The output folder already exists")
    else:
        print("The output folder does not exist, unexplained OSError")
        raise Exception()

os.chdir(out_path)


def write_text(pdf, t):
    pdf.drawString(0, 0, t)

if __name__ == '__main__':
    for i in range(100):

        text = 'This document is index number {}'.format(i)
        c = canvas.Canvas("DemoDocument{}.pdf".format(i), pagesize=letter)
        c.translate(1*inch, 10.5*inch)
        write_text(c, text)
        c.showPage()
        c.save()
        if not i % 100:
            print(i)
