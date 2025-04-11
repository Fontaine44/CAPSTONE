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
    vim \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

WORKDIR /root

# Clone repository
RUN git clone https://github.com/Fontaine44/CAPSTONE.git

# Set working directory
WORKDIR /root/CAPSTONE/client

# Create venv and instantiate it
RUN python3 -m venv .venv

# Activate venv
ENV PATH="/root/CAPSTONE/client/.venv/bin:$PATH"

# Install all dependencies
RUN pip install -r requirements.txt

# Default command to start the server with a specified dataset (path to be set on run)
CMD ["/bin/bash"]
# CMD ["python", "app.py"]
