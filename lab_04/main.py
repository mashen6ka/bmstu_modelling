import numpy.random as nr

REQUEST_COUNT = 10000
REENTER_PROBABILITY = 0.9
DELTA_T = 0.1

class UniformGenerator:
  def __init__(self, a=1, b=10):
    self._a = a
    self._b = b

  def generateTime(self):
    return nr.uniform(self._a, self._b)


class ErlangGenerator:
  def __init__(self, n=9, lmbd=0.5):
    self.n = n
    self.lmbd = lmbd

  def generateTime(self):
    return nr.gamma(self.n, self.lmbd)


class RequestGenerator:
  def __init__(self, generator):
    self._generator = generator
    self._receivers = set()

  def addReceiver(self, receiver):
    self._receivers.add(receiver)

  def removeReceiver(self, receiver):
    if (receiver in self._receivers):
      self._receivers.remove(receiver)

  def nextTimePeriod(self):
    return self._generator.generateTime()

  def emitRequest(self):
    for receiver in self._receivers:
      receiver.receiveRequest()


class RequestProcessor():
  def __init__(self, generator, reenterProbability=0):
    self._generator = generator
    self._currQueueSize = 0
    self._maxQueueSize = 0
    self._processedRequests = 0
    self._reenterProbability = reenterProbability
    self._reenteredRequests = 0

  def processedRequests(self):
    return self._processedRequests

  def maxQueueSize(self):
    return self._maxQueueSize

  def currQueueSize(self):
    return self._currQueueSize

  def reenteredRequests(self):
    return self._reenteredRequests

  def process(self):
    if self._currQueueSize > 0:
      self._processedRequests += 1
      self._currQueueSize -= 1
      if nr.random_sample() < self._reenterProbability:
        self._reenteredRequests += 1
        self.receiveRequest()

  def receiveRequest(self):
    self._currQueueSize += 1
    if self._currQueueSize > self._maxQueueSize:
      self._maxQueueSize += 1

  def nextTimePeriod(self):
    return self._generator.generateTime()


class Modeller:
  def __init__(self, generator, processor):
    self._generator = generator
    self._processor = processor
    self._generator.addReceiver(self._processor)

  def eventBasedModelling(self, requestCount):
    generator = self._generator
    processor = self._processor

    genPeriod = generator.nextTimePeriod()
    procPeriod = genPeriod + processor.nextTimePeriod()
    while processor.processedRequests() < requestCount:
      if genPeriod <= procPeriod:
        generator.emitRequest()
        genPeriod += generator.nextTimePeriod()
      else:
        processor.process()
        if processor.currQueueSize() > 0:
          procPeriod += processor.nextTimePeriod()
        else:
          procPeriod = genPeriod + processor.nextTimePeriod()

    return { "processedRequests": processor.processedRequests(),
             "reenteredRequests": processor.reenteredRequests(),
             "maxQueueSize": processor.maxQueueSize() }

  def timeBasedModelling(self, requestCount, dt=1):
    generator = self._generator
    processor = self._processor

    genPeriod = generator.nextTimePeriod()
    procPeriod = genPeriod + processor.nextTimePeriod()
    currTime = 0
    while processor.processedRequests() < requestCount:
      if genPeriod <= currTime:
        generator.emitRequest()
        genPeriod += generator.nextTimePeriod()
      if procPeriod <= currTime:
        processor.process()
        if processor.currQueueSize() > 0:
          procPeriod += processor.nextTimePeriod()
        else:
          procPeriod = genPeriod + processor.nextTimePeriod()
      currTime += dt

    return { "processedRequests": processor.processedRequests(),
             "reenteredRequests": processor.reenteredRequests(),
             "maxQueueSize": processor.maxQueueSize() }


generator = RequestGenerator(UniformGenerator())
processor = RequestProcessor(ErlangGenerator(), REENTER_PROBABILITY)
model = Modeller(generator, processor)
resultTimeBased = model.timeBasedModelling(REQUEST_COUNT, DELTA_T)
print("Time algorithm:")
print("-" * 26)
print("Processed requests: ", resultTimeBased["processedRequests"])
print("Reenter probability: ", REENTER_PROBABILITY)
print("Reentered requests: ", resultTimeBased["reenteredRequests"])
print("Buffer memory size: ", resultTimeBased["maxQueueSize"])
print("\n")

generator = RequestGenerator(UniformGenerator())
processor = RequestProcessor(ErlangGenerator(), REENTER_PROBABILITY)
model = Modeller(generator, processor)
resultEventBased = model.eventBasedModelling(REQUEST_COUNT)
print("Event algorithm:")
print("-" * 26)
print("Processed requests: ", resultEventBased["processedRequests"])
print("Reenter probability: ", REENTER_PROBABILITY)
print("Reentered requests: ", resultEventBased["reenteredRequests"])
print("Buffer memory size: ", resultEventBased["maxQueueSize"])
