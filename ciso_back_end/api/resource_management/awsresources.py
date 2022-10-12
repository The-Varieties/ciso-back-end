import os  # to get the necessary environment variables  
import time  # to wait until AWS RDS instance will be created
from datetime import datetime

import sys
from urllib import response
import boto3
# # import dotenv 
# from botocore.exceptions import ClientError

aws_secret_access_key = "O6rt9vAoNFJIHXCGD6GzBM7aTXva47bWTfyDcXTh"
aws_access_key_id = "AKIA2Q5I3UYGMGO222SJ"

session = boto3.Session(aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,                        
                        region_name='ap-southeast-1')

client = session.client('ec2')
resource = session.resource('ec2')


# response = client.monitor_instances(
#     InstanceIds=[
#         'i-049159307d725977b'
#     ]
# )
# print(response)

# response = client.unmonitor_instances(InstanceIds=['i-049159307d725977b'])
# print(response)

# instance_id = sys.argv[2]
# action = sys.argv[1].upper()

# # ec2 = boto3.client('ec2')

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
# def running():

# def stopped():

# response = resource.Instance('i-049159307d725977b')
# if response.state['Name'] == 'running':
#     print('It is running')
# else:
#     print('It is not running')

# response = client.describe_instance_status(InstanceIds=['i-049159307d725977b'])
# if response['InstanceStatuses'][0]['InstanceState']['Name'] == 'running':
#     print('It is running')
# else:
#     print('It is not running')

# response = client.describe_instance_status(InstanceIds=['i-049159307d725977b'])
# print(response)

def start_instances():
    response = client.start_instances(InstanceIds=['i-049159307d725977b'])
    print(response)

def stop_instances():
    response = client.stop_instances(InstanceIds=['i-049159307d725977b'])
    print(response)

def modify_instance_attribute_type():
    response = client.modify_instance_attribute(
        InstanceId='i-049159307d725977b',
        InstanceType={'Value': 't1.micro'}
    )

    
def main():    

            instance = resource.Instance('i-049159307d725977b')
        # while instance.state['Name'] == 'running':
        #     answer = input('Stop instances?')
        #     if answer == 'Yes':
        #         stop_instances()
            while instance.state['Name'] == 'stopped':
                    answer2 = input('What do you wish to modify?')
                    if answer2 == 'Instance Type':
                        modify_instance_attribute_type()
                    else:
                        answer3 = input('Start instances?')
                        if answer3 == 'Yes':
                            start_instances()
                        else:
                            break
            # else:
            #     break

if __name__ == "__main__":
    main()

