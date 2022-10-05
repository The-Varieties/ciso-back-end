import os  # to get the necessary environment variables  
import time  # to wait until AWS RDS instance will be created
from datetime import datetime

import sys
import boto3
# import dotenv 
# from botocore.exceptions import ClientError

aws_secret_access_key = "xQ3wCAIU2p7/zR0HpN9BvAWvkBAUrcBr1LY7RdKA"
aws_access_key_id = "AKIA2Q5I3UYGBW2Q6K7U"

session = boto3.Session(aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,                        
                        region_name='ap-southeast-1')

client = session.client('ec2')
resource = session.resource('ec2')

# ec2 = boto3.client('ec2')
# if sys.argv[1] == 'ON':
#     response = ec2.monitor_instances(InstanceIds=['INSTANCE_ID'])
# else:
#     response = ec2.unmonitor_instances(InstanceIds=['INSTANCE_ID'])
# print(response)

# instance_id = sys.argv[2]
# action = sys.argv[1].upper()

# ec2 = boto3.client('ec2')


# if action == 'ON':
#     # Do a dryrun first to verify permissions
#     try:
#         ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
#     except ClientError as e:
#         if 'DryRunOperation' not in str(e):
#             raise

#     # Dry run succeeded, run start_instances without dryrun
#     try:
response = client.start_instances(InstanceIds=['i-049159307d725977b'])
print(response)

#     except ClientError as e:
#         print(e)
# else:
#     # Do a dryrun first to verify permissions
#     try:
#         ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
#     except ClientError as e:
#         if 'DryRunOperation' not in str(e):
#             raise

#     # Dry run succeeded, call stop_instances without dryrun
#     try:

# response = client.stop_instances(InstanceIds=['i-049159307d725977b'])
# print(response)


# response = client.send_ssh_public_key(
#     # The zone where the instance was launched
#     AvailabilityZone='us-east-1a',
#     # The instance ID to publish the key to.
#     InstanceId='i-abcd1234',
#     # This should be the user you wish to be when ssh-ing to the instance (eg, ec2-user@[instance IP])
#     InstanceOSUser='ec2-user',
#     # This should be in standard OpenSSH format (ssh-rsa [key body])
#     SSHPublicKey='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3FlHqj2eqCdrGHuA6dRjfZXQ4HX5lXEIRHaNbxEwE5Te7xNF7StwhrDtiV7IdT5fDqbRyGw/szPj3xGkNTVoElCZ2dDFb2qYZ1WLIpZwj/UhO9l2mgfjR56UojjQut5Jvn2KZ1OcyrNO0J83kCaJCV7JoVbXY79FBMUccYNY45zmv9+1FMCfY6i2jdIhwR6+yLk8oubL8lIPyq7X+6b9S0yKCkB7Peml1DvghlybpAIUrC9vofHt6XP4V1i0bImw1IlljQS+DUmULRFSccATDscCX9ajnj7Crhm0HAZC0tBPXpFdHkPwL3yzYo546SCS9LKEwz62ymxxbL9k7h09t',
# )

# print(response)

response = client.modify_instance_attribute(

    InstanceId='i-049159307d725977b',
    InstanceType={'Value': 't1.micro'}
)