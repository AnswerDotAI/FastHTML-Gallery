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
    url = "https://raw.githubusercontent.com/AnswerDotAI/FastHTML-Gallery/refs/heads/main/examples/applications/csv_editor/ex_data.csv"
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
    vals.append(Td(Group(Button('delete', hx_delete=remove.to(id=row['id']).lstrip('/')),
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

