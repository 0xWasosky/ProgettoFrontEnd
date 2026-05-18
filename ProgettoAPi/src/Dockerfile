# Use the official Python image from Docker Hub
FROM python:3.11-slim


# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker caching
COPY requirements.txt .

# Install any dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project content into the working directory
COPY . .

# Expose the port for your application (change if needed)
EXPOSE 5050

# Command to run your application
CMD ["python", "run.py"]
