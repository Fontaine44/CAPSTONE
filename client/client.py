import docker.docker as docker
import os

IMAGE_NAME = "swh-graph-client"
CONTAINER_NAME = "swh-graph-client-container"
DOCKER_FILE_PATH = os.path.join(os.getcwd(), "client")

def main():
    try:
        # Build the Docker image
        res = docker.build_docker_image(IMAGE_NAME, DOCKER_FILE_PATH)
        if not res:
            raise Exception("Failed to build the Docker image.")
        else:
            # Run the container
            cmd = ["docker", "run", "-it", "--name", CONTAINER_NAME, IMAGE_NAME]
            res = docker.run_docker_container(CONTAINER_NAME, cmd)
            if not res:
                raise Exception("Failed to run the Docker container.")
                
        while True:
            inp = input("Type 'exit' to stop the program: ")
            if inp == "exit":
                break
    except Exception as e:
        print(f"Error starting container: {e}")
    finally:
        # Stop and remove the container
        docker.stop_docker_container(CONTAINER_NAME)
        docker.remove_docker_container(CONTAINER_NAME)


if __name__ == "__main__":
    main()