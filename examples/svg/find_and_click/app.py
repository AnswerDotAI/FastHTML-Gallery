from fasthtml.common import *
from fasthtml.svg import *
from fasthtml.components import Script
from random import randint
from uuid import uuid4
import time

timer = {}
app, rt = fast_app(live=True, hdrs=[Script(src="https://d3js.org/d3.v7.min.js")])

class Timer:
    def __init__(self):
        self.start = time.time()
    
    def stop(self):
        self.stop = time.time()
        return self.stop - self.start


def mk_circle(count):
    return Circle(cx=randint(20,180),cy=randint(10,70),r=randint(5,15),fill="red",
        id="circle",hx_get=f"/click/{count+1}", hx_swap="outerHTML")

def mk_click_count(count):
    return P(f"You have clicked {count} times",id="click-count")
    
@app.get('/')
def homepage(sess):
    if 'id' not in sess: sess['id'] = str(uuid4())
    return Div(
        P("Click the circle to start the timer"),
        mk_click_count(0),P(id="timer"),
        Svg(viewBox="0 0 200 80",id="svg-box")(
            mk_circle(0)
        ),
    )

@rt("/click/{count}")
def click(count: int,sess):
    ret,et = [],""
    if count == 1:
        timer[sess['id']] = Timer()
    if count == 10:
        elapsed_time=timer[sess['id']].stop()
        count = 0
        et=f"Time to click 10 times: {elapsed_time:.2f} seconds"

    return SvgInb(mk_circle(count)),mk_click_count(count)(hx_swap_oob="outerHTML"),P(et,id="timer",hx_swap_oob="outerHTML")


serve()