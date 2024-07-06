# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install ALSA libraries
RUN apt-get update && apt-get install -y \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
ENV NAME World

# Run streamlit when the container launches
# CMD ["streamlit", "run", "app.py"]
# CMD streamlit run --server.port 8501 --server.enableCORS true app.py
CMD streamlit run --server.port 8501 --server.address 0.0.0.0 --server.enableCORS false app.py