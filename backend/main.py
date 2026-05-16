from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv
import json
import pypdf
import io

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class NotesInput(BaseModel):
    notes: str

@app.post("/generate")
async def generate_flashcards(input: NotesInput):
    prompt = f"""Turn these notes into 5 flashcards.
Return JSON only, no other text, no markdown.
Format: {{"flashcards": [{{"question": "...", "answer": "..."}}]}}

Notes: {input.notes}"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
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
Return JSON only, no other text, no markdown.
Format: {{"flashcards": [{{"question": "...", "answer": "..."}}]}}

Notes: {text[:3000]}"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )
    return json.loads(response.text)