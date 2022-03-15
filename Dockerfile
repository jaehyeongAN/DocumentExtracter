# Base IMAGE
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Set the working directory to /app
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app

RUN apt-get -y update && \
    apt-get -y install --no-install-recommends default-jdk-headless && \
	apt -y install build-essential libpoppler-cpp-dev pkg-config python3-dev && \
	pip install -r requirements.txt

# Make port 8001 available to the world outside this container
# EXPOSE 8001

# Run app.py when the container launches
# CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8001","--ssl-keyfile","./key.pem","--ssl-certfile","./cert.pem"]