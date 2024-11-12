# EC2 Instance Management API with FastAPI
This API provides a user-friendly interface to manage EC2 instances using Python's FastAPI framework. It allows you to:

- Create new EC2 instances
- List existing EC2 instances
- Start stopped EC2 instances
- Stop running EC2 instances
- Terminate EC2 instances

## Endpoints
**1. GET / (root):** Returns a welcome message for the API.
<br>

**2. POST /instances (Create Instance):** Creates a new EC2 instance with the provided parameters:
  - instance_type
  - ami_id
  - key_pair_name
  - security_group_ids
  - instance_name
  Returns a dictionary with the newly created instance ID and its current state (pending).
<br>

**3. GET /instances (List Instances):** Lists all running EC2 instances with their details:
  - instance_id
  - instance_type
  - state
  - public_ip (if available)
<br>

**4. POST /instances/{instance_id}/start (Start Instance):** Starts a stopped EC2 instance with the specified instance_id.
<br>

**5. POST /instances/{instance_id}/stop (Stop Instance):** Stops a running EC2 instance with the specified instance_id.
<br>

**6. POST /instances/{instance_id}/terminate (terminate Instance):** Terminate a running/stopped EC2 instance with the specified instance_id.
<br>

## Prerequisites
1. Python 3.6 or later
2. boto3 library (pip install boto3)
3. AWS account with appropriate [IAM permissions for EC2 management](https://docs.aws.amazon.com/IAM/latest/APIReference/welcome.html)

## Setting Up Your Environment
-  Create a Virtual Environment:

```bash

python3 -m venv my_env

source my_env/bin/activate  # Linux/macOS

my_env\Scripts\activate     # Windows

```
- Install Dependencies:

```bash

git clone https://github.com/MohitGupta12/DevOps-Assignment.git

cd DevOps-Assignment

pip install fastapi boto3 uvicorn

```

## Configuration

**Replace placeholders:**
Update the create_ec2_client function with your desired AWS region (currently set to us-east-1).
In the example request body, replace placeholders like instance_name, ami_id, key_pair_name, and security_group_ids with your actual values.
Add AWS Credentials:

**Option 1: Environment Variables:**

```bash

export AWS_ACCESS_KEY_ID="<your_access_key_id>"   

export AWS_SECRET_ACCESS_KEY="<your_secret_access_key>"

```

**Option 2: Credentials File (preferred for security):**
Create a file named credentials at ~/.aws/ (Linux/macOS) or C:\Users\<username>\.aws\ (Windows).

Add your credentials in the following format:   
```bash

aws_access_key_id = <your_access_key_id>

aws_secret_access_key = <your_secret_access_key>

```
## Running the API

Start the application after Doing configuration

```bash
cd DevOps-Assignment

uvicorn main:app --reload

```

This command starts the API server on port 8000. You can access it from your browser at http://localhost:8000/.


## Deploying to AWS EC2

Log into your AWS account and create an EC2 instance (`t2.micro`), using the latest stable
Ubuntu Linux AMI.

[SSH into the instance](https://aws.amazon.com/blogs/compute/new-using-amazon-ec2-instance-connect-for-ssh-access-to-your-ec2-instances/) and run these commands to update the software repository and install
our dependencies.

```bash
sudo apt-get update
sudo apt install -y python3-pip nginx
```

Clone the FastAPI server app (or create your `main.py` in Python).

```bash
git clone https://github.com/MohitGupta12/DevOps-Assignment.git
```

Add the FastAPI configuration to NGINX's folder. Create a file called `fastapi_nginx` (like the one in this repository).

```bash
sudo vim /etc/nginx/sites-enabled/fastapi_nginx
```

And put this config into the file (replace the IP address with your EC2 instance's public IP):

```
server {
    listen 80;   
    server_name <YOUR_EC2_IP>;    
    location / {        
        proxy_pass http://127.0.0.1:8000;    
    }
}
```


Restart NGINX.

```bash
sudo service nginx restart
```

Start FastAPI.

```bash
cd DevOps-Assignment
python3 -m uvicorn main:app
```

Update EC2 security-group settings for your instance to allow HTTP traffic to port 80.

Now when you visit your public IP of the instance, you should be able to access your API.
