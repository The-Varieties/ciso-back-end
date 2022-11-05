import boto3

aws_secret_access_key = "xirzXwofNqIQrCHc/k4IPCoW2rJ+DYrzo/Q7k82p"
aws_access_key_id = "AKIA2Q5I3UYGDZRKCAVW"


def setup_boto3(access_key, secret_key, instance_id):
    session = boto3.Session(aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key,
                            region_name='ap-southeast-1')
    client = session.client('ec2')
    resource = session.resource('ec2')
    instance = resource.Instance(instance_id)

    return client, instance


def change_instance_type(access_key, secret_key, instance_id, target_instance_type):
    client, instance = setup_boto3(access_key, secret_key, instance_id)

    client.stop_instances(InstanceIds=[instance_id])

    while instance.state.get('Name') != 'stopped':
        instance.reload()
        continue

    client.modify_instance_attribute(
        InstanceId=instance_id,
        InstanceType={'Value': target_instance_type}
    )

    client.start_instances(InstanceIds=[instance_id])

    while instance.state.get('Name') != 'running':
        instance.reload()
        continue
