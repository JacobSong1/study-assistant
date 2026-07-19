from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv
import json
import pypdf
import io

load_dotenv() #loads and opens .env file

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
#returns the value of GOOGLE_API_KEY and logs into Gemini
#password not exposed since its its env file
app = FastAPI() #creates the server (app). 

# Specific domains allowed to access this backend
origins = [
    "https://studywithshin.vercel.app",
    "http://localhost:3000",
]

app.add_middleware( #.add_middleware - add a security rule to server
    CORSMiddleware, # the type of specific security rule
    allow_origins=origins, # allows access explicitly from your Vercel site and localhost
    allow_credentials=True,
    allow_methods=["*"], #which requests allowed(GET,POST,DELETE,PUT). * means everything allowed
    allow_headers=["*"], #allow all kind of extra info to attach to request
)

class NotesInput(BaseModel): # In class, NotesInput inherits everything from BaseModel (which autovalidates incoming data, checks if data is String or no)
    notes: str # notes field of string type
#when someone hits /generate, FastAPI expect JSON with a notes field that's a string

@app.post("/generate") # @ registers the function generate_flashcards to the FastAPI server instance (app)
# when React sends a POST request to /generate, generate_flashcards is run
async def generate_flashcards(input: NotesInput): #represents the prompt sent to gemini
    prompt = f"""Turn these notes into 5 flashcards.
Return JSON only, no other text, no markdown.
Format: {{"flashcards": [{{"question": "...", "answer": "..."}}]}}

Notes: {input.notes}"""
#"""" represents start and end of multi-line f string. {{ represents printing literal { in f string.
#{} means dictionary, [] means array list. Needed cus we wanna return JSON format
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )
    return json.loads(response.text)
#Take Gemini reply and json.loads turn JSON String into dict to send to React

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read() #takes awhile to read the raw bytes of the pdf file
    pdf = pypdf.PdfReader(io.BytesIO(contents)) #since pypdf unable to read raw bytes, we wrap the bytes into a file object to allow pypdf to read the new file
    text = ""
    for page in pdf.pages: # for every page in the pdf, we extract the text and add it to one big String until 3000 characters hit
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