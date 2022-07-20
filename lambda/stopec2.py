import boto3
region = 'us-west-1'
instances = ['i-12345abcde4f78g9h', 'i-08sf9b2f7csef6d52']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))