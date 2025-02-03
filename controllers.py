import grpc

from typing import Optional, Tuple, List
from google.protobuf import field_mask_pb2

import swh.graph.grpc.swhgraph_pb2 as swhgraph
import swh.graph.grpc.swhgraph_pb2_grpc as swhgraph_grpc

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
            print(src)
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
    # node, error = get_node("swh:1:cnt:ae0cdaa30908f360449bc5dc261dda2040e6f3ba")
    node, error = traverse(["swh:1:rev:3d1aca21a75171463e6d131a2ccfeaed7e52b19a", "swh:1:rev:cae2d26cf938e9dfe230a8d3ecd01e5db3f04176"], "rev")
    # node, error = traverse("swh:1:rev:cae2d26cf938e9dfe230a8d3ecd01e5db3f04176", "rev")
    # node, error = get_node("swh:1:rev:6c82eb89ce279f41f042f210131e8d54876087bf")
    print(node)