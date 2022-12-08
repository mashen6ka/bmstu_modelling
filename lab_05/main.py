from numpy.random import uniform

class TimeGenerator:
  def __init__(self, time, delta):
    self.time = time
    self.delta = delta

  def randomTime(self):
    return uniform(self.time - self.delta, self.time + self.delta)

class RequestGenerator:
  def __init__(self, timeGenerator, count, receivers = []):
    self.timeGenerator = timeGenerator
    self.requestCount = count
    self.receivers = receivers
    self.next = 0

  def generateRequest(self, currTime):
    self.requestCount -= 1
    self.next = currTime + self.generateDuration()
    for receiver in self.receivers:
      if not receiver.busy: return receiver
    return None

  def generateDuration(self):
    return self.timeGenerator.randomTime()

class RequestOperator:
  def __init__(self, timeGenerator, processor):
    self.timeGenerator = timeGenerator
    self.next = 0
    self.processor = processor
    self.busy = False

  def receiveRequest(self, currTime):
    self.busy = True
    self.next = currTime + self.generateDuration()

  def processRequest(self):
    if self.busy:
      self.next = 0
      self.busy = False

  def generateDuration(self):
    return self.timeGenerator.randomTime()

class RequestProcessor:
  def __init__(self, timeGenerator):
    self.timeGenerator = timeGenerator
    self.queueSize = 0
    self.next = 0

  def pushRequest(self):
    self.queueSize += 1

  def popRequest(self, currTime):
    if self.queueSize > 0:
      self.queueSize -= 1
      self.next = currTime + self.generateDuration()
    else:
      self.next = 0

  def generateDuration(self):
    return self.timeGenerator.randomTime()

class Model:
  def __init__(self, generator, operators, processors):
    self.generator = generator
    self.operators = operators
    self.processors = processors

  def simulate(self, delta):
    refusalCount = 0
    generatedRequests = self.generator.requestCount
    
    blocks = [self.generator, *self.operators, *self.processors]
    
    currTime = 0
    while self.generator.requestCount > 0:
      for block in blocks:
        if block.next <= currTime:
          if isinstance(block, RequestGenerator):
            receiver = self.generator.generateRequest(currTime)
            if not receiver: refusalCount += 1
            else: receiver.receiveRequest(currTime)
          elif isinstance(block, RequestOperator):
            block.processRequest()
            block.processor.pushRequest()
          elif isinstance(block, RequestProcessor):
            block.popRequest(currTime)
      currTime += delta
      
    return { "refusalProbability": refusalCount / generatedRequests, "refusalCount": refusalCount }

requestCount = 1000

computer1 = RequestProcessor(TimeGenerator(15, 0))
computer2 = RequestProcessor(TimeGenerator(30, 0))

operator1 = RequestOperator(TimeGenerator(20, 5), computer1)
operator2 = RequestOperator(TimeGenerator(40, 10), computer1)
operator3 = RequestOperator(TimeGenerator(40, 20), computer2)

requestGenerator = RequestGenerator(TimeGenerator(10, 2), requestCount, [operator1, operator2, operator3])

model = Model(requestGenerator, [operator1, operator2, operator3], [computer1, computer2])
result = model.simulate(0.01)

refusalCount, refusalProbability = result["refusalCount"], result["refusalProbability"]

print("Requests: ", requestCount)
print("Refusals: ", refusalCount)
print("Refusal probability: ", round(refusalProbability, 2))