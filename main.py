from fastapi import FastAPI, HTTPException
from typing import List
import boto3


def create_ec2_client():
    session = boto3.Session(
        # aws_access_key_id="<your-access-key-id>",
        # aws_secret_access_key="<your-secret-access-key>",
        region_name='us-east-1'
    )
    return session.client('ec2')

app = FastAPI()

def start_ec2_instance(instance_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.start_instances(InstanceIds=[instance_id])
        print(response)
        instance_state = response['StartingInstances'][0]['CurrentState']['Name']
        return {"message": f"Instance {instance_id} started successfully. Current state: {instance_state}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def stop_ec2_instance(instance_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id])
        instance_state = response['StoppingInstances'][0]['CurrentState']['Name']
        return {"message": f"Instance {instance_id} stopped successfully. Current state: {instance_state}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def terminate_ec2_instance(instance_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.terminate_instances(InstanceIds=[instance_id])
        instance_state = response['TerminatingInstances'][0]['CurrentState']['Name']
        return {"message": f"Instance {instance_id} terminated successfully. Current state: {instance_state}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"message": "Welcome to the EC2 instance management via FastApi!"}

# Example request body:
# instance_name = "From_FastApi"
# instance_type = "t2.micro"
# ami_id = "ami-063d43db0594b521b"
# key_pair_name = "<your-key-name>"
# security_group_ids = ["<your-security-group-id>"]

#End point to create an EC2 instance
@app.post("/instances")
async def create_instance(instance_type: str, ami_id: str, key_pair_name: str, security_group_ids: List[str], instance_name: str):
    ec2 = boto3.client('ec2')
    try:
        instances = ec2.run_instances(
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        }
                    ]
                }
            ],
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_pair_name,
            SecurityGroupIds=security_group_ids,
            MinCount=1,
            MaxCount=1
        )
        instance_id = instances['Instances'][0]['InstanceId']
        return {"instance_id": instance_id, "status": "pending"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to list all EC2 instances
@app.get("/instances")
async def list_instances():
    ec2 = boto3.client('ec2', region_name="us-east-1")
    try:
        response = ec2.describe_instances()
        instances = []
        # print (response)
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                state = instance['State']['Name']
                public_ip = instance['PublicIpAddress'] if 'PublicIpAddress' in instance else None
                instances.append({
                    "instance_id": instance_id,
                    "instance_type": instance_type,
                    "state": state,
                    "public_ip": public_ip
                })
        return instances
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to start an EC2 instance
@app.post("/instances/{instance_id}/start")
async def start_instance(instance_id: str):
    return start_ec2_instance(instance_id)

# Endpoint to stop an EC2 instance
@app.post("/instances/{instance_id}/stop")
async def stop_instance(instance_id: str):
    return stop_ec2_instance(instance_id)

# Endpoint to terminate an EC2 instance
@app.delete("/instances/{instance_id}")
async def terminate_instance(instance_id: str):
    return terminate_ec2_instance(instance_id)