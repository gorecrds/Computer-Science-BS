from functools import partial
from util import cost, best_path
import two_opt


def _check_arg(initial_population, distances, generations):
    if initial_population is None:
        raise ValueError("Invalid argument")
    if distances is None:
        raise ValueError("Invalid argument")
    if generations is None:
        raise ValueError("Invalid argument")
    if generations <= 0:
        raise ValueError("Invalid argument")


def crossover(route_a, route_b):
    """ Create a new_route path by combining parts of two route paths. """
    new_route = list(route_a[:mid(route_a)])  # first half of route_a
    # append to new_route any missing city from route_b skipping items present in new_route
    for city in route_b:
        if city not in new_route:
            new_route.append(city)
    return tuple(new_route)


def mid(arg) -> int:
    """Return the middle index of an argument ."""
    return len(arg) // 2


def ga_tsp(initial_population, distances, generations):
    """ Genetic algorithm for TSP that returns the best travel route available """
    _check_arg(initial_population, distances, generations)  # check for valid arguments
    routes = initial_population  # initialize routes
    # evolve routes from a number of generations
    for i in range(generations):
        # sort routes based on the cost of the path
        routes = sorted(routes, key=partial(cost, distances=distances))
        picked_routes = routes[:mid(routes)]  # assign the top half of the populatio
        new_routes = []
        index = 0
        while len(new_routes) < len(routes):
            #  assign route_a from picked_routes based on the index
            route_a = picked_routes[index]
            # assign the next route as route_b in a wrap around manner
            route_b = picked_routes[(index + 1) % len(picked_routes)]
            # create a new_route by combining route_a and route_b
            new_route = crossover(route_a, route_b)
            # optimize the new_route using two_opt
            new_route = two_opt.two_opt(new_route, distances)
            new_routes.append(new_route)  # append the new_route to new_routes
            index = len(new_routes) % len(picked_routes)
        # Replace the old routes with the new routes sorting it by total distance.
        routes = sorted(new_routes, key=partial(cost, distances=distances))
    return best_path(routes, distances)  # return the best lowest route from routes
