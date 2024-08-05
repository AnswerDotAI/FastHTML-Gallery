from fasthtml.common import *
import os
import asyncio
import uvicorn
from uvicorn.config import Config
from uvicorn.server import Server
import configparser

links = [
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    HighlightJS(langs=['python', 'javascript', 'html', 'css']),
]
app, rt = fast_app(hdrs=links)

@rt("/")
def get():
    from pathlib import Path
    dir_paths = Path('examples/').glob('*')
    return Div(
        H1("FastHTML Gallery"),
        Div(*[image_card(i) for i in dir_paths],
            cls="row", 
        ),
        cls="container",
    )

def image_card(dir_path):
    import configparser
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    
    return Div(
        A(
            Card(
                Div(
                    Img(src=dir_path/'img.png', alt=metadata['REQUIRED']['ImageAltText'], cls="card-img-top"),
                    style="height: 200px; overflow: hidden;"
                ),
                Div(
                    H3(metadata['REQUIRED']['ComponentName'][1:-1], cls="card-title"),
                    P(metadata['REQUIRED']['ComponentDescription'][1:-1], cls="card-text"),
                    cls="card-body",
                    style="height: 150px; overflow: auto;"
                ),
                style="height: 350px;"
            ),
            href=f"/{dir_path.name}",
            cls="card-link"
        ),
        cls="col-xs-12 col-sm-6 col-md-4",
        style="margin-bottom: 20px;"
    )
@rt('/{dir_name}')
def get(dir_name: str):
    dir_path = Path(f'examples/{dir_name}')

    
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')

    code_content = (dir_path/'app.py').read_text()
   
    return Div(
        Div(
            A(
                "Back to Gallery",
                href="/",
                cls="btn btn-primary",
                style="margin-bottom: 20px;"
            ),
            H1(metadata['REQUIRED']['ComponentName'][1:-1]),
            cls="d-flex align-items-center justify-content-between"
        ),
        Div(
            Div(
                H2("Source Code"),
                Pre(Code(code_content)),
                cls="col-xs-12 col-md-6 px-1"
            ),
            Div(
                H2("Live Demo"),
                Iframe(src=f"/run/{dir_name}", width="100%", height="1200px"),
                cls="col-xs-12 col-md-6 px-1"
            ),
            cls="row mx-n1"
        ),
        cls="container-fluid"
    )

running_servers = {}
@rt('/run/{dir_name}')
async def get(dir_name: Path):
    if dir_name in running_servers:
        return Iframe(src=running_servers[dir_name], width="100%", height="1200px")

    try:
        # Configure uvicorn with port 0 for auto-selection
        config = Config(f"examples.{dir_name}.app:app", port=0, log_level="info") 
        server = Server(config=config)

        # Start the server in a separate task
        server_task = asyncio.create_task(server.serve())

        # Wait for the server to start and get the port
        while not server.started:
            await asyncio.sleep(0.1)

        for srv in server.servers:
            for socket in srv.sockets:
                _, port = socket.getsockname()
                break
            break

        running_servers[dir_name] = f"http://localhost:{port}"
        # Return the iframe with the correct port
        return Iframe(src=running_servers[dir_name], width="100%", height="1200px")

    except Exception as e:
        import traceback
        error_message = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        return HTMLResponse(error_message, status_code=500)
    



serve()
