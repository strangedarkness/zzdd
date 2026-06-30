from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

from database import (
    init_database,
    get_all_albums,
    get_album_by_id,
    add_photo,
    get_photos_by_album
)

app = FastAPI()
init_database()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.get("/albums", response_class=HTMLResponse)
def albums(request: Request):
    albums = get_all_albums()

    return templates.TemplateResponse(
        request=request,
        name="albums.html",
        context={
            "albums": albums
        }
    )

@app.get("/albums/{album_id}", response_class=HTMLResponse)
def album_detail(request: Request, album_id: int):
    album = get_album_by_id(album_id)
    photos = get_photos_by_album(album_id)

    return templates.TemplateResponse(
        request=request,
        name="album.html",
        context={
            "album": album,
            "photos": photos
        }
    )

@app.post("/albums/{album_id}/upload")
def upload_photo(
    album_id: int,
    photo: UploadFile = File(...),
    title: str = Form(""),
    description: str = Form(""),
    taken_at: str = Form("")
):
    upload_dir = Path("uploads") / f"album_{album_id}"
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / photo.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    web_path = "/" + str(file_path).replace("\\", "/")

    add_photo(
        album_id=album_id,
        file_path=web_path,
        title=title,
        description=description,
        taken_at=taken_at
    )

    return RedirectResponse(
        url=f"/albums/{album_id}",
        status_code=303
    )