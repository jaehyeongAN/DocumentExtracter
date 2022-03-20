import os 
from datetime import datetime
import traceback
import logging
import logging.config
import ssl

import pdftotext

import uvicorn
from fastapi import FastAPI, BackgroundTasks, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from DocEx import pdf, hwp, docx, txt
import log_config


# Logger
logging.config.dictConfig(log_config.logger)
logger = logging.getLogger()

# app path
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
UPLOAD_DIR = os.path.join(APP_ROOT, '_tmp_uploadfiles')
if os.path.exists(UPLOAD_DIR):
    print(f"{UPLOAD_DIR} -- Folder already exists \n")
else:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    print(f"{UPLOAD_DIR} -- Folder create complete \n")


## FastAPI & CORS (Cross-Origin Resource Sharing)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/health')
async def health_check():
    s = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    out = 'INFO: ' + s + ' bb8-assist/DocumentExtracter is listening'

    return JSONResponse({'status':out})


@app.post('/pdf-extract')
async def document_extract(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        file_save_path = os.path.join(UPLOAD_DIR, f"file.{file.filename.split('.')[-1]}")
        with open(file_save_path, "wb") as fp:
            fp.write(file_content)

        # extract text
        text = pdf.get_pdf_text(file_save_path, backend='tika')
        os.remove(file_save_path) # remove file

    except Exception as e:
        logger.error(f"{traceback.format_exc()}")
        text = ''

    return JSONResponse({'text':text})


@app.post('/docx-extract')
async def document_extract(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        file_save_path = os.path.join(UPLOAD_DIR, f"file.{file.filename.split('.')[-1]}")
        with open(file_save_path, "wb") as fp:
            fp.write(file_content)

        # extract text
        text = docx.get_docx_text(file_save_path)
        os.remove(file_save_path) # remove file

    except Exception as e:
        logger.error(f"{traceback.format_exc()}")
        text = ''

    return JSONResponse({'text':text})


@app.post('/hwp-extract')
async def document_extract(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        file_save_path = os.path.join(UPLOAD_DIR, f"file.{file.filename.split('.')[-1]}")
        with open(file_save_path, "wb") as fp:
            fp.write(file_content)

        # extract text
        text = hwp.get_hwp_text(file_save_path)
        os.remove(file_save_path) # remove file

    except Exception as e:
        logger.error(f"{traceback.format_exc()}")
        text = ''

    return JSONResponse({'text':text})


@app.post('/txt-extract')
async def document_extract(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        file_save_path = os.path.join(UPLOAD_DIR, f"file.{file.filename.split('.')[-1]}")
        with open(file_save_path, "wb") as fp:
            fp.write(file_content)

        # extract text
        text = txt.get_txt_text(file_save_path)
        os.remove(file_save_path) # remove file

    except Exception as e:
        logger.error(f"{traceback.format_exc()}")
        text = ''

    return JSONResponse({'text':text})



# if __name__ == "__main__":
#     uvicorn.run('app.main:app', host='0.0.0.0', port=443, ssl_keyfile='./key.pem', ssl_certfile='./cert.pem')
