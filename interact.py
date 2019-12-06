import boto3
from botocore.exceptions import ClientError
import time
import sys

if __name__ == "__main__":
    number_of_VMs_string = input("Enter number of VMs: ")
    difficulty_level_string = input("Enter level of difficulty (1 to 64): ")

    key_name = input("Your key pair name/path: ")
    role_ARN = input("Enter the IAM role for your instance (AmazonEC2RoleforSSM policy is required): ")
    delete_bucket = input("Do you want to delete the bucket when finish? (yes/no): ")

    s3 = boto3.resource('s3')  
    bucket_created = False
    while not bucket_created:
        bucket_name = input("Your bucket name: ")
        try:
            s3.create_bucket(Bucket=bucket_name)
            bucket_created = True
        except ClientError:
            print("Bucket name is already taken, try again")
    
    print("Bucket is ready, uploading pow file to bucket")
    s3.meta.client.upload_file(Filename='pow.py', Bucket=bucket_name, Key='pow.py')
    time.sleep(5)

    print("Creating instances")
    ec2_resource = boto3.resource('ec2')
    newly_created_instances = ec2_resource.create_instances(
            ImageId ='ami-00068cd7555f543d5',
            MinCount = int(number_of_VMs_string),
            MaxCount = int(number_of_VMs_string),
            InstanceType = 't2.micro',
            KeyName = key_name,
            SecurityGroups = ['launch-wizard-1'],
            IamInstanceProfile = {
                'Arn' : role_ARN
            }
        )
    
    print("Instances created, wait till running and pass status check")
    hosts = []
    waiter = ec2_resource.meta.client.get_waiter('instance_status_ok')
    for new_instance in newly_created_instances:
        new_instance.wait_until_running()
        hosts.append(new_instance.id)
    
    waiter.wait(InstanceIds = hosts)

    hosts = []
    for instance in ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]):
        hosts.append(instance.id)


    print("Downloading file from bucket to instances")
    ssm = boto3.client('ssm')
    ssm.send_command(
        InstanceIds=hosts, 
        DocumentName='AWS-RunShellScript', 
        Parameters={'commands': ['aws s3 cp s3://' + bucket_name + '/pow.py ~/pow.py']})
    time.sleep(10)


    print("Starting execute")
    for index, host in enumerate(hosts):
        ssm.send_command(
            InstanceIds=[host], 
            OutputS3BucketName=bucket_name,
            OutputS3KeyPrefix='output',
            DocumentName='AWS-RunShellScript',
            Parameters={'commands': ['cd ~/..', 'cd ..', 'cd root', 'python pow.py %d %s %s' % (index, number_of_VMs_string, difficulty_level_string)]})
        print('python pow.py %d %s %s' % (index, number_of_VMs_string, difficulty_level_string))
    time.sleep(5)


    results = []
    bucket = s3.Bucket(bucket_name)
    finished = False
    while not finished:
        for item in bucket.objects.all():
            if('output' in item.key):
                ec2_resource.instances.terminate()
                results.append(s3.Object(bucket_name, item.key).get()['Body'].read())  
                finished = True
                break
        time.sleep(10)   

    print(results)
    bucket.objects.filter(Prefix="output/").delete()

    if delete_bucket == "yes":
        for item in bucket.objects.all():
            item.delete()
        s3.Bucket(bucket_name).delete()