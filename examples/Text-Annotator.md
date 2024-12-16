# Text-Annotator

> An app built by Alex Volkov that demonstrates annotation use-cases and tailwind styling in FastHTML

# Text Annotation Web App

This project is a web-based tool for annotating LLM-generated text, built using FastHTML, HTMX, and Tailwind CSS, originally built by [Alex Volkov](https://x.com/altryne) in the [fasthtml-examples repo](https://github.com/AnswerDotAI/fasthtml-example/blob/main/annotate_text/main.py)

## Key Technologies and Techniques

1. **FastHTML**: A Python-based framework for building web applications with a focus on web fundamentals.
2. **HTMX**: Used to create dynamic server-side content updates that allow interaction with the app without page reloads.
3. **Tailwind CSS**: Tailwind classes are used throughout the HTML to style the app, providing a clean and responsive design.
4. **DaisyUI**: A Tailwind CSS component library used for additional styling.

## How It Works

### Server-Side Logic

The app uses FastHTML to define routes and handle annotation logic on the server. Key routes include:

- `/`: The main page that renders the initial annotation interface.
- `/{idx}`: Handles both GET and POST requests for specific annotation items.

### State Management

The app state is managed server-side using a SQLite database:

- `texts_db`: Stores annotation items, including messages, feedback, and notes.
- `total_items_length`: Tracks the total number of items in the database.

### Dynamic Content

HTMX is used extensively to create a dynamic user interface:

- `hx-post` attributes on forms trigger POST requests to update annotations.
- `hx-get` attributes on navigation buttons load new items.
- `hx-swap` determines how the new content should replace the old content, using `outerHTML` to replace entire elements.

### Key Components

1. **Arrow Navigation**: Allows users to move between annotation items.
2. **Annotation Buttons**: Provides options to mark text as correct or incorrect.
3. **Notes Field**: Allows users to add additional notes to each annotation.
4. **Text Display**: Shows the LLM-generated text to be annotated.
5. **SQLite** database integration

This app demonstrates the power of combining FastHTML, HTMX, and Tailwind CSS to create a responsive and efficient web application for text annotation tasks.

## Implementation

```python
from fasthtml.common import *
import json
import httpx

# Set up the app, including daisyui and tailwind for the chat component
tlink = Script(src="https://cdn.tailwindcss.com?plugins=typography"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")

def Arrow(arrow, hx_get, id):
    # Grey out button if you're at the end
    if arrow == "←": ptr_evnts = "pointer-events-none opacity-50" if id == 1 else ""
    elif arrow == "→": ptr_evnts = " pointer-events-none opacity-50" if id == total_items_length - 1 else ""
    # CSS Styling for both arrow buttons
    common_classes = "relative inline-flex items-center bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
    return A(Span(arrow, cls="sr-only"),
             Span(arrow, cls="h-5 w-5", aria_hidden="true"),
             hx_get=hx_get, hx_swap="outerHTML",
             cls=f" {'' if arrow=='←' else '-ml-px'} rounded-{'l' if arrow=='←' else 'r'}-md {common_classes} {ptr_evnts}")

def AnnotateButton(value, feedback):
    # Different button styling if it's already marked as correct/incorrect
    classes = '' if feedback=='correct' else 'btn-outline'
    # Green for correct red for incorrect
    classes += f" btn-{'success' if value=='correct' else 'error'}"
    classes += ' mr-2' if value=='correct' else ''
    return Button(value.capitalize(), name='feedback', value=value, cls='btn hover:text-white '+classes)
    
def render(Item):
    messages = json.loads(Item.messages)
    
    card_header = Div(cls="border-b border-gray-200 bg-white p-4")(
        Div(cls="flex justify-between items-center mb-4")(
            H3(f"Sample {Item.id} out of {total_items_length}" if total_items_length else "No samples in DB", cls="text-base font-semibold leading-6 text-gray-9000"),
            Div(cls="flex-shrink-0")(
                Arrow("←", f"{Item.id - 2}" if Item.id > 0 else "#", Item.id),
                Arrow("→", f"{Item.id}" if Item.id < total_items_length - 1 else "#", Item.id))),
        Div(cls="-ml-4 -mt-4 flex flex-wrap items-center justify-between sm:flex-nowrap")(
            Div(cls="ml-4 mt-4")(
                P(messages[0]['content'], cls="mt-1 text-sm text-gray-500 max-h-16 overflow-y-auto whitespace-pre-wrap"))))
    
    card_buttons_form = Div(cls="mt-4")(
        Form(cls="flex items-center", method="post", hx_post=f"{Item.id}", target_id=f"item_{Item.id}", hx_swap="outerHTML", hx_encoding="multipart/form-data")(
            Input(type="text", name="notes", value=Item.notes, placeholder="Additional notes?", cls="flex-grow p-2 my-4 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-transparent"),
            Div(cls="flex-shrink-0 ml-4")(
                AnnotateButton('correct', Item.feedback),
                AnnotateButton('incorrect', Item.feedback))))
    
    # Card component
    card = Div(cls="  flex flex-col h-full flex-grow overflow-auto", id=f"item_{Item.id}",
           style="min-height: calc(100vh - 6rem); max-height: calc(100vh - 16rem);")(
                card_header,
                Div(cls="bg-white shadow rounded-b-lg p-4 pt-0 pb-10 flex-grow overflow-scroll")(
                    Div(messages[1]['content'], id="main_text", cls="mt-2 w-full rounded-t-lg text-sm whitespace-pre-wrap h-auto marked")),
                card_buttons_form)
    return card

hdrs=(tlink, dlink, picolink, MarkdownJS(), HighlightJS())
app, rt, texts_db, Item = fast_app('texts.db',hdrs=hdrs, render=render, bodykw={"data-theme":"light"},
                                   id=int, messages=list, feedback=bool, notes=str, pk='id')


# Get Dummy Data
data_url = 'https://raw.githubusercontent.com/AnswerDotAI/fasthtml-example/main/annotate_text/data/dummy_data.jsonl'
response = httpx.get(data_url)

# Insert Dummy Data into Db
for line in response.text.splitlines():
    item = json.loads(line)
    texts_db.insert(messages=json.dumps(item), feedback=None, notes='')

# Set total_items_length after inserting dummy data
total_items_length = len(texts_db())
print(f"Inserted {total_items_length} items from dummy data")

@rt("/{idx}")
def post(idx: int, feedback: str = None, notes: str = None):
    print(f"Posting feedback: {feedback} and notes: {notes} for item {idx}")
    items = texts_db()
    item = texts_db.get(idx)
    
    item.feedback, item.notes = feedback, notes
    texts_db.update(item)

    next_item = next((i for i in items if i.id > item.id), items[0])    
    print(f"Updated item {item.id} with feedback: {feedback} and notes: {notes} moving to {next_item.id}")
    return next_item

@rt("/")
@rt("/{idx}")
def get(idx:int = 0):
    items = texts_db()
    
    index = idx 
    if index >= len(items): index = len(items) - 1 if items else 0

    # Container for card and buttons
    content = Div(cls="w-full max-w-2xl mx-auto flex flex-col max-h-full")(
        H1('LLM generated text annotation tool with FastHTML (and Tailwind)',cls="text-xl font-bold text-center text-gray-800 mb-8"),
        items[index])

    return Main(content,
                cls="container mx-auto min-h-screen bg-gray-100 p-8 flex flex-col",
                hx_target="this")

```
