from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()


@app.get("/")
async def serve_ui():
    return FileResponse(os.path.join('ui', 'index.html'))

# Для обслуживания статических файлов, таких как CSS и JS


@app.get("/ui/{file_path:path}")
async def static_files(file_path: str):
    return FileResponse(os.path.join('ui', file_path))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
