import math


class Vector2:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def copy(self):
        return Vector2(self.x, self.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Order:
    def __init__(self, start: Vector2, end: Vector2, cluster: int):
        self.start = start
        self.end = end
        self.length = math.dist([start.x, start.y], [end.x, end.y])
        self.mid = Vector2((start.x + end.x) / 2, (start.y + end.y) / 2)
        self.cluster = cluster

    def __repr__(self):
        return f"A = ({self.start}, B = {self.end})"

    def __copy__(self):
        return Order(
            start=self.start,
            end=self.end,
            cluster=self.cluster
        )


def dist(A: Vector2, B: Vector2) -> float:
    return math.dist([A.x, A.y], [B.x, B.y])


def dist_between_orders(first: Order, second: Order):
    return min(
        dist(first.start, second.start) + dist(second.start, first.end) + dist(first.end, second.end),
        dist(first.start, second.start) + second.length + dist(second.end, first.end),
        first.length + dist(first.end, second.start) + second.length,
        dist(second.start, first.start) + dist(first.start, second.end) + dist(second.end, first.end),
        dist(second.start, first.start) + first.length + dist(first.end, second.end),
        second.length + dist(second.end, first.start) + first.length,
    ) - max(first.length, second.length)


class Courier:
    def __init__(self, pos: Vector2, cluster_id: int):
        self.pos = pos
        self.orders = []
        self.order_dist = 0
        self.cluster_id = cluster_id

    def add_order(self, order: Order):
        self.orders.append(order)
        if len(self.orders) == 0:
            self.order_dist = order.length + dist(self.pos, order.start)
            return

        min_dist = dist_between_orders(order, self.orders[0])
        for i in range(1, len(self.orders)):
            distance = dist_between_orders(order, self.orders[i])
            if distance < min_dist:
                min_dist = distance
        self.order_dist += min_dist


class Destination:
    type_start = "s"
    type_end = "e"

    def __init__(self, pos: Vector2, order_id: int, dest_type: str):
        self.pos = pos
        self.dest_type = dest_type
        self.order_id = order_id
