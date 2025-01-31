from fasthtml.common import APIRouter, uvicorn, FastHTMLWithLiveReload
# add Routers https://docs.fastht.ml/ref/handlers.html#apirouter
# Markdown support https://docs.fastht.ml/tutorials/quickstart_for_web_devs.html#rendering-markdown
# Markdown support for daisy ui chat https://isaac-flath.github.io/website/posts/boots/FasthtmlTutorial.html

from fasthtml.common import Div, Span, Body, P, Form, Input, Button, Script, Link, Label, Nav, Title, Template, Style, serve
import json
from fasthtml.components import Zero_md
from functools import partial
import uuid

# llamaindex imports (!pip install llama_index)
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent


# =============== Router ===============
# in this example we will use the APIRouter to create a chat application and then mount it to the main app

r_chat = APIRouter()

# Init global variables for OpenAI agent
agent = None
api_key_set = False # flag to check if API key is set

# global user data storage
user_data = {}

# Markdown Rendering
def render_md(md):
    def render_local_md(md, css=''):
        css_template = Template(Style(css), data_append=True)
        return Zero_md(css_template, Script(md, type="text/markdown"))

    # handling css styles
    css = '.markdown-body {background-color: unset !important; color: unset !important;}'
    _render_local_md = partial(render_local_md, css=css)
    return _render_local_md(md)


# Chat  bubble with markdown
def ChatMessageMd(msg_idx:int, msg:str, **kwargs):    
    assert msg_idx is not None, "Message index is missing"    
    Msg = msg
    role = Msg.role.value
    content = Msg.content or ""

    # print(f" <<<<< Got new chat message role: {role}, content: {content}")

    is_user = role == 'user'

    # If user message return chat bubble
    if is_user:
        return Div(Div(content,

                       # Target if updating the content
                       id=f"chat-content-{msg_idx}",
                       cls="chat-bubble chat-bubble-neutral"
                       ),

                   # Target if replacing the whole message
                   id=f"chat-message-{msg_idx}",
                   cls="chat chat-end", **kwargs)

    # return answer in div with markdown
    msg_md = render_md(content)
    return Div(Div(msg_md,

                   # Target if updating the content
                   id=f"chat-content-{msg_idx}",
                   ),

               # Target if replacing the whole message
               id=f"chat-message-{msg_idx}",
               cls='container bg-base-100 rounded-md shadow-md p-6 w-full mx-auto', **kwargs)


# Span with markdown
def SpanMd(msg, **kwargs):
    return Span(render_md(msg), **kwargs)


# On socket disconnect clear user chat data
async def on_disconnect(send, session):
    session_id = session.get('session_id', "no-session-id" )
    user_data.pop(session_id, None) # clear user data    

#  Socket connection
@r_chat.ws('/wscon',  disconn = on_disconnect)
async def ws(data, send,  session):
    
    if not api_key_set:
        print(">>>> OpenAI API key is not set ! ")
        await send(Div(" - OpenAI API Key is not set! Setup your OpenAI API Key to chat", cls="text-error", hx_swap_oob='innerHTML', id="notification"))
        return

    if not data:
        print(">>>> No data received by socket ! ")
        await send(Div(" - No data received by socket !", cls="text-error", hx_swap_oob='innerHTML', id="notification"))
        return

    # get user message      
    msg = data['msg']   

    if not msg:        
        data_str = json.dumps(data)
        print(" >>>> Cannot get message from received data ", data_str)
        await send(Div(P(" Websocket Data Error: No message could be constructed from received socket data"),
                       P(data_str), cls="text-error"), hx_swap_oob='innerHTML', id="notification")
        return

    # check-out user messages
    session_id = session['session_id']
    data_messages = user_data.setdefault(session_id, [])    
       
    # add user message to messages list
    UserMessage = ChatMessage(role=MessageRole.USER, content=msg )
    data_messages.append(UserMessage)
    user_msg_idx = len(data_messages)-1
    
    # Send the user message to the user (updates the UI right away)
    await send(Div(ChatMessageMd(user_msg_idx, msg=UserMessage), hx_swap_oob='beforeend', id="chatlist"))

    # Send the clear input field command to the user
    await send(ChatInput())

    # Start loader
    await send(Div(Loader(), hx_swap_oob='innerHTML', id="loader"))

    # Model response (streaming)
    response_stream = await agent.astream_chat(message=msg, chat_history=data_messages)

    # clear loader message
    await send(Div("", hx_swap_oob='innerHTML', id="loader"))

    # Send an empty message with the assistant response
    new_message = ''
    ReplyMessage = ChatMessage(role=MessageRole.ASSISTANT, content=new_message)
    data_messages.append(ReplyMessage)
    reply_msg_idx = len(data_messages)-1    
    
    await send(Div(ChatMessageMd(reply_msg_idx, ReplyMessage), hx_swap_oob='beforeend', id="chatlist"))

    # process async streaming 
    line_buffer = ""
    async for response in response_stream.async_response_gen():
        chunk_message = response
        print(chunk_message, end='', flush=True) # print message to console, remove for production
        
        # keep message and line buffer
        new_message += chunk_message
        line_buffer += chunk_message
        
        # send complete lines with markdown
        lines = line_buffer.split("\n")  # split buffer into lines
        line_buffer = lines.pop()  # keep last line in buffer
        if lines:
            new_lines = "\n".join(lines)
            await send(SpanMd(new_lines, hx_swap_oob="beforeend", id=f"chat-content-{reply_msg_idx}"))

    # send final chunk
    await send(SpanMd(line_buffer, hx_swap_oob="beforeend", id=f"chat-content-{reply_msg_idx}"))

    # replace last message with final message
    final_msg = ChatMessage(role=MessageRole.ASSISTANT, content=new_message)
    data_messages[reply_msg_idx] = final_msg   

    # replace entire message with markdown
    msg_md = render_md(new_message)
    await send(Div(msg_md,  hx_swap_oob='innerHTML', id=f"chat-content-{reply_msg_idx}"))
    
    # check-in user messages to global store
    user_data[session_id] = data_messages


