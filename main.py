from models import *
from random import random, seed, randint, choice
import matplotlib.pyplot as plt
import itertools
from copy import deepcopy
import matplotlib._color_data as mcd

seed(7)


def calculate_distances(destinations, from_pos: Vector2):
    return [dist(from_pos, destinations[i].pos) for i in range(len(destinations))]


def index_of_min(items: list) -> int:
    min_index = 0
    min_item = items[0]
    for i in range(1, len(items)):
        if min_item > items[i]:
            min_index = i
            min_item = items[i]
    return min_index


def calculate_cluster_cost(cluster_orders: list, courier: Courier) -> int:
    orders_num = len(cluster_orders)
    if orders_num == 0:
        return 0

    current_dest = Destination(
        pos=courier.pos,
        order_id=-1,
        dest_type=Destination.type_start
    )
    available_destinations = [Destination(
        pos=cluster_orders[i].start,
        order_id=i,
        dest_type=Destination.type_start
    ) for i in range(orders_num)]
    total_dist = 0

    while len(available_destinations) > 0:
        distances = []
        for i in range(len(available_destinations)):
            destinations = available_destinations.copy()
            current_destination = destinations.pop(i)
            distance = dist(current_dest.pos, current_destination.pos)

            for _ in range(3):
                if current_destination.dest_type == Destination.type_start:
                    destinations.append(Destination(
                        pos=cluster_orders[current_destination.order_id].end,
                        order_id=current_destination.order_id,
                        dest_type=Destination.type_end
                    ))

                if len(destinations) == 0:
                    break

                local_dist = calculate_distances(destinations, current_destination.pos)
                closest_dest_index = index_of_min(local_dist)

                distance += local_dist[closest_dest_index]
                current_destination = destinations.pop(closest_dest_index)
            distances.append(distance)

        closest_dest_index = index_of_min(distances)
        total_dist += distances[closest_dest_index]
        current_dest = available_destinations.pop(closest_dest_index)
        if current_dest.dest_type == Destination.type_start:
            available_destinations.append(Destination(
                pos=cluster_orders[current_dest.order_id].end,
                order_id=current_dest.order_id,
                dest_type=Destination.type_end
            ))

    return total_dist


def annealing_schedule(t):
    T_init = 1000
    alpha = 0.99
    return T_init * alpha**t


def alter_state(orders: list, cluster_num: int) -> list:
    new_orders = deepcopy(orders)
    num_of_orders = len(orders)

    available_indices = [i for i in range(num_of_orders)]
    r_first = choice(available_indices)
    available_indices.pop(r_first)
    r_second = choice(available_indices)

    r_first_item = new_orders[r_first]
    r_second_item = new_orders[r_second]

    if r_first_item.cluster == r_second_item.cluster:
        r_first_item.cluster = randint(0, cluster_num-1)
        r_second_item.cluster = randint(0, cluster_num-1)
    else:
        temp = r_first_item.cluster
        r_first_item.cluster = r_second_item.cluster
        r_second_item.cluster = temp

    return new_orders


def calculate_total_cost(orders: list, couriers: list) -> float:
    cost = 0
    for courier in couriers:
        cluster_orders = list(filter(lambda order: order.cluster == courier.cluster_id, orders))
        cost += calculate_cluster_cost(cluster_orders, courier)

    return cost


def simulated_annealing(orders: list, couriers: list):
    t = 0
    T_final = 0.1
    current_state = orders
    current_E = calculate_total_cost(orders, couriers)
    while True:
        T = annealing_schedule(t)
        if T < T_final:
            return current_state

        candidate = alter_state(orders, len(couriers))
        E = calculate_total_cost(candidate, couriers)
        dE = current_E - E
        if dE > 0:
            current_state = candidate
            current_E = E
        else:
            p = math.exp(dE/T)
            if random() < p:
                current_state = candidate
                current_E = E

        t += 1
        print(f"Total cost is: {E}")


def plot(orders: list, couriers: list, filename: str):
    num_of_couriers = len(couriers)
    num_of_orders = len(orders)
    palette = list(mcd.XKCD_COLORS.values())[::num_of_couriers]
    for i in range(num_of_orders):
        plt.arrow(orders[i].start.x, orders[i].start.y,
                  orders[i].end.x - orders[i].start.x,
                  orders[i].end.y - orders[i].start.y, width=0.05, label=i,
                  color=palette[orders[i].cluster])
        plt.annotate(str(i), xy=(orders[i].start.x, orders[i].start.y))
    for i in range(num_of_couriers):
        plt.scatter(couriers[i].pos.x, couriers[i].pos.y, color=palette[i])
    plt.savefig(f"{filename}.png")


def run_algorithm():
    num_of_orders = 10
    num_of_couriers = 3

    orders = []
    for i in range(num_of_orders):
        orders.append(
            Order(Vector2(random() * 10, random() * 10), Vector2(random() * 10, random() * 10), randint(0, num_of_couriers - 1)))

    couriers = []
    for i in range(num_of_couriers):
        couriers.append(Courier(Vector2(random() * 10, random() * 10), i))

    plot(orders, couriers, "initial")
    optimal_orders = simulated_annealing(orders, couriers)

    plot(optimal_orders, couriers, "optimal")

    # for cluster in clusters:
    #     print(cluster.orders)
    #     print(f"Total cost: {calculate_cluster_cost(cluster)}")


if __name__ == '__main__':
    run_algorithm()
