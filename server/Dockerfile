# To build the docker container
### docker build -t swh-graph-service .

# To run the docker container
### docker run -p 5009:5009 -it swh-graph-service

# To run inside the container
### swh graph rpc-serve -g compressed/graph

FROM debian:latest

# Install dependencies
RUN apt update && apt install -y \
    build-essential \
    libclang-dev \
    python3 \
    python3-dev \
    python3-venv \
    libpq-dev \
    default-jre \
    zstd \
    protobuf-compiler \
    curl \
    git \
    libssl-dev \
    pkg-config \
    openssl \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

WORKDIR /root

# Set environment variables for Rust
ENV PATH="/root/.cargo/bin:${PATH}"

# Install swh.graph grpc server
RUN RUSTFLAGS="-C target-cpu=native" cargo install --git https://gitlab.softwareheritage.org/swh/devel/swh-graph.git swh-graph-grpc-server

# Create venv and instantiate it
RUN python3 -m venv .venv
ENV PATH="/root/.venv/bin:${PATH}"

# Install swh.graph python package
RUN pip install swh.graph

# Download dataset
RUN swh graph download --name 2021-03-23-popular-3k-python 2021-03-23-popular-3k-python/compressed

# Switch to the graph directory
WORKDIR /root/2021-03-23-popular-3k-python

# Reindex the dataset
RUN RUSTFLAGS="-C target-cpu=native" cargo install swh-graph
RUN swh graph reindex compressed/graph

# Regenerate .ef files
RUN RUSTFLAGS="-C target-cpu=native" cargo install swh-graph
RUN swh graph reindex --ef compressed/graph

# Create the /output directory
RUN mkdir -p /root/2021-03-23-popular-3k-python/output

# Decompress the ids
RUN zstd -d /root/2021-03-23-popular-3k-python/compressed/graph.nodes.csv.zst -o /root/2021-03-23-popular-3k-python/output/graph.nodes.csv

# Start the server
# RUN swh graph rpc-serve -g compressed/graph

# Expose the API server port
EXPOSE 5009
EXPOSE 50091

# Default command to start the server with a specified dataset (path to be set on run)
CMD ["swh", "graph", "grpc-serve", "-g", "compressed/graph"]
# CMD ["/bin/bash"]
