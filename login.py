import base64
import boto3
import subprocess

print("Initializing secure Boto3 session client...")
client = boto3.client('ecr', region_name='us-east-1')

try:
    print("Requesting secure token handshake from AWS...")
    auth_data = client.get_authorization_token()
    token = auth_data['authorizationData'][0]['authorizationToken']
    
    decoded_token = base64.b64decode(token).decode('utf-8')
    username, password = decoded_token.split(':')
    
    # Reconstruct the cloud path safely inside the code execution block
    account_id = "396037508514"
    registry_url = f"{account_id}.dkr.ecr.us-east-1.amazonaws.com"
    repo_name = "aws-ecs-python-pipeline"
    full_target_image = f"{registry_url}/{repo_name}:latest"
    
    print("Passing credentials directly into Docker...")
    subprocess.run(
        ['docker', 'login', '--username', username, '--password-stdin', registry_url],
       input=password, check=True, text=True
    )
    
    print("\n[STEP 1/2] Labeling local container image for ECR registry...")
    subprocess.run(['docker', 'tag', 'cloudops-app:latest', full_target_image], check=True)
    
    print("[STEP 2/2] Pushing image up to AWS Cloud Repository...")
    subprocess.run(['docker', 'push', full_target_image], check=True)
    
    print("\n🚀 SUCCESS! Your Docker container image has been shipped to AWS ECR!")

except Exception as e:
    print(f"\nPipeline failed: {e}")