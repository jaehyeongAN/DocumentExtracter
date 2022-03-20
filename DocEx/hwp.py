import os
import re
import olefile
import zlib
import struct


def get_hwp_text(filename):

    # Option 1. HWP -> Text
    # converted_file_path = filename.split('.hwp')[0]+'.txt'
    # hwp2txt_cmd = f"hwp5txt {filename} > {converted_file_path}"
    # os.system(hwp2txt_cmd)

    # Option 2. HWP -> HTML -> parsing text
    converted_file_path = filename.split('.hwp')[0]+'.html'
    hwp2html_cmd = f"hwp5html {filename} --html --output {converted_file_path}"
    os.system(hwp2html_cmd) # convert .hwp to .txt and save file

    # load converted file
    with open(converted_file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        html = html.replace('<p class="Normal parashape-13"></p>','\n').replace('<p class="Normal parashape-13">','').replace('</p>','\n').replace('&#13;','')

    # strip html
    text = re.sub('<[^>]*>', '', html)
    # strip css
    css_list = [i for i in re.finditer(';\n}',text)]
    text = text[css_list[-1].end():]
    
    text = text.replace('&lt;','<').replace('&gt;','>')
    text = text.strip()

    # remove converted file
    if converted_file_path:
        os.remove(converted_file_path)



    # f = olefile.OleFileIO(filename)
    # dirs = f.listdir()

    # # HWP 파일 검증
    # if ["FileHeader"] not in dirs or \
    #    ["\x05HwpSummaryInformation"] not in dirs:
    #     raise Exception("Not Valid HWP.")

    # # 문서 포맷 압축 여부 확인
    # header = f.openstream("FileHeader")
    # header_data = header.read()
    # is_compressed = (header_data[36] & 1) == 1

    # # Body Sections 불러오기
    # nums = []
    # for d in dirs:
    #     if d[0] == "BodyText":
    #         nums.append(int(d[1][len("Section"):]))
    # sections = ["BodyText/Section"+str(x) for x in sorted(nums)]

    # # 전체 text 추출
    # text = ""
    # for section in sections:
    #     bodytext = f.openstream(section)
    #     data = bodytext.read()
    #     if is_compressed:
    #         unpacked_data = zlib.decompress(data, -15)
    #     else:
    #         unpacked_data = data
    
    #     # 각 Section 내 text 추출    
    #     section_text = ""
    #     i = 0
    #     size = len(unpacked_data)
    #     while i < size:
    #         header = struct.unpack_from("<I", unpacked_data, i)[0]
    #         rec_type = header & 0x3ff
    #         rec_len = (header >> 20) & 0xfff

    #         if rec_type in [67]:
    #             rec_data = unpacked_data[i+4:i+4+rec_len]
    #             section_text += rec_data.decode('utf-16')
    #             section_text += "\n"

    #         i += 4 + rec_len

    #     text += section_text
    #     text += "\n"

    #     # remove junk
    #     text = re.sub('[╨|╦]','',text)
    #     text = re.sub('[^0-9a-zA-Z가-힣][ȃ|Ā| ྠĀ]','',text)
    #     text = re.sub(u'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff\u3300-\u33ff\ufe30-\ufe4f\uf900-\ufaff]','', text) # remove 한자
    #     text = re.sub(r'[\x02|\x15]',r'',text)
    #     text = re.sub(r'\x0b','\n',text)

    
    return text


if __name__ == '__main__':
    import sys
    result = get_hwp_text(sys.argv[1])
    print(result)