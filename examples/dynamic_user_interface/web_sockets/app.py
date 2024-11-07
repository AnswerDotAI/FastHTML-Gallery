from fasthtml.common import *
from collections import deque

app, rt = fast_app(exts='ws')

# All messages here, but only most recent 15 are stored
messages = deque(maxlen=15)
users = {}

# Takes all the messages and renders them
box_style = "border: 1px solid #ccc; border-radius: 10px; padding: 10px; margin: 5px 0;"
def render_messages(messages):
    return Div(*[Div(m, style=box_style) for m in messages], id='msg-list')

# Input field is reset via hx_swap_oob after submitting a message
def mk_input(): return Input(id='msg', placeholder="Type your message", value="", hx_swap_oob="true")

@rt
def index():
    return Titled("Leave a message for others!"),Div(
        Form(mk_input(), ws_send=True), # input field
        P("Leave a message for others!"),
        Div(render_messages(messages),id='msg-list'), # All the Messages
        hx_ext='ws', ws_connect='ws') # Use a web socket 

def on_connect(ws, send): users[id(ws)] = send
def on_disconnect(ws):users.pop(id(ws),None)

@app.ws('/ws', conn=on_connect, disconn=on_disconnect)
async def ws(msg:str,send):
    await send(mk_input()) # reset the input field immediately
    messages.appendleft(msg) # New messages first
    for u in users.values(): # Get `send` function for a user
        await u(render_messages(messages)) # Send the message to that user

serve()
