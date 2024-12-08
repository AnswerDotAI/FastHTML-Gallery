from fasthtml.common import *
import random

app, rt = fast_app()

def get_progress(percent_complete: int):
    "Simulate progress check"
    return percent_complete + random.random()/3

@rt
def index():
    return (Div(H3("Start the job to see progress!"),id='progress_bar'),
            Button("Start Job",post=update_status, hx_target="#progress_bar"))

@rt
def update_status(): 
    "Start job and progress bar"
    return progress_bar(percent_complete=0)

@rt
def update_progress(percent_complete: float):
    # Check if done
    if percent_complete >= 1: return H3("Job Complete!", id="progress_bar")
    # get progress
    percent_complete = get_progress(percent_complete)
    # Update progress bar
    return progress_bar(percent_complete)

def progress_bar(percent_complete: float):
    return Progress(id="progress_bar",value=percent_complete,
                    get=update_progress,hx_target="#progress_bar",hx_trigger="every 500ms",
                    hx_vals=f"js:'percent_complete': '{percent_complete}'")

serve()