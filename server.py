import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Response, Request, UploadFile, File
from fastapi.responses import FileResponse

from hypercorn.config import Config
from hypercorn.asyncio import serve

from services.showcaseGenius import generateIndex, revaluateIndex, generateDoc

import asyncio

base_dir = Path(__file__).resolve().parent
sys.path.append(str(base_dir))

app = FastAPI()

from services.logger import setup_logging, get_logger

setup_logging()
logger = get_logger()

@app.get("/hello")
def hello():
    return 'world'

# Showcase Genius routes
@app.get("/generateIndex")
async def generateIndex(q: str, slide_no: int):
    logger.debug("[GET] API Request on /generateIndexGenerating index for slide " + str(slide_no) + " with query " + q)
    if slide_no <= 0:
        raise HTTPException(status_code=400, detail="Slide number needs to be larger than 1.")
    elif slide_no > 8:
        raise HTTPException(status_code=400, detail="Slide number needs to be less than or equal to 8.")
    
    try:
        generatedIndex = generateIndex(q, slide_no)
        return Response(content={"index": generatedIndex, "query": q}, status_code=200)
    except Exception as e:
        logger.error("Error generating index: " + str(e))
        raise HTTPException(status_code=500, detail=f"Error generating index: {str(e)}")
    
@app.post("/revaluateIndex")
async def revaluateIndex(request: Request):
    logger.debug("[POST] API Request on /revaluateIndex for revaluating index")
    
    body = await request.json()
    q = body.get("query")
    slide_no = body.get("slide_no")
    index = body.get("index")

    if slide_no <= 0:
        raise HTTPException(status_code=400, detail="Slide number needs to be larger than 1.")
    elif slide_no > 8:
        raise HTTPException(status_code=400, detail="Slide number needs to be less than or equal to 8.")
    
    try:
        revaluatedIndex = revaluateIndex(q, slide_no, index)
        return Response(content={"index": revaluatedIndex, "query": q}, status_code=200)
    except Exception as e:
        logger.error("Error revaluating index: " + str(e))
        raise HTTPException(status_code=500, detail=f"Error revaluating index: {str(e)}")
    
@app.post("/generateDoc")
async def generateDoc(request: Request):
    body = await request.json()
    q = body.get("query")
    logger.debug(f"[POST] API Request on /generateDoc for generating document for query: {q}")

    slide_no = body.get("slide_no")
    index = body.get("index")
    
    try:
        generatedDoc = generateDoc(slide_no, index)
        return Response(content={"doc": generatedDoc}, status_code=200)
    except Exception as e:
        logger.error("Error generating document: " + str(e))
        raise HTTPException(status_code=500, detail=f"Error generating document: {str(e)}")
    

# Visulearn Routes
from services.visulearn import is_image, ocr, summarise_text, text_to_speech, get_length_of_audio, generate_images, final_video_production, get_title_from_text

@app.post("/gen-vid-from-image")
async def create_upload_file(file: UploadFile = File(...)):
    logger.debug("[POST] API Request on /gen-vid-from-image")
    if not is_image(file):
        raise HTTPException(status_code=400, detail="File is not a valid image")

    text = ocr(file.file)
    title = get_title_from_text(text)
    title = "nigga"
    summarised_text = summarise_text(text)
    audio_path = text_to_speech(summarised_text)

    # figuring out the number of images to produce based on the audio generated
    audio_duration = get_length_of_audio(audio_path)
    num_images = int(audio_duration / 10) + 1
    image_paths: list[str] = generate_images(text, num_images)

    logger.debug("Starting video production 🚀")
    video_path = final_video_production(image_paths, audio_path)

    if not video_path:
        raise HTTPException(status_code=500, detail="Error while creating video :(")
    return FileResponse(video_path, filename=title+".mp4")

async def main():
    config = Config()
    port = "5001"
    config.bind = [f"0.0.0.0:{port}"]
    logger.info("HTTP Server running on port " + os.environ.get('HTTP_PORT', "5001"));
    await serve(app, config)


if __name__ == '__main__':
    logger.info("Starting server...")
    logger.info("CURRENT ENVIRONMENT: " + os.environ.get('RUNTIME_ENV', "Development"))
    
    asyncio.run(main())