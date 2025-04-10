import grpc

from typing import Optional, Tuple

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