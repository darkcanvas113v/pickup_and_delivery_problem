import matplotlib._color_data as mcd
import matplotlib.pyplot as plt


def plot_clusters(orders: list, couriers: list, filename: str):
    num_of_couriers = len(couriers)
    num_of_orders = len(orders)
    palette = list(mcd.XKCD_COLORS.values())

    for i in range(num_of_orders):
        plt.arrow(orders[i].start.x, orders[i].start.y,
                  orders[i].end.x - orders[i].start.x,
                  orders[i].end.y - orders[i].start.y, width=0.05,
                  color=palette[int(orders[i].cluster / num_of_couriers * len(palette))])
        plt.annotate(str(i), xy=(orders[i].start.x, orders[i].start.y))
    for i in range(num_of_couriers):
        plt.scatter(couriers[i].pos.x, couriers[i].pos.y, color=palette[int(i / num_of_couriers * len(palette))])
    plt.savefig(f"{filename}.png")
    plt.clf()


def plot_routes(routes: list):
    palette = list(mcd.XKCD_COLORS.values())

    for k in range(len(routes)):
        route = routes[k]
        last_pos = route[0]
        plt.scatter(last_pos.x, last_pos.y, color=palette[int(k / len(routes) * len(palette))])
        for i in range(1, len(route)):
            plt.arrow(last_pos.x, last_pos.y,
                      route[i].x - last_pos.x,
                      route[i].y - last_pos.y, width=0.05,
                      color=palette[int(k / len(routes) * len(palette))])
            last_pos = route[i]
    plt.savefig(f"routes.png")
    plt.clf()
