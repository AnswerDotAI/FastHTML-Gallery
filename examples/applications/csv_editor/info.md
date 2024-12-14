# CSV Editor App

This project is a web-based CSV editor built using FastHTML, HTMX, and SQLite.

## Key Technologies and Techniques

1. **FastHTML**: A Python-based framework for building web applications with a focus on web fundamentals.
2. **HTMX**: Used to create dynamic server-side content updates that let you interact with the app without page reloads.
3. **SQLite**: A lightweight, serverless database used to store and manage CSV data.
4. **FastSQL**: A library that simplifies database operations and integrates well with FastHTML.
5. **httpx**: An asynchronous HTTP client for Python, used to fetch example CSV data.

## How It Works

### Server-Side Logic

The app uses FastHTML to define routes and handle CSV operations. Key routes include:

- `GET /`: The main page that renders the CSV upload interface.
- `GET /get_test_file`: Provides an example CSV file for download.
- `POST /upload`: Handles CSV file uploads and displays the data.
- `POST /update`: Updates individual CSV rows.
- `DELETE /remove`: Deletes specific rows from the CSV data.
- `GET /download`: Allows downloading the current CSV data.

### Data Management

CSV data is stored in an SQLite database:

- A unique table is created for each session, storing the CSV data with an 'id' column as the primary key.

### Dynamic Content

HTMX is used to create a dynamic user interface:

- `hx-post` attribute on the upload button triggers a POST request to upload and display CSV data.
- `hx-delete` and `hx-post` attributes on row buttons handle row deletion and updates.
- `hx-target` specifies where the response from the server should be inserted.
- `hx-swap` determines how the new content should be added or replaced.
- `hx-include` is used to include specific form data in requests.

### Key Features

1. **CSV Upload**: Users can upload CSV files to view and edit the data.
2. **Example CSV**: An example CSV file is provided for download.
3. **Data Display**: Uploaded CSV data is displayed in an editable table format.
4. **Row Editing**: Each row can be updated or deleted individually.
5. **Data Download**: The current state of the CSV data can be downloaded at any time.
6. **Session Management**: Each user session has its own unique data storage.
7. **File Size Limit**: Only the first 50 rows of a CSV file are processed and displayed.

This CSV Editor app demonstrates how FastHTML and HTMX can be combined to create a responsive, server-side web application for data manipulation tasks.