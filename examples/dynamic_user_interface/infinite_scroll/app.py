from fasthtml.common import *
from typing import List, Tuple, NamedTuple
import uuid

class PaginatedTable(NamedTuple):
    rows: List[Tr]
    next_page: int
    end_reached: bool

def generate_contact(id: int) -> dict:
    return {'name': 'Agent Smith',
            'email': f'void{str(id)}@matrix.com',
            'phone': f'555-1234-{str(id)}',
            'id': str(uuid.uuid4())
            }

def create_table_row(row_data: dict, is_header: bool = False) -> Tr:
    cell_type = Th if is_header else Td
    return Tr(*[cell_type(str(field)) for field in row_data])

def create_table_rows(df: pd.DataFrame, include_header: bool = True) -> List[Tr]:
    rows = []
    if include_header:
        rows.append(create_table_row(df.columns, is_header=True))
    rows.extend(create_table_row(row) for _, row in df.iterrows())
    return rows

def paginate_table(df: pd.DataFrame, page_size: int = 10, page_num: int = 1) -> PaginatedTable:
    total_rows = len(df)
    total_pages = -(-total_rows // page_size)  # Ceiling division

    if page_num < 1 or page_num > total_pages:
        raise ValueError(f"Invalid page number. Must be between 1 and {total_pages}")

    start_index = (page_num - 1) * page_size
    end_index = min(start_index + page_size, total_rows)
    
    include_header = page_num == 1
    rows = create_table_rows(df.iloc[start_index:end_index], include_header)
    
    return PaginatedTable(
        rows=rows,
        next_page=page_num + 1,
        end_reached=page_num == total_pages
    )

def htmx_infinite_scroll(data: pd.DataFrame, page_size: int = 20, page: int = 1) -> Tuple[Tr, ...]:
    paginated_data = paginate_table(data, page_size, page)
    
    if not paginated_data.end_reached:
        last_row = paginated_data.rows[-1]
        last_row.attrs.update({
            'hx-get': f'/dynamic_user_interface/infinite_scroll/page/?idx={paginated_data.next_page}',
            'hx-trigger': 'revealed',
            'hx-swap': 'afterend'
        })
    
    return tuple(paginated_data.rows)

app, rt = fast_app(hdrs=(picolink))

app.get("/")
def homepage():
    return Titled('Infinite Scroll',
                  P("Example (faked) person data taken from ", A("this repo", href="https://github.com/datablist/sample-csv-files/tree/main")),
                  H2("A large data frame"),
                  Div(Table(htmx_infinite_scroll(people, page_size=20, page=1))),
                  Div(id="end-of-table"))

@rt("/page/")
def get(idx:int|None = 0):
    return htmx_infinite_scroll(people, page_size=20, page=idx)

