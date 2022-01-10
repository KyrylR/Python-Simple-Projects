import PyPDF2

if __name__ == '__main__':
    with open('data/dummy.pdf', 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        page = reader.getPage(0)
        print(page)