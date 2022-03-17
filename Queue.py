class Queue():
 
    # Constructor method
    def __init__(self):
        self.head = 0
        self.tail = 0
        self.items = []
        self.maxSize = 20

    #Enqueue Method
    def enQueue(self, itemsToAdd):
        if self.isFull():
            return "Queue is full,"
        else:
            self.tail += 1
            self.items.append(itemsToAdd)

    def deQueue(self):
        if self.isEmpty():
            return "Queue is isEmpty"
        else:
            itemsToRemove = self.items[self.head]
            self.head += 1
            return itemsToRemove

    def showQueue(self):
        print(self.items[self.head:self.tail + 1])

    def isFull(self):
        return len(self.items[self.head:self.tail + 1]) >= self.maxSize

    def isEmpty(self):
        return self.head == self.tail

    def findTotal(self):
        if self.isEmpty():
            return "Queue is empty"
        currentQueue = (self.items[self.head:self.tail + 1])
        total = sum(currentQueue)
        return total

    def Peek(self):
        if self.isEmpty():
            return "Queue is empty"
        return self.items[self.head]
