from numpy import linalg

TIME_DELTA = 1e-3
EPS = 1e-5

def __getCoefMatrix(matrix):
  count = len(matrix)
  coefMatrix = [[0.0 for j in range(count)] for i in range(count)]

  for i in range(count):
    for j in range(count):
      if (i == j):
        coefMatrix[i][i] = -sum(matrix[i]) + matrix[i][i] 
      else:
        coefMatrix[i][j] = matrix[j][i]
  return coefMatrix

def calculateProbability(matrix):
  count = len(matrix)
  
  coefMatrix = __getCoefMatrix(matrix)
  coefMatrix[count - 1] = [1 for j in range(count)]

  ordinateValues = [0 if i != count - 1 else 1 for i in range(count)]
  return linalg.solve(coefMatrix, ordinateValues).tolist()

def __calculateProbDelta(matrix, probCurr):
  count = len(matrix)
  
  probDelta = []
  coefMatrix = __getCoefMatrix(matrix)
  
  for i in range(count):
    for j in range(count):
      coefMatrix[i][j] *= probCurr[j]
    probDelta.append(sum(coefMatrix[i]) * TIME_DELTA)
  return probDelta
  
def calculateTime(matrix, prob):
  count = len(matrix)
  
  timeCurr = 0.0
  probCurr = [1.0 / count for i in range(count)]
  # probCurr = [0.0 if i != 0 else 1 for i in range(count)]
  time = [0.0 for i in range(count)]
  while not all(time):
    probDelta = __calculateProbDelta(matrix, probCurr)
    for i in range(count):
      if not time[i] and abs(probCurr[i] - prob[i]) <= EPS:
        time[i] = timeCurr
      probCurr[i] += probDelta[i]
    timeCurr += TIME_DELTA
  
  return time