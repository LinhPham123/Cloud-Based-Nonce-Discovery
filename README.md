# Cloud-Based-Nonce-Discovery
#comsm0010_CW

This is the repository for the Cloud Computing coursework at Bristol University.

## Scripts
- “interact.py” is the main script to be execute on the local machine.
- “pow.py” is the script running the proof of work, and will be sent to the cloud and executed by the instances.
- “scram.py” is an emergency stop which will terminate all the EC2 instances, plus deleting the S3 bucket if required.

## Dependencies Needed on Local Machine
- Python3
- Boto3 library

## Deployment Process
1. Install the required dependencies.
2. Place credentials details of your AWS account in ```~/.aws/credentials```.
3. Place extra configurations such as region etc, in ```~/.aws/config```.
4. Create a key pair and store the secrect key file in ```~/.ssh/```.
5. Create an IAM Role that include the "AmazonEC2RoleforSSM" policy.
5. Download all source codes into one folder and execute.
```python interact.py```
6. Enter the parameters prompted.
7. In case an emergency stop needed, stop the interact.py script with ```CTRL+C``` and execute
```python scram.py```.
