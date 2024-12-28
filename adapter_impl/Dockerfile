FROM python:3.9
WORKDIR /app

# Copy the requirements file first (to leverage Docker caching for dependencies)
COPY ./adapter_impl/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./adapter_impl/adapter.py ./adapter_impl/db_func.py .

# Set the default command to run the app
CMD ["python", "adapter.py"]
