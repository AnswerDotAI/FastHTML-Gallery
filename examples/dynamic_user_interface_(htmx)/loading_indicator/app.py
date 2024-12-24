from fasthtml.common import *
from monsterui.all import *
import asyncio

app, rt = fast_app(hdrs=Theme.blue.headers())

@rt
def index(): 
    return Titled("Loading Demo",
        # Button to trigger an HTMX request
        Button("Load", id='load', 
               # Trigger HTMX request to add content to #content
               get=load, hx_target='#content', hx_swap='beforeend',
               # While request in flight, show loading indicator
               hx_indicator='#loading'), 
        # A place to put content from request
        Div(id='content'), 
        # Loading indicator ready for htmx use
        # For more options see https://monsterui.answer.ai/api_ref/docs_loading
        Loading(id='loading', htmx_indicator=True)) 

@rt
async def load(): 
    # Sleep for a second to simulate a long request
    await asyncio.sleep(1)
    return P("Loading Demo")

serve()
