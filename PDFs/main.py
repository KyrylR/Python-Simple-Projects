import sys

import PyPDF2

inputs = sys.argv[1:]


def pdf_combiner(pdf_list):
    merger = PyPDF2.PdfFileMerger()
    for pdf in pdf_list:
        print(pdf)
        merger.append(pdf)
    merger.write('data/super.pdf')


def pdf_watermark():
    template = PyPDF2.PdfFileReader(open('data/super.pdf', 'rb'))
    watermark = PyPDF2.PdfFileReader(open('data/wtr.pdf', 'rb'))
    result = PyPDF2.PdfFileWriter()

    for i in range(template.getNumPages()):
        page = template.getPage(i)
        page.mergePage(watermark.getPage(0))
        result.addPage(page)

    with open('data/wtr_res.pdf', 'wb') as file:
        result.write(file)


if __name__ == '__main__':
    # # Rotate pdf
    # with open('data/dummy.pdf', 'rb') as file:
    #     reader = PyPDF2.PdfFileReader(file)
    #     page = reader.getPage(0)
    #     page.rotateCounterClockwise(90)
    #     writer = PyPDF2.PdfFileWriter()
    #     writer.addPage(page)
    #     with open('data/tilt.pdf', 'wb') as wfile:
    #         writer.write(wfile)

    pdf_watermark()
    pass
