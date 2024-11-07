from fasthtml.common import *
import numpy as np, seaborn as sns, matplotlib.pylab as plt

app,rt = fast_app()
data = np.random.rand(4,10)

def fh_svg(func):
  "show svg in fasthtml decorator"
  def wrapper(*args, **kwargs):
      func(*args, **kwargs) # calls plotting function
      f = io.StringIO() # create a buffer to store svg data
      plt.savefig(f, format='svg', bbox_inches='tight')
      f.seek(0) # beginning of file
      svg_data = f.getvalue()
      plt.close()
      return NotStr(svg_data)
  return wrapper

@fh_svg
def plot_heatmap(matrix,figsize=(6,7),**kwargs):
  plt.figure(figsize=figsize)
  sns.heatmap(matrix, cmap='coolwarm', annot=False,**kwargs)

@rt
def index():
  return Div(Label(H3("Heatmap Columns"), _for='n_cols'),
             Input(type="range", min="1", max="10", value="1",
                   get=update_heatmap, hx_target="#plot", id='n_cols'),
             Div(id="plot"))

@app.get("/update_charts")
def update_heatmap(n_cols:int):
  svg_plot = plot_heatmap(data[:,:n_cols])
  return svg_plot

serve()
