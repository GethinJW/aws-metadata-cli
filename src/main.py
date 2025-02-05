from dotenv import load_dotenv

from aws_client import AWSClient

load_dotenv()

if __name__ == "__main__":
    aws_client = AWSClient()
    ec2_resource = aws_client.get_resource("ec2")
    for instance in ec2_resource.instances.all():
        print(f"Instance ID: {instance.id}")
        print(f"State: {instance.state['Name']}")
        print(f"Type: {instance.instance_type}")
        print(f"Launch Time: {instance.launch_time}")
        print("-" * 40)
