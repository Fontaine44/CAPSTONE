import controllers as cc
from flask import Flask, jsonify, request
import base64

app = Flask(__name__)

@app.route("/node/<swhid>", methods=["GET"])
def get_node_route(swhid: str):
    """
    Fetches a node from the gRPC server and returns the result as a JSON response.
    """
    try:
        response, error = cc.get_node(swhid)
        if error:
            return jsonify({"error": error}), 500
        if response is None:
            return jsonify({"error": "Node not found"}), 404
        # Convert the response to a dictionary if needed
        print(response)
        print(dir(response))
        print(response.cnt)
        print("------------------")
        serialized_data = response.SerializeToString()
        encoded_data = base64.b64encode(serialized_data).decode('utf-8')
        return jsonify({
            "data": encoded_data,  # Replace with response fields if needed
        }), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

@app.route("/stats", methods=["GET"])
def get_stats_route():
    """
    Fetches statistics from the gRPC server and returns the result as a JSON response.
    """
    try:
        response, error = cc.get_stats()
        if error:
            return jsonify({"error": error}), 500
        if response is None:
            return jsonify({"error": "Stats not found"}), 404
        # Convert the response to a dictionary if needed
        return jsonify({
            "stats": response,  # Replace with response fields if needed
        }), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500


# with grpc.insecure_channel(GRAPH_GRPC_SERVER) as channel:
#     stub = swhgraph_grpc.TraversalServiceStub(channel)
#     response = stub.Stats(swhgraph.StatsRequest())
#     print(response)
#     print("Compression ratio:", response.compression_ratio * 100, "%")

# Main entry point
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)