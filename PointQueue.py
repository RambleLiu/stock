import BaseTool as tool


class Node:
    data = None
    next = None
    pre = None
    date = None


# 链式队列,出队后数据仍然保留，仅front移动
class PointQueue:
    # 队首指针
    front = Node()
    # 队尾指针
    rear = front
    # 队列长度
    length = 0

    # 入队
    def enQueue(self, data, date):
        node = Node()
        node.data = data
        node.date = date
        node.pre = self.rear
        self.rear.next = node
        self.rear = node
        self.length += 1

    # 出队,出队需要判空
    def deQueue(self):
        if self.isEmpty():
            return None
        rs = self.front.next
        self.front = self.front.next
        self.length -= 1
        return rs

    def first(self):
        if self.isEmpty():
            return None
        return self.front.next

    def isEmpty(self):
        return self.length == 0

    def _len_(self):
        return self.length

    # 队列对齐
    def align(self, tar):
        if self.isEmpty() or tar.isEmpty() or self.first().date is None or tar.first().date is None:
            return None

        # 如果本队列比目标队列建立更早，则将本队列出队，直到两个队列开始时间相同
        while tool.compare_time(self.first().date, tar.first().date) < 0:
            self.deQueue()
        # 如果目标队列建立时间更早，则将目标队列出队
        while tool.compare_time(self.first().date, tar.first().date) < 0:
            tar.deQueue()

    def preData(self):
        return self.front.data