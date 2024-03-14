from models import *
from random import randint, random
import matplotlib.pyplot as plt
import itertools


def dist_sqrd(A: Location, B: Location) -> float:
    return (A.lon - B.lon)**2 + (A.lat - B.lat)**2


def find_initial_centroids(points: list, cluster_size: int, n: int):
    points_pool = points.copy()
    first_point = randint(0, n-1)
    centroids = [points_pool.pop(first_point)]

    for i in range(cluster_size - 1):
        dist_to_centroid = []
        for j in range(len(points_pool)):
            dist_to_centroid.append(dist_sqrd(centroids[i], points_pool[j]))
        total_dist = sum(dist_to_centroid)
        rand_point = random() * total_dist
        for j in range(len(points_pool)):
            rand_point -= dist_to_centroid[j]
            if rand_point <= 0:
                centroids.append(points_pool.pop(j))
                break

    return centroids


def clusterize_using_kmeans(dataset: list, cluster_size: int):
    n = len(dataset)
    points = [dataset[i].mid for i in range(n)]

    centroids = find_initial_centroids(points, cluster_size, n)

    # plt.scatter([points[i].lat for i in range(n)], [points[i].lon for i in range(n)], color="blue")
    # plt.scatter([centroids[i].lat for i in range(cluster_size)], [centroids[i].lon for i in range(cluster_size)], color="red")
    # plt.show()

    clusters = [[] for _ in range(cluster_size)]

    total_dist = 0
    last_total_dist = 1000

    while abs(total_dist - last_total_dist) > 0.1:
        last_total_dist = total_dist
        total_dist = 0

        for i in range(n):
            closest_centroid = 0
            closest_centroid_dist = dist_sqrd(centroids[closest_centroid], points[i])
            total_dist += closest_centroid_dist

            for j in range(1, cluster_size):
                dist = dist_sqrd(centroids[j], points[i])
                if closest_centroid_dist > dist:
                    closest_centroid = j
                    closest_centroid_dist = dist
                total_dist += dist

            clusters[closest_centroid].append(dataset[i])

        colors = itertools.cycle(["r", "b", "g"])
        for j in range(cluster_size):
            color = next(colors)
            for i in range(len(clusters[j])):
                plt.plot([clusters[j][i].A.lat, clusters[j][i].B.lat], [clusters[j][i].A.lon, clusters[j][i].B.lon], c=color, marker='>')
        plt.scatter([centroids[i].lat for i in range(cluster_size)], [centroids[i].lon for i in range(cluster_size)], c="red", alpha=0.4)
        plt.show()

        for i in range(cluster_size):
            mean = Location()
            for j in range(len(clusters[i])):
                mean.x += clusters[i][j].mid.x
                mean.y += clusters[i][j].mid.y
            mean.x /= len(clusters[i])
            mean.y /= len(clusters[i])
            centroids[i] = mean

    return clusters

