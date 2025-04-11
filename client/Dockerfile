# To build the docker container
### docker build -t swh-graph-client .

# To run the docker container
### docker run -it --name swh-graph-client swh-graph-client

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

# COPY current app.py and controllers.py to the container
# COPY app.py /root
# COPY controllers.py /root

RUN git clone https://github.com/Fontaine44/CAPSTONE.git \
    && cd CAPSTONE/client 

# Create venv and instantiate it
RUN python3 -m venv .venv
ENV PATH="/root/.venv/bin:${PATH}"

# Install swh.graph python package
RUN pip install swh.graph grpcio

# Install all dependencies
# RUN pip install -r requirements.txt

# Default command to start the server with a specified dataset (path to be set on run)
CMD ["/bin/bash"]
# CMD ["python", "app.py"]
