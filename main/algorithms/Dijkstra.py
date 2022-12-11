import pygame
from queue import PriorityQueue, Queue
from .RP import reconstruct_path
from .RP import get_unvisited_nodes

"""
Algorithm

for each vertex in graph:
    distance[vertex] = inf
    if vertex != start, add vertex to Priority Queue (unvisited nodes)
distance[start] = 0

while the queue is not empty:
    U = min from queue
    for each unvisited neighbor vertex of U
        tempDistance = distance[U] + edge_weight(U, vertex)
        if tempDistance < distance[vertex]:
            distance[vertex] = tempDistance
            previous[vertex] = U

"""

# TODO: Refactor using a priority queue
# Make distance a priority queue (node, inf)
def dijkstra(draw, start, end):
    # Stores all nodes connected to start
    unvisited_nodes = get_unvisited_nodes(start)

    # Set up the node values
    distance = {node: float("inf") for node in unvisited_nodes}
    distance[start] = 0

    # Holds the path from start to end
    previous = {}

    run = True

    while unvisited_nodes and run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                run = False

        # Choose node with smallest distance
        current_min = min(unvisited_nodes, key=distance.get)

        # Ends the search once the end is reached
        # May add a toggle for this
        if current_min == end:
            break

        for neighbor in current_min.neighbors:
            # Don't recheck for performance
            if not neighbor.is_checked():
                if not neighbor.is_start() and not neighbor.is_end():
                    neighbor.uncheck()
                # edges between vertecies are not weighted
                # (using constant weight of 1)
                temp_value = distance[current_min] + 1
                if temp_value < distance[neighbor]:
                    distance[neighbor] = temp_value
                    previous[neighbor] = current_min

                draw()

                if not neighbor.is_start() and not neighbor.is_end():
                    neighbor.check()

        unvisited_nodes.remove(current_min)

    reconstruct_path(previous, end, draw)
