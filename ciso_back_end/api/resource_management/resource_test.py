import boto3


aws_secret_access_key = "puUg/5WW06YJlEvYvrLaku4hL1NxRGjfzotNDxMh"
aws_access_key_id = "AKIA2Q5I3UYGLDW72AP2"

session = boto3.Session(aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name='ap-southeast-1')

client = session.client('ec2')
resource = session.resource('ec2')


def main():
    instance = resource.Instance('i-049159307d725977b')

    client.stop_instances(InstanceIds=['i-049159307d725977b'])

    while instance.state.get('Name') != 'stopped':
        instance.reload()
        continue

    client.modify_instance_attribute(
        InstanceId='i-049159307d725977b',
        InstanceType={'Value': 't2.micro'}
    )

    client.start_instances(InstanceIds=['i-049159307d725977b'])
    print("Done")


if __name__ == "__main__":
    main()
