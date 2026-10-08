import os
import modal

# Define the Modal Image and install all required python dependencies
image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install_from_requirements("requirements.txt")
)

app = modal.App("livecode-ai", image=image)

@app.function(
    secrets=[
        modal.Secret.from_name("livecode-secrets")
    ],
    mounts=[
        # Mount the backend source code
        modal.Mount.from_local_dir("./backend", remote_path="/root/backend"),
        # Mount the React compiled build assets if they exist
        modal.Mount.from_local_dir("./frontend/dist", remote_path="/root/frontend/dist", condition=lambda p: os.path.exists("./frontend/dist"))
    ]
)
@modal.asgi_app()
def fastapi_app():
    # Lazy import to ensure environment variables and mounts are active inside the container
    from backend.main import app as web_app
    return web_app
