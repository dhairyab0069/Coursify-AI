
# Coursify AI Application

Coursify AI is a Flask-based web application designed to assist educators in generating educational content effortlessly. This guide will walk you through setting up the project on your local machine for development and testing purposes.

## Prerequisites

Before you begin, ensure you have the following software installed on your system:

- **Docker:** [Download & Install Docker](https://www.docker.com/get-started)
- **Git:** [Download & Install Git](https://git-scm.com/downloads)
- **Visual Studio Code (VSCode):** [Download & Install VSCode](https://code.visualstudio.com/) (Optional, but recommended for editing the code)

## Installation

Follow these steps to get your development environment set up:

1. **Clone the Repository**

   Open a terminal and run the following command to clone the repository:

   ```bash
   git clone https://github.com/COSC-499-W2023/year-long-project-team-16.git
   ```


2. **Navigate to the Project Directory**

   Change into the project directory:

   ```bash
   cd <repository-name>/app/coursify-ai
   ```

   Ensure you are in the directory containing the `Dockerfile`.

3. **Build the Docker Image**

   Build the Docker image for the application:

   ```bash
   docker build -t coursify-app .
   ```

   This command creates a Docker image named `coursify-app`.

4. **Run the Docker Container**

   Run the application inside a Docker container:

   ```bash
   docker run -p 5001:5000 coursify-app
   ```

   This command maps port 5001 on your local machine to port 5000 inside the Docker container.

5. **Access the Application**

   Open a web browser and go to [http://localhost:5001](http://localhost:5001) to view the application.

## Stopping the Application

To stop the application, you will need to stop the Docker container:

1. **Find the Container ID**

   List all running containers:

   ```bash
   docker ps
   ```

2. **Stop the Container**

   Use the container ID to stop the container:

   ```bash
   docker stop <container_id>
   ```

Replace `<container_id>` with the ID of your container.

## Development

For development, it's recommended to use Visual Studio Code. You can open the project directory in VSCode and use its built-in terminal and Git support for an efficient development workflow.

## Support

For any issues or questions, please open an issue on the GitHub repository.

Thank you for trying out Coursify AI!

