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