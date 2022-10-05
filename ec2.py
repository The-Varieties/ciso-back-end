import boto3 


aws_secret_access_key = "xQ3wCAIU2p7/zR0HpN9BvAWvkBAUrcBr1LY7RdKA"
aws_access_key_id = "AKIA2Q5I3UYGBW2Q6K7U"

session = boto3.Session(aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,                        
                        region_name='us-east-1')

client = session.client('ec2')
resource = session.resource('ec2')


Myec2=client.describe_instances()
x = list(Myec2.keys())

# instance_id = models.AutoField(primary_key=True)
# instance_name = models.CharField(max_length=100, unique=True)
# instance_status = models.CharField(max_length=100, null=True, default="Unknown")
# instance_ipv4 = models.CharField(max_length=100, unique=True)
# instance_AWSSecretKey = models.TextField(default="Unknown")
# instance_AWSAccessKey = models.TextField(default="Unknown")
# instance_region = models.TextField()
# instance_os = models.TextField()
# instance_volume_type = models.TextField()
# instance_type = models.TextField()
# instance_pricing_plan = models.TextField()
arr_dicts = []

for i in range(len(x) - 1):
    for y in Myec2[x[i]]:
        for z in y['Instances']:
            instance_dict = {
                "instance_pricing_plan": x[i],
                "instance_type": z["InstanceType"],
                "instance_ipv4": z["PublicIpAddress"],
                "instance_AWSSecretKey": aws_secret_access_key,
                "instance_AWSAccessKey": aws_access_key_id,
                "instance_region": z["Placement"]["AvailabilityZone"],
                "instance_os": z["PlatformDetails"],
            }   
            
            for j in z["Tags"]:
                if "Name" in j.values():
                    instance_dict["instance_name"] = j["Value"]
                    
            if "instance_name" not in instance_dict:
                instance_dict["instance_name"] = "Instance"
            
            volume_id = z["BlockDeviceMappings"][0]["Ebs"]["VolumeId"]
            
            for volume in resource.volumes.filter(VolumeIds=[volume_id]):
                instance_dict["instance_volume_type"] = volume.volume_type
            
            arr_dicts.append(instance_dict)
            
            
print(arr_dicts)
                
                



            
            
                
            
            
            
            
#             print(z['InstanceId'])
#             print(z['InstanceType'])
    
    
# for volume in resource.volumes.filter(
#     VolumeIds=['vol-019bcff1d2665abe3']
# ):
#     # print(f'Volume {volume.type} ({volume.size} GiB) -> {volume.state}')
#     print(volume.throughtput)
    
    
    
    
    
    
    
    
    
    
    
    
    
# for pythonins in Myec2['Reservations']:
#  for printout in pythonins['Instances']:
#   print(printout['InstanceId'])
#   print(printout['InstanceType'])


# Myec2=client.describe_hosts()
# print(Myec2)

# client.describe_volume()


# ec2s = session.resource('ec2')
# instances = ec2s.instances.all()
# for instance in instances:
#     print(instance.__dict__)
    # print(f'EC2 instance {instance.id}" information:')
    # print(f'Instance state: {instance.state["Name"]}')
    # print(f'Instance AMI: {instance.image.id}')
    # print(f'Instance platform: {instance.platform}')
    # print(f'Instance type: "{instance.instance_type}')
    # print(f'Piblic IPv4 address: {instance.public_ip_address}')
    # print('-'*60)
