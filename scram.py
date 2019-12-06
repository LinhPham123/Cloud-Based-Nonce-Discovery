import boto3

if __name__ == "__main__":
    print("Emergency closing everything on Cloud")

    ec2_resource = boto3.resource('ec2')
    ec2_resource.instances.terminate()

    bucket_to_kill = input("Enter the bucket name you wish to kill (n/a if not): ")
    if bucket_to_kill != 'n/a':
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_to_kill)
        for item in bucket.objects.all():
            item.delete()
        s3.Bucket(bucket_to_kill).delete()
