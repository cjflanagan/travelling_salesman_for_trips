from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import requests, json
import pandas as pd


def print_solution(manager, routing, assignment):
    """Prints assignment on console."""
    print("Objective: {} miles".format(assignment.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    assignment_index = []
    while not routing.IsEnd(index):
        place_to_visit = manager.IndexToNode(index)
        assignment_index.append(place_to_visit)
        plan_output += " {} ->".format(place_to_visit)
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += " {}\n".format(manager.IndexToNode(index))
    print(plan_output)
    print(manager.IndexToNode(index))
    plan_output += "Route distance: {}miles\n".format(route_distance)
    return assignment_index


def compute_optimal_tour(data):
    """Entry point of the program."""
    # Instantiate the data problem.

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        route = print_solution(manager, routing, assignment)
        return route
    else:
        return None
