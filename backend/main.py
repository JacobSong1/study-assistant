from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types  # Imported for Structured JSON configuration
import os
from dotenv import load_dotenv
import json
import pypdf
import io

load_dotenv() # loads and opens .env file

# 1. FIX: Grab the key and strictly strip out trailing or hidden whitespace/newlines
raw_api_key = os.getenv("GOOGLE_API_KEY")
clean_api_key = raw_api_key.strip() if raw_api_key else None

client = genai.Client(api_key=clean_api_key)
app = FastAPI() 

# Specific domains allowed to access this backend
origins = [
    "https://studywithshin.vercel.app",
    "http://localhost:3000",
]

app.add_middleware( 
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

class NotesInput(BaseModel): 
    notes: str 

@app.post("/generate") 
async def generate_flashcards(input: NotesInput): 
    prompt = f"""Turn these notes into 5 flashcards.
Format: {{"flashcards": [{{"question": "...", "answer": "..."}}]}}

Notes: {input.notes}"""

    # 2. FIX: Force the native Gemini SDK to return clean, valid JSON structures
    response = client.models.generate_content(
        model="gemini-1.5-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read() 
    pdf = pypdf.PdfReader(io.BytesIO(contents)) 
    text = ""
    for page in pdf.pages: 
        text += page.extract_text()

    prompt = f"""Turn these notes into 5 flashcards.
Format: {{"flashcards": [{{"question": "...", "answer": "..."}}]}}

Notes: {text[:3000]}"""

    # 2. FIX: Apply clean structured configuration to the PDF endpoint as well
    response = client.models.generate_content(
        model="gemini-1.5-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)