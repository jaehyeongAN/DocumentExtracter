import re

def get_pdf_text(filename, backend='tika'):
    if backend == 'tika':
        from tika import parser

        raw = parser.from_file(filename, xmlContent=True)
        body = raw['content'].split('<body>')[1].split('</body>')[0]
        text = re.sub('<[^>]*>', '', body).strip()

    elif backend == 'pdfminer': # 줄바꿈 인식이 제대로 안됨.
        from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
        from pdfminer.converter import TextConverter
        from pdfminer.layout import LAParams
        from pdfminer.pdfpage import PDFPage
        from io import StringIO

        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = "utf-8"
        laparams = LAParams()
        device = TextConverter(
           rsrcmgr, 
           retstr,  
           laparams=laparams
        )
        fp = open(filename, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        pages = PDFPage.get_pages(
            fp, 
            pagenos, 
            maxpages=maxpages, 
            password=password, 
            caching=caching, 
            check_extractable=True
        )
        for page in pages:
            interpreter.process_page(page)

        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
    else:
        text = ''
    
    return text


'''
## pdftotext ##
 > 텍스트 순서가 뒤죽박죽 꼬임.
'''
# # refer to https://pypi.org/project/pdftotext/
# import pdftotext

# def get_pdf_text(filename):
#     file = open(filename, 'rb')
#     file = pdftotext.PDF(file)
#     text = "\n\n".join(file)

#     return str(text)


if __name__ == '__main__':
    import sys
    result = get_pdf_text(sys.argv[1])
    print(result)