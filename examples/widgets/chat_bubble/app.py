from fasthtml.common import *

app, rt = fast_app()

@rt('/')
def homepage():
    return Div(*[create_chat_message(**msg, msg_num=i) for i, msg in enumerate(example_messages)])

def create_chat_message(role, content, msg_num):
    text_color = '#1F2937'
    match role:
        case 'system': color = '#8B5CF6'
        case 'user': color = "#F000B8"
        case _: color = "#37CDBE"

    # msg 0 = left, msg 1 = right, msg 2 = left, etc.
    alignment = 'flex-end' if msg_num % 2 == 1 else 'flex-start'

    message = Div(Div(
            Div(# Shows the Role
                Strong(role.capitalize()),
                style=f"color: {text_color}; font-size: 0.9em; letter-spacing: 0.05em;"),
            Div(# Shows content and applies font color to stuff other than syntax highlighting
                Style(f".marked *:not(code):not([class^='hljs']) {{ color: {text_color} !important; }}"),
                Div(content),
                style=f"margin-top: 0.5em; color: {text_color} !important;"),
            # extra styling to make things look better
            style=f"""
                margin-bottom: 1em; padding: 1em; border-radius: 24px; background-color: {color};
                max-width: 70%; position: relative; color: {text_color} !important; """),
        style=f"display: flex; justify-content: {alignment};")

    return message

example_messages = [
        {
            "role": "system",
            "content": "Hello, world!  I am a chatbot that can answer questions about the world.",
        },
        {
            "role": "user",
            "content": "I have always wondered why the sky is blue.  Can you tell me?",
        },
        {
            "role": "assistant",
            "content": "The sky is blue because of the atmosphere.  As white light passes through air molecules cause it to scatter.  Because of the wavelengths, blue light is scattered the most.",
        },
        {
            "role": "user",
            "content": "What is the meaning of life?",
        },
        {
            "role": "assistant",
            "content": "42 is the meaning of life.  It is the answer to the question of life, the universe, and everything.",
        }
    ]

serve()