from numpy.random import uniform


class TimeGenerator:
  def __init__(self, time, delta):
    self.time = time
    self.delta = delta

  def randomTime(self):
    return uniform(self.time - self.delta, self.time + self.delta)

class RequestGenerator:
  def __init__(self, timeGenerator, count):
    self.generator = timeGenerator
    self.requestCount = count
    self.receivers = []
    self.next = 0

  def generateRequest(self):
    self.requestCount -= 1
    for receiver in self.receivers:
      if receiver.receiveRequest(): return receiver
    return None

  def delay(self):
    return self.generator.randomTime()

class RequestProcessor:
  def __init__(self, generator, maxQueueSize=1):
    self.generator = generator
    self.queue, self.received, self.maxQueue, self.processed = 0, 0, maxQueueSize, 0
    self.next = 0

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
    return self.generator.randomTime()

class Model:
  def __init__(self, generator, operators, computers):
    self.generator = generator
    self.operators = operators
    self.computers = computers

  def simulate(self):
    refusalCount = 0
    generatedRequests = self.generator.requestCount
    generator = self.generator

    generator.receivers = self.operators
    self.operators[0].receivers = [self.computers[0]]
    self.operators[1].receivers = [self.computers[0]]
    self.operators[2].receivers = [self.computers[1]]

    generator.next = generator.delay()
    self.operators[0].next = self.operators[0].delay()

    blocks = [generator, self.operators[0], self.operators[1], self.operators[2], self.computers[0], self.computers[1]]

    while generator.requestCount >= 0:
      currTime = generator.next
      for block in blocks:
        if 0 < block.next < currTime: currTime = block.next

      for block in blocks:
        if currTime == block.next:
          if isinstance(block, RequestGenerator):
            nextGenerator = generator.generateRequest()
            if nextGenerator is not None: nextGenerator.next = currTime + nextGenerator.delay()
            else: refusalCount += 1
            generator.next = currTime + generator.delay()
          elif isinstance(block, RequestProcessor):
            block.processRequest()
            if block.queue == 0: block.next = 0
            else: block.next = currTime + block.delay()

    return { "refusalProbability": refusalCount / generatedRequests, "refusalCount": refusalCount }

clientCount = 300

generator = RequestGenerator(TimeGenerator(10, 2), clientCount)
operators = [RequestProcessor(TimeGenerator(20, 5)), RequestProcessor(TimeGenerator(40, 10)), RequestProcessor(TimeGenerator(40, 20))]
computers = [RequestProcessor(TimeGenerator(15, 0)), RequestProcessor(TimeGenerator(30, 0))]

model = Model(generator, operators, computers)
result = model.simulate()

refusalCount, refusalProbability = result["refusalCount"], result["refusalProbability"]

print("Refusals: ", refusalCount)
print("Refusal probability: ", round(refusalProbability, 2))