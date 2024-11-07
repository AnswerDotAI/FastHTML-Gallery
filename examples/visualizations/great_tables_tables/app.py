from functools import cache
import polars as pl
from great_tables import GT, html
from great_tables.data import sza
from fasthtml.common import *

app, rt = fast_app()

@cache
def get_sza_pivot():
    # Filter and pivot the data
    return (pl.from_pandas(sza)
            .filter((pl.col("latitude") == "20") & (pl.col("tst") <= "1200"))
            .select(pl.col("*").exclude("latitude"))
            .drop_nulls()
            .pivot(values="sza", index="month", on="tst", sort_columns=True))

def get_notstr_table(color1: str = "#663399", color2: str = "#FFA500"):
    # Create the table
    sza_gt = (GT(get_sza_pivot(), rowname_col="month")
                .data_color(
                    domain=[90, 0],
                    palette=[color1, "white", color2],
                    na_color="white",)
                .tab_header(
                    title="Solar Zenith Angles from 05:30 to 12:00",
                    subtitle=html("Average monthly values at latitude of 20&deg;N."))
                .sub_missing(missing_text=""))
    # Return the table by converting to raw HTML
    return Div(NotStr(sza_gt.as_raw_html()))

@app.post("/submit", name="submit")
def post(d: dict):
    return get_notstr_table(**d)

@rt
def index():
    return (Title("FastHTML-GT Website"),
            Titled("Great Tables shown in FastHTML", style="text-align:center"),
            Main(cls='container')(
                Form(post="submit", hx_target="#gt", hx_trigger="input")(
                    Grid(Card(H2("Color1"), Input(type="color",id="color1", value="#663399")),
                         Card(H2("Color2"), Input(type="color",id="color2", value="#FFA500")))),
                Div(get_notstr_table(), id="gt")))
