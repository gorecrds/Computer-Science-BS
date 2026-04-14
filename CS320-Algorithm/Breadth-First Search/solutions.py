"""Breadth-first search lab 7 implementation assignment."""

from tokenize import group

from edgegraph import VertexEL, EdgeEL, GraphEL


def _validate_args(graph, start):
    """ Check Arguments for BFS """
    if graph is None or start is None:
        raise ValueError("Invalid graph or vertex")

    if start not in graph.vertices():  # check if start vertex is in graph
        return False
    return True


def bfs(graph: GraphEL, start: VertexEL) -> list:
    """Performs a breadth-first search from given vertex """
    check = _validate_args(graph, start)
    if not check:
        return []
    lot = []  # tuples to return
    visited = set()  # track visited
    queue = [start]  # queue for bfs

    visited.add(start)  # adds the first vertex to visited

    while queue:
        lot.append(tuple(queue))  # add the current group to the list of tuples
        next_queue = []  # queue for the next level
        for item in queue:  # loop throught the current queue
            for adjacent in graph.adjacent(item):  # loop through adjacent vertices
                #  if adjacent vertex is not visited, add to next queue and to visited
                if adjacent not in visited:
                    next_queue.append(adjacent)
                    visited.add(adjacent)
        queue = next_queue
    return lot


if __name__ == "__main__":
    test_graph = GraphEL()

    # create vertices
    vA = VertexEL("A")
    vB = VertexEL("B")
    vC = VertexEL("C")
    vD = VertexEL("D")
    vE = VertexEL("E")
    vF = VertexEL("F")
    vG = VertexEL("G")

    # create edges
    e1 = EdgeEL("1", vA, vB)
    e2 = EdgeEL("2", vA, vC)
    e3 = EdgeEL("3", vA, vD)
    e4 = EdgeEL("4", vC, vE)
    e5 = EdgeEL("5", vD, vF)

    # add edges to graph
    test_graph.add_edge(e1)
    test_graph.add_edge(e2)
    test_graph.add_edge(e3)
    test_graph.add_edge(e4)
    test_graph.add_edge(e5)
    test_graph.add_vertex(vG)
    print(test_graph)  # print the graph structure
    print(bfs(test_graph, vA))
