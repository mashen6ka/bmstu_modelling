from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algs import uniformDistribution, uniformDistributionDensity, erlangDistribution, erlangDistributionDensity

def initCanvasFigure(title):
  fig, axs = plt.subplots(2, figsize=(5, 6), dpi=50)

  fig.suptitle(title)

  axs[0].set_xlabel('x')
  axs[0].set_ylabel('F(x)')

  axs[1].set_xlabel('x')
  axs[1].set_ylabel('f(x)')

  axs[0].grid(True)
  axs[1].grid(True)

  return fig, axs

def drawCanvasFigure(axs, x, y, density):
  axs[0].plot(x, y, color='blue')
  axs[1].plot(x, density, color='blue')

def __plotUniform():
  a = float(txtA.get())
  b = float(txtB.get())

  x1 = float(txtX1U.get())
  x2 = float(txtX2U.get())

  plotUniform(a, b, x1, x2)

def plotUniform(a, b, x1, x2):
  x = np.arange(x1, x2, 0.0001)
  y = [uniformDistribution(_x, a, b) for _x in x]
  y_density = [uniformDistributionDensity(_x, a, b) for _x in x]

  fig, axs = initCanvasFigure("Uniform distribution")
  drawCanvasFigure(axs, x, y, y_density)

  drawCanvasUniform(fig)

def __plotErlang():
  n = int(txtN.get())
  lmbd = float(txtLmbd.get())

  x1 = float(txtX1E.get())
  x2 = float(txtX2E.get())

  plotErlang(n, lmbd, x1, x2)

def plotErlang(n, lmbd, x1, x2):
  x = np.arange(x1, x2, 0.0001)
  y = [erlangDistribution(_x, n, lmbd) for _x in x]
  y_density = [erlangDistributionDensity(_x, n, lmbd) for _x in x]

  fig, axs = initCanvasFigure("Erlang distribution")
  drawCanvasFigure(axs, x, y, y_density)

  drawCanvasErlang(fig)

def drawCanvasUniform(fig):
  global canvasUniform
  if canvasUniform:
    canvasUniform.get_tk_widget().destroy()

  canvasUniform = FigureCanvasTkAgg(fig, master=window)
  canvasUniform.draw()
  canvasUniform.get_tk_widget().grid(column=0, row=6, columnspan=4, padx=20, pady=20)

def drawCanvasErlang(fig):
  global canvasErlang
  if canvasErlang:
    canvasErlang.get_tk_widget().destroy()

  canvasErlang = FigureCanvasTkAgg(fig, master=window)
  canvasErlang.draw()
  canvasErlang.get_tk_widget().grid(column=5, row=6, columnspan=4, padx=20, pady=20)

window = Tk() 

canvasUniform = None
canvasErlang = None


window.title('Lab1: Uniform & Erlang distribution') 
window.geometry("1100x750")
window.resizable(False,False)

lblU = Label(window, text="Uniform distribution")
lblU.grid(column=0, row=0, columnspan=4)

lblA = Label(window, text="Parameter a:") 
lblA.grid(column=0, row=1, padx=20) 
txtA = Entry(window,width=10)
txtA.insert(0, -10)
txtA.grid(column=1, row=1)

lblB = Label(window, text="Parameter b:")
lblB.grid(column=2, row=1) 
txtB = Entry(window,width=10)
txtB.insert(0, 10)
txtB.grid(column=3, row=1)

lblX1U = Label(window, text="Left border:") 
lblX1U.grid(column=0, row=2, padx=20) 
txtX1U = Entry(window,width=10)
txtX1U.insert(0, -20)
txtX1U.grid(column=1, row=2)

lblX2U = Label(window, text="Right border:")
lblX2U.grid(column=2, row=2) 
txtX2U = Entry(window,width=10)
txtX2U.insert(0, 20)
txtX2U.grid(column=3, row=2)

btnU = Button(window, text="Plot uniform distribution", command=__plotUniform)  
btnU.grid(column=0, columnspan=4, row=3)
__plotUniform()

lblE = Label(window, text="Erlang distribution")
lblE.grid(column=5, row=0, columnspan=4)

lblN = Label(window, text="Parameter n:")
lblN.grid(column=5, row=1) 
txtN = Entry(window,width=10)
txtN.insert(0, 1)
txtN.grid(column=6, row=1)

lblLmbd = Label(window, text="Parameter lambda:")
lblLmbd.grid(column=7, row=1) 
txtLmbd = Entry(window,width=10)
txtLmbd.insert(0, 1)
txtLmbd.grid(column=8, row=1)

lblX1E = Label(window, text="Left border:") 
lblX1E.grid(column=5, row=2, padx=20) 
txtX1E = Entry(window,width=10)
txtX1E.insert(0, 0)
txtX1E.config(state='disabled')
txtX1E.grid(column=6, row=2)

lblX2E = Label(window, text="Right border:")
lblX2E.grid(column=7, row=2) 
txtX2E = Entry(window,width=10)
txtX2E.insert(0, 10)
txtX2E.grid(column=8, row=2)


btnE = Button(window, text="Plot erlang distribution", command=__plotErlang)
btnE.grid(column=5, row=3, columnspan=4)
__plotErlang()

window.mainloop()