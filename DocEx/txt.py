def get_txt_text(file_path):
    '''
    Extract text from .txt
    '''
    with open(file_path, mode='r', encoding='utf-8') as f:
        text = f.read()

    return text