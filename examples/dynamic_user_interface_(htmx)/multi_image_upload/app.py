from base64 import b64encode
from fasthtml.common import *

app, rt = fast_app()

@rt
def index():
    inp = Card(
        H3("Drag and drop images here", style="text-align: center;"),
        # HTMX for uploading multiple images
        Input(type="file",name="images", multiple=True, required=True, 
              # Call the upload route on change
              post=upload, hx_target="#image-list", hx_swap="afterbegin", hx_trigger="change",
              # encoding for multipart
              hx_encoding="multipart/form-data",accept="image/*"),
        # Make a nice border to show the drop zone
        style="border: 2px solid #ccc; border-radius: 8px;",)

    return Titled("Multi Image Upload", 
        inp, 
        H3("👇 Uploaded images 👇", style="text-align: center;"),
        Div(id="image-list"))


async def ImageCard(image):
    contents = await image.read()
    # Create a base64 string
    img_data = f"data:{image.content_type};base64,{b64encode(contents).decode()}"
    # Create a card with the image
    return Card(H4(image.filename), Img(src=img_data, alt=image.filename))

@rt
async def upload(images: list[UploadFile]):
    # Create a grid filled with 1 image card per image
    return Grid(*[await ImageCard(image) for image in images])

serve()
