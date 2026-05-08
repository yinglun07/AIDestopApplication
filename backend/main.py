from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import json

from router import route_query
from agents.transcription_agent import TranscriptionAgent
from agents.vision_agent import VisionAgent
from agents.generation_agent import GenerationAgent
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transcription_agent = TranscriptionAgent()
vision_agent = VisionAgent()
generation_agent = GenerationAgent()


def save_history(query, result):
    entry = {
        "query": query,
        "result": result
    }

    try:
        with open("history.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open("history.json", "w") as f:
        json.dump(data, f, indent=2)


@app.post("/upload/")
async def upload_video(file: UploadFile = File(...), query: str = "transcribe"):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    route = route_query(query)

    if route == "transcription":
        result = transcription_agent.run(file_path)

    elif route == "vision":
        result = vision_agent.analyze(file_path)

    elif route == "generation":
        result = generation_agent.create_report()

    elif route == "clarification":
        return {
            "route": "clarification",
            "message": "Your request is unclear. What would you like to do with the video?",
            "suggestions": [
                "Transcribe the video",
                "Detect objects in the video",
                "Summarize the video"
            ]
    }

    else:
        result = "Unknown task"

    if result is None:
        result = "No output generated"

    save_history(query, result)

    return {
        "route": route,
        "result": result
    }
    
@app.get("/download/{filename}")
def download_file(filename: str):
    return FileResponse(filename, media_type="application/pdf")