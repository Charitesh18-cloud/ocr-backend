from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import pytesseract
import io
from pdf2image import convert_from_bytes
import requests
import time
import os  # ⬅️ For environment variables

app = FastAPI(title="OCR + DeepTranslate API")

# ---------- CORS Setup ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- OCR Endpoint ----------
@app.post("/ocr")
async def ocr(file: UploadFile, language: str = Form("eng")):
    try:
        content = await file.read()

        if file.filename.lower().endswith(".pdf"):
            images = convert_from_bytes(content, dpi=300)
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img, lang=language) + "\n"
        else:
            image = Image.open(io.BytesIO(content))
            text = pytesseract.image_to_string(image, lang=language)

        if not text.strip():
            raise HTTPException(status_code=204, detail="No text found")

        return {"text": text.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


# ---------- Translation Endpoint ----------
class TranslateRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

class TranslateResponse(BaseModel):
    translated_text: str
    modelUsed: str
    processing_time: float

def deep_translate(text, source_lang, target_lang):
    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang
    }
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),  # ⬅️ Key is now hidden!
        "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()["data"]["translations"]["translatedText"]
        return result[0] if isinstance(result, list) else result
    else:
        raise Exception(f"Translation API error: {response.text}")

@app.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    try:
        start = time.time()
        result = deep_translate(request.text, request.source_language, request.target_language)
        return TranslateResponse(
            translated_text=result,
            modelUsed="Deep Translate API",
            processing_time=round(time.time() - start, 3)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- Run ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
