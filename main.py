from models import *
from visualization import *
from random import random, seed, randint, choice
from copy import deepcopy

import time

T_init = 10
depth = 3


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


def calculate_cluster_cost(cluster_orders: list, courier: Courier):
    orders_num = len(cluster_orders)
    route = [courier.pos]
    if orders_num == 0:
        return 0, route

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
    total_dist = 0.0

    while len(available_destinations) > 0:
        distances = []
        for i in range(len(available_destinations)):
            destinations = available_destinations.copy()
            current_destination = destinations.pop(i)
            distance = dist(current_dest.pos, current_destination.pos)

            for _ in range(depth):
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
        route.append(available_destinations[closest_dest_index].pos)
        total_dist += dist(current_dest.pos, available_destinations[closest_dest_index].pos)
        current_dest = available_destinations.pop(closest_dest_index)
        if current_dest.dest_type == Destination.type_start:
            available_destinations.append(Destination(
                pos=cluster_orders[current_dest.order_id].end,
                order_id=current_dest.order_id,
                dest_type=Destination.type_end
            ))

    return total_dist, route


# Функция для определения температуры T.
def annealing_schedule(t):
    alpha = 0.98
    return T_init * alpha**t


# Функция для изменения состояния. Выбирает рандомное количество точек и добавляет их к случайному кластеру.
def alter_state(orders: list, cluster_num: int, T: float) -> list:
    new_orders = deepcopy(orders)
    num_of_orders = len(orders)

    num_of_orders_to_alter = randint(1, max(int(num_of_orders * T/T_init), 1))
    # num_of_orders_to_alter = randint(1, num_of_orders-1)

    available_indices = [i for i in range(num_of_orders)]

    for i in range(num_of_orders_to_alter):
        r_order_index = choice(available_indices)
        available_indices.remove(r_order_index)

        r_order = new_orders[r_order_index]
        r_order.cluster = randint(0, cluster_num - 1)

    return new_orders


def calculate_total_cost(orders: list, couriers: list):
    costs = []
    routes = []
    for courier in couriers:
        cluster_orders = list(filter(lambda order: order.cluster == courier.cluster_id, orders))
        (cost, route) = calculate_cluster_cost(cluster_orders, courier)
        costs.append(cost)
        routes.append(route)

    return max(costs), routes


def simulated_annealing(orders: list, couriers: list):
    t = 0
    T_final = 0.1
    current_state = orders
    current_E, global_min_routes = calculate_total_cost(orders, couriers)

    global_min = current_E
    global_min_state = current_state
    while True:
        T = annealing_schedule(t)
        if T < T_final:
            return global_min, global_min_state, global_min_routes

        candidate = alter_state(current_state, len(couriers), T)
        (E, routes) = calculate_total_cost(candidate, couriers)
        dE = current_E - E

        if E < global_min:
            global_min = E
            global_min_state = candidate
            global_min_routes = routes

        if dE > 0:
            current_state = candidate
            current_E = E
            print(f"New state with cost: {E}")
        else:
            p = math.exp(dE/T)
            if random() < p:
                current_state = candidate
                current_E = E
                print(f"New state with cost: {E}")

        t += 1
        print(f"Temperature is: {T}")


def run_algorithm(num_of_orders=100, num_of_couriers=10, initialization_seed=2, num_of_independent_runs=4, NNsearch_depth=3):
    global depth
    depth = NNsearch_depth

    seed(initialization_seed)


    orders = []
    for i in range(num_of_orders):
        orders.append(
            Order(Vector2(random() * 10, random() * 10), Vector2(random() * 10, random() * 10), randint(0, num_of_couriers - 1)))

    couriers = []
    for i in range(num_of_couriers):
        couriers.append(Courier(Vector2(random() * 10, random() * 10), i))

    seed(time.time())

    plot_clusters(orders, couriers, "initial")

    timestamp = time.time_ns()

    best_dist, best_orders, best_routes = simulated_annealing(orders, couriers)
    for _ in range(1, num_of_independent_runs):
        (optimal_dist, optimal_orders, optimal_routes) = simulated_annealing(orders, couriers)
        if optimal_dist < best_dist:
            best_dist = optimal_dist
            best_orders = optimal_orders
            best_routes = optimal_routes

    print(f"\nCalculation time: {(time.time_ns() - timestamp) / 1_000_000_000} seconds")
    print(f"Distance of the longest courier route: {best_dist}")

    plot_clusters(best_orders, couriers, "optimal")
    plot_routes(best_routes)


if __name__ == '__main__':
    run_algorithm()
