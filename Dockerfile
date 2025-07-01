# Use the AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.9

# Set working directory
WORKDIR /var/task

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY ./app /var/task/app
COPY ./models /var/task/models
COPY ./Utils /var/task/Utils
COPY lambda_handler.py .
COPY init_db.py .

# Make sure the database directory exists
RUN mkdir -p /var/task/database

# Run the init script to generate the DB with 3 tables
RUN python3 init_db.py

# Lambda handler
CMD ["lambda_handler.lambda_handler"]