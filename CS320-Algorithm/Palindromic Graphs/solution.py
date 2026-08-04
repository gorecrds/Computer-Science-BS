def pld_graph(graph) -> list:
    """
    returns a list of tuples of all the palindromes 
    found after traversing all the paths in the graph
    """
    if graph is None:
        raise ValueError("Bad graph")  # raise value error if graph is None

    edges = graph.edges()
    result = set()

    if len(edges) == 0:  # if no edges, return empty list
        return []

    # Count occurrences for each edge
    count = {}
    for edge in edges:
        value = edge.get_value()
        count[value] = count.get(value, 0) + 1

    for edge in edges:  # iterate through edges
        value = edge.get_value()
        # if there is only one occurence, skip it since it cannot be an endpoint
        if count[value] == 1:
            continue

        v1, v2 = edge.ends()  # get vertex endpoints
        # Each path stores the current vertex, used edges, and path values
        paths = [(v1, {edge}, [value]), (v2, {edge}, [value])]
        # Keep looking while there are still paths to check
        while len(paths) > 0:
            current_vertex, used_edges, path_values = paths.pop()  # Pop the last path to explore
            # add to result if path values has at least 3 values and is a palindrome
            if len(path_values) >= 3 and path_values == path_values[::-1]:
                result.add(tuple(path_values))
            # Explore adjacent edges
            for next_edge in graph.incident(current_vertex):
                if next_edge not in used_edges:  # if edge not used in current path
                    next_ends = next_edge.ends()  # get next vertex endpoints

                    # if curent vertex matches first endpoint, next vertex
                    # is second endpoint, otherwise next vertex is first endpoint
                    if current_vertex == next_ends[0]:
                        next_vertex = next_ends[1]
                    else:
                        next_vertex = next_ends[0]
                    # update used edge and path values fo rnext path
                    next_used_edges = set(used_edges)
                    next_used_edges.add(next_edge)
                    next_path_values = path_values + [next_edge.get_value()]
                    # append new path to paths
                    paths.append((next_vertex, next_used_edges, next_path_values))
    return sorted(result)


if __name__ == "__main__":
    # test run code
    from edgegraph import parse_graph_file
    graph_file = parse_graph_file(r".\Palindromic Graphs\graph.txt")
    print(pld_graph(graph_file))
