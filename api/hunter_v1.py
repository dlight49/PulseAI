import os
import sys
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Ensure project root in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

import hunter.researcher as researcher
import hunter.pitch_generator as pitch_gen

# Load config
load_dotenv(dotenv_path=os.path.join(project_root, "config", ".env"))

app = FastAPI(title="Pulse AI Hunter API")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HunterRequest(BaseModel):
    niche: str
    location: str

@app.post("/hunter/find")
async def find_leads(req: HunterRequest):
    """
    Triggers 'The Hunter' to find prospects in a specific niche and location.
    """
    prospects = researcher.find_prospects(req.niche, req.location)
    if not prospects:
        return {"status": "no_results", "leads": []}
    
    return {"status": "success", "leads": prospects}

@app.post("/hunter/generate-pitch")
async def generate_pitch(prospect: dict):
    """
    Generates a high-conversion sales pitch for a specific prospect.
    """
    try:
        pitch = pitch_gen.generate_pitch(prospect)
        return {"status": "success", "pitch": pitch}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
