import anvil.server
import numpy as np
import seaborn as sns
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def prepPlots():
  x = np.array(range(-50,50))
  y1 = x
  y2 = x*x
  y3 = x*x*x
  sns.set_theme()
  fig1 = sns.lineplot(x=x, y=y1)
  fig2 = sns.lineplot(x=x, y=y2)
  fig3 = sns.lineplot(x=x, y=y3)
  return fig1, fig2, fig3