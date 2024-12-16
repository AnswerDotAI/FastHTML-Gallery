# CSV Editor

> An app to upload csv files, edit in browser, and then download the updated file

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

## Implementation

```python
from fasthtml.common import *
from uuid import uuid4

db = database('sqlite.db')
hdrs = (Style('''
button,input { margin: 0 1rem; }
[role="group"] { border: 1px solid #ccc; }
.edited { outline: 2px solid orange; }
'''), )
app, rt = fast_app(hdrs=hdrs)

@rt
async def get_test_file():
    import httpx
    url = "https://raw.githubusercontent.com/AnswerDotAI/FastHTML-Gallery/main/applications/start_simple/csv_editor/ex_data.csv"
    response = await httpx.AsyncClient().get(url)
    return Response(response.text, media_type="text/csv",
                        headers={'Content-Disposition': 'attachment; filename="ex_data.csv"'})

@rt
def index(sess):
    if 'id' not in sess: sess['id'] = str(uuid4())
    return Titled("CSV Uploader",
                 A('Download Example CSV', href="get_test_file", download="ex_data.csv"),
                 Group(Input(type="file", name="csv_file", accept=".csv"),
                       Button("Upload", hx_post="upload", hx_target="#results",
                              hx_encoding="multipart/form-data", hx_include='previous input'),
                       A('Download', href='download', type="button")),
                 Div(id="results"))

def render_row(row):
    vals = [Td(Input(value=v, name=k, oninput="this.classList.add('edited')")) for k,v in row.items()]
    vals.append(Td(Group(Button('delete', hx_delete=remove.rt(id=row['id']).lstrip('/')),
                   Button('update', hx_post='update', hx_include="closest tr"))))
    return Tr(*vals, hx_target='closest tr', hx_swap='outerHTML')

@rt
def download(sess):
    tbl = db[sess['id']]
    csv_data = [",".join(map(str, tbl.columns_dict))]
    csv_data += [",".join(map(str, row.values())) for row in tbl()]
    headers = {'Content-Disposition': 'attachment; filename="data.csv"'}
    return Response("\n".join(csv_data), media_type="text/csv", headers=headers)

@rt('/update')
def post(d:dict, sess): return render_row(db[sess['id']].update(d))

@app.delete('/remove')
def remove(id:int, sess): db[sess['id']].delete(id)

@rt("/upload")
def post(csv_file: UploadFile, sess):
    db[sess['id']].drop(ignore=True)
    if not csv_file.filename.endswith('.csv'): return "Please upload a CSV file"
    content = b''
    for i, line in enumerate(csv_file.file):
        if i >= 51: break
        content += line
    tbl = db.import_file(sess['id'], content, pk='id')
    header = Tr(*map(Th, tbl.columns_dict))
    vals = [render_row(row) for row in tbl()]
    return (Span('First 50 rows only', style="color: red;") if i>=51 else '', Table(Thead(header), Tbody(*vals)))

serve()


```
