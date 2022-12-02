from numpy.random import uniform


class TimeGenerator:
  def __init__(self, time, delta):
    self.time = time
    self.delta = delta

  def randomTime(self):
    return uniform(self.time - self.delta, self.time + self.delta)

class RequestGenerator:
  def __init__(self, timeGenerator, count, recievers = []):
    self.timeGenerator = timeGenerator
    self.requestCount = count
    self.receivers = recievers
    self.next = 0

  def generateRequest(self):
    self.requestCount -= 1
    for receiver in self.receivers:
      if receiver.receiveRequest(): return receiver
    return None

  def delay(self):
    return self.timeGenerator.randomTime()

class RequestProcessor:
  def __init__(self, timeGenerator, recievers = [], maxQueueSize = 1):
    self.timeGenerator = timeGenerator
    self.queue, self.received, self.maxQueue, self.processed = 0, 0, maxQueueSize, 0
    self.next = 0
    self.receivers = recievers

  def receiveRequest(self):
    if self.maxQueue > self.queue:
      self.queue += 1
      self.received += 1
      return True
    return False

  def processRequest(self):
    if self.queue > 0:
      self.queue -= 1
      self.processed += 1

  def delay(self):
    return self.timeGenerator.randomTime()

class Model:
  def __init__(self, requestGenerator, requestProcessors):
    self.requestGenerator = requestGenerator
    self.requestProcessors = requestProcessors

  def simulate(self, delta):
    refusalCount = 0
    generatedRequests = self.requestGenerator.requestCount

    self.requestGenerator.next = self.requestGenerator.delay()
    self.requestProcessors[0].next = self.requestProcessors[0].delay()

    blocks = [self.requestGenerator, *self.requestProcessors]
    
    currTime = 0
    while self.requestGenerator.requestCount >= 0:
      for block in blocks:
        if block.next <= currTime:
          if isinstance(block, RequestGenerator):
            receiver = self.requestGenerator.generateRequest()
            if receiver: receiver.next = currTime + receiver.delay()
            else: refusalCount += 1
            self.requestGenerator.next = currTime + self.requestGenerator.delay()
          elif isinstance(block, RequestProcessor):
            block.processRequest()
            if block.queue == 0: block.next = 0
            else: block.next = currTime + block.delay()
      currTime += delta
      
    return { "refusalProbability": refusalCount / generatedRequests, "refusalCount": refusalCount }

requestCount = 300

computer1 = RequestProcessor(TimeGenerator(15, 0))
computer2 = RequestProcessor(TimeGenerator(30, 0))

operator1 = RequestProcessor(TimeGenerator(20, 5), [computer1])
operator2 = RequestProcessor(TimeGenerator(40, 10), [computer1])
operator3 = RequestProcessor(TimeGenerator(40, 20), [computer2])

requestGenerator = RequestGenerator(TimeGenerator(10, 2), requestCount, [operator1, operator2, operator3])

model = Model(requestGenerator, [operator1, operator2, operator3, computer1, computer2])
result = model.simulate(0.01)

refusalCount, refusalProbability = result["refusalCount"], result["refusalProbability"]

print("Refusals: ", refusalCount)
print("Refusal probability: ", round(refusalProbability, 2))