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

# COPY current directory to the container
# COPY . .

# Set environment variables for Rust
ENV PATH="/root/.cargo/bin:${PATH}"

# Install swh.graph grpc server
# RUN RUSTFLAGS="-C target-cpu=native" cargo install --git https://gitlab.softwareheritage.org/swh/devel/swh-graph.git swh-graph-grpc-server

# Create venv and instantiate it
RUN python3 -m venv .venv
ENV PATH="/root/.venv/bin:${PATH}"

# Install swh.graph python package
RUN pip install swh.graph grpcio

# Default command to start the server with a specified dataset (path to be set on run)
CMD ["/bin/bash"]
