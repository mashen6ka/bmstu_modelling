import math

def uniformDistribution(x, a, b):
  if a <= x < b:
    return (x - a) / (b - a)
  if x < a:
    return 0
  return 1

def uniformDistributionDensity(x, a, b):
  if a <= x <= b:
    return 1 / (b - a)
  return 0

def erlangDistribution(x, n, lmbd):
  return 1 - math.exp(-x / lmbd) * sum((x / lmbd)**i/math.factorial(i) for i in range(n))

def erlangDistributionDensity(x, n, lmbd):
  return x**(n - 1) * math.exp(-x * lmbd) * lmbd**n / math.factorial(n - 1)
