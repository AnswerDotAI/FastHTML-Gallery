from fasthtml.common import *
import numpy as np, seaborn as sns, matplotlib.pylab as plt

app,rt = fast_app()
data = np.random.rand(4,5)

# define the decorator
def fh_svg(func):
  "show svg in fasthtml"
  def wrapper(*args, **kwargs):
      func(*args, **kwargs)

      f = io.StringIO()
      plt.savefig(f, format='svg', bbox_inches='tight')

      f.seek(0)
      svg_data = f.getvalue()
      plt.close()
      return NotStr(svg_data)
  return wrapper


@fh_svg
def plot_heatmap(matrix,figsize=(6,7),**kwargs):
  plt.figure(figsize=figsize)
  sns.heatmap(matrix, cmap='coolwarm', annot=False,**kwargs)
  plt.ylabel('')
  plt.title('heatmap')


@rt("/")
def get():
  return Div(
    H3("Move the slider to change the width of the graph"),
    Input(
       type="range",
       min="1", max="10", value="1",
       hx_get='/update_chart', hx_target="#plot",
       id='width'),
    Div(id="plot")
 )

@rt("/update_chart")
def get(width:int):
  svg_plot = plot_heatmap(data,figsize=(width,7))
  return svg_plot

serve()