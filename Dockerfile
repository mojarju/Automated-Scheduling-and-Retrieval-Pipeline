# Use AWS Lambda Python 3.9 base image
# --platform=linux/amd64 forces the image architecture to AMD64
# This helps avoid compatibility issues if building on Apple Silicon (M1/M2 Macs)
FROM --platform=linux/amd64 public.ecr.aws/Lambda/Python:3.9

# Set working directory to /var/task (AWS Lambda defaults)
# AWS Lambda expects application files in /var/task
# Any following COPY, RUN, CMD commands use this directory by default
WORKDIR /var/task

# Copy Application files into the container 
    # copy the lambda function source file and dependaciesfrom your local machine into the container
COPY lambda_function.py .   
COPY requirements.txt .

# Install dependancies 
# --no-cache-dir prevents pip from storing cache files (keeps Docker Image Smaller)
RUN pip install --no-cache-dir -r requirements.txt

# Set the container entrypoint
# This tells docker what the executable should always be when the container starts
#
# /var/lang/bin/python3.9
#       -> the Python interpreter included in the Lambda base image 
#
# -m awslambdaric 
#       -> runs the AWS Lambda Runtime Interface Client 
#       -> this component allows the container to communate with AWS Lambda
ENTRYPOINT [ "/var/lang/bin/python3.9", "-m", "awslambdaric" ]

# Specify the Lambda handler function
#
# Format: 
#       "<filename>.,function_name>"
#
# lambda_function
#       -> refers to lambda_function.py
#
# lambda_handler
#       -> the function inside the file that AWS Lambda should execute
CMD [ "lambda_function.lambda_handler" ]