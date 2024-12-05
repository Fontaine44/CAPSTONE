import grpc

import swh.graph.grpc.swhgraph_pb2 as swhgraph
import swh.graph.grpc.swhgraph_pb2_grpc as swhgraph_grpc

GRAPH_GRPC_SERVER = "host.docker.internal:5010"
GRAPH_GRPC_SERVER = "192.168.65.254:5010"
# GRAPH_GRPC_SERVER = "10.0.0.198:5002"

with grpc.insecure_channel(GRAPH_GRPC_SERVER) as channel:
    stub = swhgraph_grpc.TraversalServiceStub(channel)
    response = stub.Stats(swhgraph.StatsRequest())
    print(response)
    print("Compression ratio:", response.compression_ratio * 100, "%")