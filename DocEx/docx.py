try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile

NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = NAMESPACE + 'p'
TEXT = NAMESPACE + 't'


def get_docx_text(filename):
    document = zipfile.ZipFile(filename)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)
    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        paragraphs.append('\n')
        for node in paragraph.getiterator():
            if node.text:
                paragraphs.append(node.text)
            
    return ''.join(paragraphs).strip()


if __name__ == '__main__':
    import sys
    result = get_docx_text(sys.argv[1])
    print(result)