import docker.docker as docker 
import os

IMAGE_NAME = "swh-graph-service"
CONTAINER_NAME = "swh-graph-service-container"
DOCKER_FILE_PATH = os.path.join(os.getcwd(), "server")
TARGET_PATH = "/root/2021-03-23-popular-3k-python/output/graph.nodes.csv"
DEST_PATH = os.path.join(os.getcwd(), "server", "files", "data", "graph.nodes.csv")


def main():
    try:
        # Build the Docker image
        res = docker.build_docker_image(IMAGE_NAME, DOCKER_FILE_PATH)
        if not res:
            raise Exception("Failed to build the Docker image.")
        else:
            # Run the container
            cmd = ["docker", "run", "-d", "-p", "5010:50091", "--name", CONTAINER_NAME, IMAGE_NAME]
            res = docker.run_docker_container(CONTAINER_NAME, cmd)
            if not res:
                raise Exception("Failed to run the Docker container.")
            else:
                # Copy the file from the container to the host
                res = docker.docker_cp(CONTAINER_NAME, TARGET_PATH, DEST_PATH)
                if not res:
                    raise Exception("Failed to copy the file from the container.")
                else:
                    with open(DEST_PATH, "r") as f:
                        lines = f.readlines()
                    
                    print("Filtering origins")
                    # Keep only origins and rewrite file
                    with open(DEST_PATH, "w") as f:
                        for line in lines:
                            if line.startswith("swh:1:ori"):
                                f.write(line)
                
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

if __name__ == '__main__':
    main()