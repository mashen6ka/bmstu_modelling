from random import randint

def generateTabular(count, low=0, high=100):
  seq = []
  with open('table.txt') as file:
    for line in file:
      for curr in line.split(" ")[1:]:
        if (len(seq) < count and curr != ''): seq.append(low + int(curr) % (high - low))
      if (len(seq) >= count): break
  return seq

def __settingsLinearCongruent():
  # оптимальные начальные значения:
  # m, a, c, x0  = 312500, 36261, 66037, 60000
  m = randint(100000, 1000000)
  a = randint(10000, 100000)
  c = randint(10000, 100000)
  x0 = randint(10000, 100000)
  return m, a, c, x0

def generateLinearCongruent(count, low=0, high=100):
  m, a, c, x0 = __settingsLinearCongruent()
  
  seq = []
  seq.append(x0)
  for i in range(1, count + 1):
    curr = (seq[i-1] * a + c) % m
    seq.append(low + curr % (high - low))
  return seq[1:]

def __occurrenceRate(seq):
  occurrence = dict()
  for num in seq:
    if (not occurrence.get(num)):
      occurrence[num] = 1
    else:
      occurrence[num] += 1
  return occurrence

def __increment(seq):
  increment = []
  for i in range(1, len(seq)):
    increment.append(seq[i] - seq[i-1])
  return increment

def randomnessFactor(seq):
  occurence = __occurrenceRate(seq)
  increment = __increment(seq)
  k = max(__occurrenceRate(occurence.values()))
  m = max(__occurrenceRate(increment).values())
  return 1 - (k + m + 1) / len(seq) / 2
