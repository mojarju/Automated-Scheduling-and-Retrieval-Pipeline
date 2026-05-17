## command to create a repository in AWS ECR with name calendy 
aws ecr create-repository --repository-name calendly --region ca-west-1

## command to build the Docker Container Image (don't forget the dot "." essentially "." = current directory)
#docker build -t calendly .
docker build --platform linux/amd64 --provenance=false -t calendly .


## Command to give the tag latest to the Docker Image 
docker tag calendly:latest 568256617027.dkr.ecr.ca-west-1.amazonaws.com/calendly:latest

## You can get above URI from AWS ECR console 
## Command to connect to AWS ECR 
aws ecr get-login-password --region ca-west-1 | docker login --username AWS --password-stdin 568256617027.dkr.ecr.ca-west-1.amazonaws.com/calendly:latest

## Command to Push the latest Image to AWS ECR
docker push 568256617027.dkr.ecr.ca-west-1.amazonaws.com/calendly:latest