def entry_form(apikey:str=""):
    return Div(
        P("This demo requires Open AI API key to run. Enter your API key here "),
        Form(
            Div(
                Label(
                    Span('Open AI API Key', cls='label-text font-semibold'),
                    cls='label'
                ),

                Input(type='text', id='apikey', name='apikey', value=apikey, placeholder='Open AI API Key',
                      required=True, cls='input input-bordered w-full',
                      oninvalid="this.setCustomValidity('Open AI API Key is required')",
                      oninput="this.setCustomValidity('')"),

                cls='form-control w-full tooltip tooltip-bottom',
                data_tip='To get API Key vist https://platform.openai.com/',
            ),


            Button('Setup Key for session', type='submit', cls='btn btn-primary'),
            cls='w-full mt-2  flex items-end space-x-4',
            
            method='post',
           
            # Bind form to route via HTMX (yeah baby!)
            hx_post="/set_api_key", 
            hx_target="#notification", # target div for response
            hx_swap="innerHTML", # how target content shoudl be replaced (crazy stuff!)           


        ),
        cls='container bg-base-100 rounded-md shadow-md p-6 w-full space-y-4',
    )


def ChatInput():
    return Input(type='text', name='msg', id='msg-input', placeholder='Ask a follow up question...',
                 cls='input input-bordered w-full',
                 hx_swap_oob='true'),


def FollowUpForm():
    return Form(
        # User Input Message
        ChatInput(),

        Button('Send', type='submit', cls='btn btn-primary'),

        cls='w-full mt-2 flex items-end space-x-4',

        # send data to websocket
        ws_send=True,
    )

# Loader message
def Loader():
    return Div(
        Span(cls='loading loading-dots text-primary'),
        Span('Im doing the research and preparing your report, this may take a minute',
             cls='text-primary'),

        cls='flex items-center space-x-3 mx-4 bg-base-200'
    )

@r_chat.post("/set_api_key")
async def set_api_key(apikey: str):
    global agent, api_key_set
    agent = OpenAIAgent.from_tools(llm=OpenAI(model="gpt-4o", api_key=apikey))
    
    hello = ""
    
    try:
       hello = agent.query("You are witty and cheerful assitant, say hello") 
       print(f"Hello from OpenAI: {hello}")    
           
    except Exception as e:
        print(f"Error setting OpenAI API Key: {e}")
        return f"Error setting OpenAI API Key: {e}"
    
    api_key_set = True
    print(f"API Key set successfully")
    return f"API key set successfully.  {hello}"

# Chat page
@r_chat("/", name="chat")
def get(session):  # noqa: F811
    
    # check session id
    session_id = session.setdefault('session_id', str(uuid.uuid4()))
    messages = user_data.get(session_id, []) 
    
    return Title("Streaming OpenAI Chat with Llamaindex"), Body(

        # Navbar
        Nav(
            Div(
                Div('Async Streaming Chat with Llamaindex OpenAI Agent',
                    cls='btn btn-ghost normal-case text-xl'),
                cls='navbar-start'
            ),

            cls='navbar z-510 bg-base-100 shadow-md border-none'
        ),
        

                
        # Chat Message Section
        Div(

            # entry form
            Div(

                entry_form(),

                cls='container mx-auto w-full p-4',
                id='entryform',

                # connect div with form to websocket
                hx_ext="ws", ws_connect="/wscon"
            ),
            
        # Notification
        Div(
        Div(P("Welcome to OpenAI Agent chat with LllamaIndex RAG. Enter your OpenAI API Key to start chatting. To get API Key vist https://platform.openai.com/",
              cls='mx-3'),
            id='notification',
            cls='alert alert-info mx-auto w-full p-4 ',
        ), cls='container  mx-auto w-full px-4'),
            
           # Chat messages
            Div(
                # Chat messages
                *[ChatMessageMd(msg_idx, msg)
                  for msg_idx, msg in enumerate(messages)],
                
                id='chatlist',
                cls='flex-1 p-4 space-y-3 h-full'
            ),
            cls='container flex flex-1 flex-col h-full w-full mx-auto overflow-y-auto'
        ),

        # loader
        Div(id='loader',  cls='container mx-auto w-full p-4'),

        # Follow up input area
        Div(

            # Follow up chat form
            FollowUpForm(),

            id='followup',
            cls=' container p-4 px-7 w-full mx-auto',

            # connect div to websocket
            hx_ext="ws", ws_connect="/wscon"
        ),

        cls='h-screen w-full flex flex-col bg-base-200 pt-1 ',
    )


# =============== App =================
# Now we will create the app and mount the router to it


headers = (
    Script(src="https://cdn.tailwindcss.com"),
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.12.23/dist/full.min.css"),
    Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register") # zero-md for markdown rendering
)
# Set up the app, including daisyui and tailwind for the chat component
app = FastHTMLWithLiveReload(hdrs=headers, exts='ws', debug=True, htmlkw=dict(
    lang="en", data_theme="corporate"))

# Add the router to the
r_chat.to_app(app)


# Run the app
if __name__ == "__main__":  


    # start uvicorn server for app
    serve(reload=True)
