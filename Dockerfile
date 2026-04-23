# 1. Start with a lightweight Python image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first to cache layers
COPY requirements.txt .

# 4. Install necessary libraries
RUN pip install --no-cache-dir -r requirements.txt


# 5. Copy the rest of the application code and data
COPY . .

# 6. The command to run the script when the container starts
CMD ["python", "engine.py"]