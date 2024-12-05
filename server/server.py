from files.docker import *
# from files.http_requests import *

def print_line_break():
    print("-"*20)

def main():
    try:
        # Ensure the 'data' directory exists
        # os.makedirs(os.path.dirname(DEST_PATH), exist_ok=True)

        # Build the Docker image
        if build_docker_image(IMAGE_NAME):
            # Run the container
            if run_docker_container(IMAGE_NAME, CONTAINER_NAME):
                # Copy the file from the container to the host
                docker_cp(CONTAINER_NAME, TARGET_PATH, DEST_PATH)
                
        while True:
            inp = input("Type 'exit' to stop the program: ")
            if inp == "exit":
                break
    except Exception as e:
        print(f"Error starting container: {e}")
    finally:
        # Stop and remove the container
        stop_docker_container(CONTAINER_NAME)
        remove_docker_container(CONTAINER_NAME)

if __name__ == '__main__':
    main()