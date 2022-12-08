from numpy.random import uniform
from random import random

REFUSAL_QUEUE_SIZE = 10

MIN_QUEUE_SIZE = 5
MAX_QUEUE_SIZE = 7

HAS_TICKET_PROBABILITY = 0.6

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
    self.hasTicketProbability = HAS_TICKET_PROBABILITY

  def generateRequest(self, currTime):
    self.requestCount -= 1
    self.next = currTime + self.generateDuration()
    
    hasTicket = random() < self.hasTicketProbability
    if hasTicket: return self.receivers[0].getReceiver()
    
    minQueueSize = self.receivers[0].queueSize
    minReceiverId = 0
    for index, receiver in enumerate(self.receivers):
      if receiver.queueSize < minQueueSize:
        minQueueSize = receiver.queueSize
        minReceiverId = index
    return self.receivers[minReceiverId]
      
  def generateDuration(self):
    return self.timeGenerator.randomTime()

class RequestProcessor:
  def __init__(self, timeGenerator, receivers = []):
    self.timeGenerator = timeGenerator
    self.queueSize = 0
    self.next = 0
    self.receivers = receivers

  def pushRequest(self):
    self.queueSize += 1

  def popRequest(self, currTime):
    if self.queueSize > 0:
      self.queueSize -= 1
      self.next = currTime + self.generateDuration()
      return True
    else:
      self.next = 0
      return False

  def getReceiver(self):
    return self.receivers[0]

  def generateDuration(self):
    return self.timeGenerator.randomTime()

class Exhibition(RequestProcessor):
  def __init__(self, timeGenerator):
    super().__init__(timeGenerator)

  def pushRequest(self):
    super().pushRequest()

  def popRequest(self, currTime):
    if self.queueSize >= MIN_QUEUE_SIZE:
      self.queueSize -= min(self.queueSize, MAX_QUEUE_SIZE)
      self.next = currTime + self.generateDuration()
      return True
    else:
      self.next = 0
      return False
  
  def getReceiver(self):
    return None
  
  def generateDuration(self):
    return super().generateDuration()

class BoxOffice(RequestProcessor):
  def __init__(self, timeGenerator, receivers = []):
    super().__init__(timeGenerator, receivers)

  def pushRequest(self):
    super().pushRequest()

  def popRequest(self, currTime):
    return super().popRequest(currTime)
  
  def getReceiver(self):
    minQueueSize = self.receivers[0].queueSize
    minReceiverId = 0
    
    for index, receiver in enumerate(self.receivers):
      if receiver.queueSize < minQueueSize:
        minQueueSize = receiver.queueSize
        minReceiverId = index
    if minQueueSize >= REFUSAL_QUEUE_SIZE: return None
    return self.receivers[minReceiverId]
  
  def generateDuration(self):
    return super().generateDuration()

class Model:
  def __init__(self, generator, processors):
    self.generator = generator
    self.processors = processors

  def simulate(self, delta):
    refusalCount = 0
    generatedRequests = self.generator.requestCount
    
    blocks = [self.generator, *self.processors]

    currTime = 0
    while self.generator.requestCount > 0:
      for block in blocks:
        if block.next <= currTime:
          if isinstance(block, RequestGenerator):
            receiver = self.generator.generateRequest(currTime)
            if not receiver: refusalCount += 1
            else: receiver.pushRequest()
          elif isinstance(block, BoxOffice):
            if block.popRequest(currTime):
              receiver = block.getReceiver()
              if receiver is None: refusalCount += 1
              else: receiver.pushRequest()
          elif isinstance(block, Exhibition):
            block.popRequest(currTime)
      currTime += delta
    return { "refusalProbability": refusalCount / generatedRequests, "refusalCount": refusalCount }

requestCount = 5000

exhibition1 = Exhibition(TimeGenerator(75, 3))
exhibition2 = Exhibition(TimeGenerator(75, 3))

boxOffice1 = BoxOffice(TimeGenerator(5, 3), [exhibition1, exhibition2])
boxOffice2 = BoxOffice(TimeGenerator(5, 3), [exhibition1, exhibition2])
boxOffice3 = BoxOffice(TimeGenerator(5, 3), [exhibition1, exhibition2])

requestGenerator = RequestGenerator(TimeGenerator(5, 2), requestCount, [boxOffice1, boxOffice2, boxOffice3])

model = Model(requestGenerator, [boxOffice1, boxOffice2, boxOffice3, exhibition1, exhibition2])
result = model.simulate(0.01)

refusalCount, refusalProbability = result["refusalCount"], result["refusalProbability"]

print("Visitors: ", requestCount)
print("Probability of having a ticket: ", HAS_TICKET_PROBABILITY)
print("Refusals: ", refusalCount)
print("Refusal probability: ", round(refusalProbability, 2))