from base64 import b64encode
from fasthtml.common import *

app, rt = fast_app()

@rt
def index():
    inp = Card(
        H3("Drag and drop images here"),
        # HTMX for uploading multiple images
        Input(
        type="file",
        name="images",
        multiple=True,
        required=True,
        accept="image/*",
        hx_post="/upload",
        hx_target="#image-list",
        hx_swap="afterbegin",
        hx_trigger="change",
        hx_encoding="multipart/form-data",
    ), 
    # Format upload box with white border so its clear where to drop the images
    style="text-align: center; border: 2px solid #ccc; border-radius: 8px;",
    )
    # Custom CSS to put images in a responsive grid
    image_list = Div(
        id="image-list",
        style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; padding: 20px;"
    )
    return Title("Multi Image Upload"), Div(
        H1("Multi Image Upload"), 
        inp, 
        H3("👇 Uploaded images 👇", style="text-align: center;"),
        image_list, 
    )

@rt
async def upload(request: Request):
    form = await request.form()
    images = form.getlist("images")
    image_elements = []
    for image in images:
        # Convert the image to base64 for image display
        contents = await image.read()
        img_data = f"data:{image.content_type};base64,{b64encode(contents).decode()}"
        # Card styling for a single image
        card = Div(
            Card(
                H4(image.filename),
                Img(
                    src=img_data,
                    alt=image.filename,
                    style="width: 100%; height: 200px; object-fit: cover; margin: 0;",
                ),
                style="height: 100%; text-align: center;",
            )
        )
        image_elements.append(card)
    return image_elements

serve()
