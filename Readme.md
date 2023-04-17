# Application Dockerization

This repository contains a Dockerfile and docker-compose.yml for running the `application.py` Python script.

## Usage

1. Clone this repository: `git clone https://github.com/your-username/your-repo.git`
2. Change into the cloned directory: `cd your-repo`
3. Build the Docker image: `docker build -t app .`
4. Start the Docker container: `docker-compose up -d`
5. Access the application at `http://localhost:8050`

## Notes

- The Docker image uses Python 3.6.
- The `name.db` and `schoolList.csv` files must be present in the same directory as the `docker-compose.yml` file in order to be mounted into the container.
- The application can be accessed at `http://localhost:8050` in your web browser.
