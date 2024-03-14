from models import *
from random import random, seed
import matplotlib.pyplot as plt
import itertools

seed(7)


def run_algorithm():
    num_of_orders = 10
    orders = []
    for i in range(num_of_orders):
        orders.append(Order(Location(random() * 10, random() * 10), Location(random() * 10, random() * 10), random() * 1000))

    num_of_couriers = 3
    couriers = []
    for i in range(num_of_couriers):
        couriers.append(Courier(Location(random() * 10, random() * 10)))

    # while len(orders) > 0:
    #     courier = min(couriers, key=lambda x: x.order_dist)
    #     closest_order = 0
    #     closest_order_dist = dist(orders[0].start, courier.pos)
    #     for j in range(len(orders)):
    #         distance = dist(orders[j].start, courier.pos)
    #         if distance < closest_order_dist:
    #             closest_order = j
    #             closest_order_dist = distance
    #     courier.add_order(orders.pop(closest_order))

    dist = []
    for i in range(num_of_orders):
        for j in range(i+1, num_of_orders):
            dist.append([i, j, dist_between_orders(orders[i], orders[j])])

    dist.sort(key=lambda x: x[2])
    print(dist)

    for i in range(num_of_orders):
        plt.arrow(orders[i].start.x, orders[i].start.y, orders[i].end.x - orders[i].start.x,
                  orders[i].end.y - orders[i].start.y, width=0.05, label=i)
        plt.annotate(str(i), xy=(orders[i].start.x, orders[i].start.y))
    for i in range(num_of_couriers):
        plt.scatter(couriers[i].pos.x, couriers[i].pos.y)

    # for j in range(num_of_couriers):
    #     color = next(colors)
    #     orders = couriers[j].orders
    #     for i in range(len(orders)):
    #         plt.arrow(orders[i].start.x, orders[i].start.y, orders[i].end.x - orders[i].start.x, orders[i].end.y - orders[i].start.y, color=color, width=0.05, label=i)
    #     plt.scatter(couriers[j].pos.x, couriers[j].pos.y, color=color)
    # for i in range(num_of_orders):
    #     plt.scatter(orders[i].start.x, orders[i].start.y, label=f"${i}")
    #     plt.annotate(str(i), xy=(orders[i].start.x, orders[i].start.y))
    plt.show()


if __name__ == '__main__':
    run_algorithm()
