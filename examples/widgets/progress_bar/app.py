from fasthtml.common import *
import random

app, rt = fast_app()

def get_progress(percent_complete: int):
    # simulate progress check
    percent_complete += random.random()/3
    return percent_complete

@app.get('/')
def homepage():
    return Div(H3("Start the job to see progress!"),id='progress_bar'),Button("Start Job",hx_post='/widgets/progress_bar/job', hx_target="#progress_bar",)

@app.post('/job')
def update_status():
    # Start the job
    return progress_bar(percent_complete=0)

@app.get('/job')
def update_progress(percent_complete: float):
    # Check if done
    if percent_complete >= 1: return H3("Job Complete!", id="progress_bar")
    # get progress
    percent_complete = get_progress(percent_complete)
    # Update progress bar
    return progress_bar(percent_complete)

def progress_bar(percent_complete: float):
    return Progress(id="progress_bar",value=percent_complete,
                    hx_get='/widgets/progress_bar/job',hx_target="#progress_bar",hx_trigger="every 500ms",
                    hx_vals=f"js:'percent_complete': '{percent_complete}'")
