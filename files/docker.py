import subprocess
import os

IMAGE_NAME = "swh-graph-service"
CONTAINER_NAME = "swh-graph-container"
TARGET_PATH = "/root/2021-03-23-popular-3k-python/output/graph.nodes.csv"
DEST_PATH = os.path.join(os.getcwd(), "files", "data", "graph.nodes.csv")

# Function to check if image exists already
def check_docker_image_exists(image_name):
    try:
        # Run the docker images command and get the output
        result = subprocess.run(['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}'],
                                capture_output=True, text=True, check=True)

        # Split the output into a list of image names and tags
        images = result.stdout.splitlines()
        
        # Check if the base image name exists in the list of images
        for image in images:
            # Split the repository and tag from the image
            repo, tag = image.split(":")
            
            # Check if the repository matches the base image name
            if repo == image_name:
                return True  # Image exists
        return False  # Image does not exist

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return False
    
# Function to build the Docker image
def build_docker_image(image_name):
    try:
        # Build the Docker image
        if check_docker_image_exists(image_name):
            print(f"Image '{image_name}' already exists.")
            return True
        subprocess.run(["docker", "build", "-t", image_name, "."], check=True)
        print(f"Image '{image_name}' built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building image: {e}")
        return False
    return True

# Function to run the Docker container
def run_docker_container(image_name, container_name):
    try:
        # Run the container with interactive mode
        subprocess.run(["docker", "run", "-d", "-p", "5009:5009", "--name", container_name, image_name], check=True)
        print(f"Container '{container_name}' started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running container: {e}")
        return False
    return True

# Function to copy files from the container to the host
def docker_cp(container_name, container_path, host_path):
    try:
        # Perform docker cp command
        subprocess.run(["docker", "cp", f"{container_name}:{container_path}", host_path], check=True)
        print(f"Copied file from container '{container_name}' to '{host_path}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error copying file: {e}")
        return False
    return True

# Function to gracefully stop the container
def stop_docker_container(container_name, timeout=10):
    try:
        # Gracefully stop the container by sending SIGTERM (with a timeout)
        subprocess.run(["docker", "stop", "-t", str(timeout), container_name], check=True)
        print(f"Container '{container_name}' stopped gracefully.")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping container: {e}")
        return False
    return True

# Function to remove the container
def remove_docker_container(container_name):
    try:
        # Force remove the container
        subprocess.run(["docker", "rm", "-f", container_name], check=True)
        print(f"Container '{container_name}' removed.")
    except subprocess.CalledProcessError as e:
        print(f"Error removing container: {e}")
        return False
    return True

def run_container():
    try:
        # Ensure the 'data' directory exists
        os.makedirs(os.path.dirname(DEST_PATH), exist_ok=True)

        # Build the Docker image
        if build_docker_image(IMAGE_NAME):
            # Run the container
            if run_docker_container(IMAGE_NAME, CONTAINER_NAME):
                # Copy the file from the container to the host
                docker_cp(CONTAINER_NAME, TARGET_PATH, DEST_PATH)
    except Exception as e:
        print(f"Error starting container: {e}")
    finally:
        # Stop and remove the container
        stop_docker_container(CONTAINER_NAME)
        remove_docker_container(CONTAINER_NAME)

if __name__ == "__main__":
    print("hi")