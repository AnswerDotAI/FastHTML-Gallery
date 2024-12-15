# Intermediate Todo App (SQLite)

This project is a web-based implementation of an intermediate todo app built using FastHTML, HTMX, and SQLite. This builds on the minimal todo app by adding a due date and a done field to todos. Functionality related to these new fields has been added to the app. 

## Key Technologies and Techniques

1. **FastHTML**: A Python-based framework for building web applications with a focus on web fundamentals.
2. **HTMX**: Used to create dynamic server-side content updates that let you interact with the app without page reloads.
3. **SQLite**: A lightweight, serverless database used to store and manage todo items.
4. **FastSQL**: A library that simplifies database operations and integrates well with FastHTML.

## How It Works

### Server-Side Logic

The app uses FastHTML to define routes and handle todo list operations. Key routes include:

- `GET /`: The main page that renders the initial todo list.
- `POST /`: Handles adding new todo items.
- `DELETE /{id}`: Handles deleting todo items.

### Data Management

Todo items are stored in an SQLite database:

- `todos`: A table storing todo items with `id`, `title`, `done`, and `due`fields.

### Dynamic Content

HTMX is used to create a dynamic user interface:

- `hx-post` attribute on the form triggers a POST request to add new todos.
- `hx-delete` attribute on delete links triggers DELETE requests to remove todos.
- `hx-target` specifies where the response from the server should be inserted.
- `hx-swap` determines how the new content should be added or replaced.
    + `beforeend`: Adds the new content at the end of the target element.  This is used to add the new list item to end of the todo list.
    + `outerHTML`: Replaces the entire target element with the new content.  This is used to replaces the todo list item completely with `None` to remove it from the list.

### Key Features

1. **Add Todo**: Users can add new todos using a form at the top of the list.
2. **Delete Todo**: Each todo item has a delete link to remove it from the list.
3. **Real-time Updates**: The list updates dynamically without full page reloads.
4. **Persistent Storage**: Todos are stored in an SQLite database for data persistence.
5. **Due Date**: Each todo item has a due date field and the list is sorted by due date. If the item is past due the date is displayed in red.
6. **Done**: Each todo item has a done field. Items can be marked as done and the list shows completed items crossed out.
7. **fh-frakenui**: Simple styling is done using the fh-frakenui library.
8. **Edit Todo**: Each todo item has an edit link to edit the item. The edit form is displayed in a card and the todo list is updated with the new values.
