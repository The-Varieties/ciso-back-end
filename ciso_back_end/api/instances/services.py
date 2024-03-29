import boto3
from ciso_back_end.api.instances.models import Instances


def collect_ec2_instances(aws_access_key, aws_secret_key, user):
    session = boto3.Session(aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_key,
                            region_name='ap-southeast-1')

    client = session.client('ec2')
    resource = session.resource('ec2')

    myec2 = client.describe_instances()
    x = list(myec2.keys())

    arr_dicts = []
    for i in range(len(x) - 1):
        for y in myec2[x[i]]:
            for z in y['Instances']:
                if z["State"]["Name"] == "running":
                    instance_dict = {
                        "instance_aws_id": z["InstanceId"],
                        "instance_pricing_plan": x[i],
                        "instance_type": z["InstanceType"],
                        "instance_ipv4": z["PublicIpAddress"] + ":9100",
                        "instance_region": z["Placement"]["AvailabilityZone"],
                        "instance_os": z["PlatformDetails"]
                    }

                    for j in z["Tags"]:
                        if "Name" in j.values():
                            instance_dict["instance_name"] = j["Value"]

                    if "instance_name" not in instance_dict:
                        instance_dict["instance_name"] = "Instance"

                    volume_id = z["BlockDeviceMappings"][0]["Ebs"]["VolumeId"]

                    for volume in resource.volumes.filter(VolumeIds=[volume_id]):
                        instance_dict["instance_volume_type"] = volume.volume_type

                    instance = Instances.objects.create(
                        instance_aws_id=instance_dict['instance_aws_id'],
                        instance_os=instance_dict['instance_os'],
                        instance_pricing_plan=instance_dict['instance_pricing_plan'],
                        instance_type=instance_dict['instance_type'],
                        instance_ipv4=instance_dict['instance_ipv4'],
                        instance_region=instance_dict['instance_region'],
                        instance_name=instance_dict['instance_name'],
                        instance_volume_type=instance_dict['instance_volume_type'],
                        user=user
                    )

                    instance.save()
    client.close()
    return arr_dicts


def get_targets_for_prometheus():
    all_instances = Instances.objects.all()

    response_data = []
    if all_instances:
        for instance in all_instances.iterator():
            target_dict = {
                "targets": [instance.instance_ipv4],
                "labels": {"hostname": instance.instance_name}
            }
            response_data.append(target_dict)
    return response_data
