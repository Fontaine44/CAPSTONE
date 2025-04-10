import grpc

from typing import Optional, Tuple, List

import swh.graph.grpc.swhgraph_pb2 as swhgraph
import swh.graph.grpc.swhgraph_pb2_grpc as swhgraph_grpc

import os

GRAPH_GRPC_SERVER = "host.docker.internal:5010"

def get_node(swhid: str) -> Tuple[Optional[swhgraph.GetNodeRequest], Optional[str]]:
    """
    Fetches a node from the gRPC server.

    Args:
        swhid (str): The identifier of the node to fetch.

    Returns:
        Tuple[Optional[swhgraph.GetNodeResponse], Optional[str]]:
        - The node response if successful, None otherwise.
        - An error message if an error occurs, None otherwise.
    """
    try:
        with grpc.insecure_channel(GRAPH_GRPC_SERVER) as channel:
            stub = swhgraph_grpc.TraversalServiceStub(channel)
            try:
                response = stub.GetNode(swhgraph.GetNodeRequest(swhid=swhid))
                return response, None
            except grpc.RpcError as e:
                error_msg = f"gRPC request failed: {e.details()} (Code: {e.code()})"
                return None, error_msg
            except Exception as e:
                error_msg = f"Unexpected error during stub.GetNode: {e}"
                return None, error_msg
    except grpc.RpcError as e:
        error_msg = f"Failed to connect to gRPC server: {e.details()} (Code: {e.code()})"
        return None, error_msg
    except Exception as e:
        error_msg = f"Unexpected error during channel setup: {e}"
        return None, error_msg

def get_stats() -> Tuple[Optional[swhgraph.StatsResponse], Optional[str]]:
    """
    Fetches statistics from the gRPC server.

    Returns:
        Tuple[Optional[swhgraph.StatsResponse], Optional[str]]:
        - The stats response if successful, None otherwise.
        - An error message if an error occurs, None otherwise.
    """
    try:
        with grpc.insecure_channel(GRAPH_GRPC_SERVER) as channel:
            stub = swhgraph_grpc.TraversalServiceStub(channel)
            try:
                response = stub.Stats(swhgraph.StatsRequest())
                return response, None
            except grpc.RpcError as e:
                error_msg = f"gRPC request failed: {e.details()} (Code: {e.code()})"
                return None, error_msg
            except Exception as e:
                error_msg = f"Unexpected error during stub.Stats: {e}"
                return None, error_msg
    except grpc.RpcError as e:
        error_msg = f"Failed to connect to gRPC server: {e.details()} (Code: {e.code()})"
        return None, error_msg
    except Exception as e:
        error_msg = f"Unexpected error during channel setup: {e}"
        return None, error_msg

def traverse(src: List[str], node_filter: Optional[str] = None) -> Tuple[Optional[List[swhgraph.Node]], Optional[str]]:
    """
    Traverses the graph starting from the given source node with an optional node filter.

    Args:
        src (str): The identifier of the source node to start the traversal from.
        node_filter (Optional[str]): The type of nodes to return (e.g., "ori"). Defaults to None.

    Returns:
        Tuple[Optional[List[swhgraph.Node]], Optional[str]]:
        - A list of nodes encountered during traversal if successful, None otherwise.
        - An error message if an error occurs, None otherwise.
    """
    try:
        with grpc.insecure_channel(GRAPH_GRPC_SERVER) as channel:
            stub = swhgraph_grpc.TraversalServiceStub(channel)
            try:
                # Construct the TraversalRequest with optional node filter
                if node_filter:
                  request = swhgraph.TraversalRequest(
                      src=src,
                      return_nodes=swhgraph.NodeFilter(types=node_filter)
                  )
                else:
                  request = swhgraph.TraversalRequest(
                      src=src
                  )
                
                # Call the Traverse method and collect the streamed responses
                response_stream = stub.Traverse(request)
                nodes = list(response_stream)  # Collect all nodes from the stream
                return nodes, None
            except grpc.RpcError as e:
                error_msg = f"gRPC request failed: {e.details()} (Code: {e.code()})"
                return None, error_msg
            except Exception as e:
                error_msg = f"Unexpected error during stub.Traverse: {e}"
                return None, error_msg
    except grpc.RpcError as e:
        error_msg = f"Failed to connect to gRPC server: {e.details()} (Code: {e.code()})"
        return None, error_msg
    except Exception as e:
        error_msg = f"Unexpected error during channel setup: {e}"
        return None, error_msg


if __name__ == "__main__":
    
    while True:
        inp = input("Enter swhid: ")
        if inp == "exit":
            break
        if inp == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        node, error = get_node(inp)
        # node, error = traverse([inp], "dir")
        if error:
            print(f"Error: {error}")
        else:
            print(node)
        print("=====================================")
    
    # node, error = get_node("swh:1:ori:006762b49f6052c9648a93fabcddeb68c90d2382")      # voila repo
    # node, error = get_node("swh:1:snp:b92523aa95ddd89735f4bb0d3017ebc009fc0c68")
    # node, error = traverse(["swh:1:rev:cae2d26cf938e9dfe230a8d3ecd01e5db3f04176"], "rev")
    # node, error = traverse(["swh:1:rev:9d09aa1b405c14b67673d1dd067606b208293b7c"], "rev")
    # node, error = get_node("swh:1:ori:0089824c1a5fc9ae7a9993bf7b7db33474472980")
    # node, error = get_node("swh:1:ori:dfc18ea9691caf7b0692a93b21d20a9504d5a9a2")      # Pypi repo
    # node, error = get_node("swh:1:ori:00a082063e1572f77e21b9dedef30635e60a99e8")        # crashing repo
    # print(node)