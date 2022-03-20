# DocumentExtracter

## Functions
- Extract text from .pdf, .docx, .hwp, .txt format (but, the text extraction is not perfect.)
- REST API

## Install
```bash
pip install -r requirements.txt
```
#### If you want use the <code>tika</code>, please install jdk. (<code>tika</code> usually works better.)
- To use this library, you need to have Java 7+ installed on your system
- Refer to [https://github.com/chrismattmann/tika-python](https://github.com/chrismattmann/tika-python)
```
# Install OpenJDK
## 1. In MacOS
brew install cask
brew install --cask adoptopenjdk8 # or adoptopenjdk11

## 2. In Linux
apt-get -y install --no-install-recommends default-jdk-headless
```

## Usages
### 1. Only Use TextExtaction
```python
from DocEx import pdf, hwp, docx, txt

# Extract text from PDF
extracted_text = pdf.get_pdf_text(file_save_path, backend='tika') # backend options: ['tika', 'pdfminer']

# Extract text from DOCX
extracted_text = docx.get_docx_text(file_save_path)

# Extract text from HWP
extracted_text = hwp.get_hwp_text(file_save_path)

# Extract text from TXT
extracted_text = txt.get_txt_text(file_save_path)
```

### 2. Run as REST API (by FastAPI)
```bash
# In local
uvicorn main:app --port 8001

# If you want to run with external IP and background running
nohup uvicorn main:app --host 0.0.0.0 --port 8001 --ssl-keyfile ./key.pem --ssl-certfile ./cert.pem &
```