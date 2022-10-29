from tkinter import *
from algs import calculateProbability, calculateTime

MAX_STATE_COUNT = 10
TIME_DELTA = 1e-3
EPS = 1e-5

def initMatrix(startColumn, startRow):
  global txtMatrix
  txtMatrix = []
  for i in range(MAX_STATE_COUNT):
    row = []
    for j in range(MAX_STATE_COUNT):
      lblLeft = Label(window, text="S"+str(i+1)+":")
      lblLeft.grid(column=startColumn, row=startRow+i+1)
      lblUp = Label(window, text="S"+str(j+1)+":")
      lblUp.grid(column=startColumn+j+1, row=startRow)
      
      cell = Entry(window, width=5, fg='blue', font=('Arial',16))
      cell.grid(column=startColumn+j+1, row=startRow+i+1)
      cell.insert(END, 0)
      row.append(cell)
    txtMatrix.append(row)

def initResult(startColumn, startRow):
  global txtResult
  txtResult = []
  params = ["P", "t"]
  for i in range(len(params)):
    row = []
    for j in range(MAX_STATE_COUNT):
      lblLeft = Label(window, text=params[i])
      lblLeft.grid(column=startColumn, row=startRow+i+1)
      lblUp = Label(window, text="S"+str(j+1)+":")
      lblUp.grid(column=startColumn+j+1, row=startRow)
      
      cell = Entry(window, width=5, fg='blue', font=('Arial',16))
      cell.grid(column=startColumn+j+1, row=startRow+i+1)
      # cell.insert(END, 0)
      cell.config(state='readonly', readonlybackground="white")
      row.append(cell)
    txtResult.append(row)
    
def initStateCountBtns():
  for i in range(MAX_STATE_COUNT):
    callback = lambda n: lambda: updateStateCount(n)
    btn = Button(window, text=str(i+1), command=callback(i+1))
    btn.grid(column=i+2, row=0)

def updateMatrix(count):
  global txtMatrix
  if count > MAX_STATE_COUNT:
    return
  for i in range(MAX_STATE_COUNT):
    for j in range(MAX_STATE_COUNT):
      if i > count-1 or j > count-1:
        txtMatrix[i][j].delete(0, 'end')
        txtMatrix[i][j].config(state='disabled')
      else:
        txtMatrix[i][j].config(state='normal')
        txtMatrix[i][j].delete(0, 'end')
        txtMatrix[i][j].insert(END, 0)
        
def updateResult(count):
  global txtResult
  if count > MAX_STATE_COUNT:
    return
  for i in range(len(txtResult)):
    for j in range(MAX_STATE_COUNT):
      if j > count-1:
        txtResult[i][j].delete(0, 'end')
        txtResult[i][j].config(state='disabled')
      else:
        txtResult[i][j].config(state='readonly')
        txtResult[i][j].delete(0, 'end')
        # txtResult[i][j].insert(END, 0)

def updateStateCount(count):
  updateMatrix(count)
  updateResult(count)

def getIntensityMatrix():
  matrix = []
  for i in range(MAX_STATE_COUNT):
    row = []
    for j in range(MAX_STATE_COUNT):
      if txtMatrix[i][j]["state"] == 'normal':
        row.append(float(txtMatrix[i][j].get()))
    if (len(row)):
      matrix.append(row)
  return matrix

def calculate():
  global txtResult
  matrix = getIntensityMatrix()
  
  probRes = calculateProbability(matrix)
  timeRes = calculateTime(matrix, probRes)
  
  result = [probRes, timeRes]
  
  for i in range(len(result)):
    for j in range(len(result[0])):
      txtResult[i][j].config(state='normal')
      txtResult[i][j].delete(0, 'end')
      txtResult[i][j].insert(END, "{:.2f}".format(round(result[i][j], 2)))
      txtResult[i][j].config(state='readonly')
  return

txtMatrix = []
txtResult = []

window = Tk()

window.title('Lab2: Markov chains') 
window.geometry("770x520")
window.resizable(False,False)

lblStateCount = Label(window, text="State count:", padx=20)
lblStateCount.grid(column=0, row=0)

initStateCountBtns()

lblMatrix = Label(window, text="Intensity matrix: ", padx=20)
lblMatrix.grid(column=0, row=1)

initMatrix(1, 1)

btnStateCount = Button(window, text="Calculate", command=calculate)
btnStateCount.grid(column=1, row=13, columnspan=12, pady=20)

lblMatrix = Label(window, text="Result: ", padx=20)
lblMatrix.grid(column=0, row=14)

initResult(1, 14)

window.mainloop()