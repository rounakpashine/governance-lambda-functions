#Author: Rounak Pashine And Pradeep Shinde
#Description: This lambda function nightly stops the EC2 instances with the tag "NightWatcher=Yes".
#Trigger: CloudWatch CRON event

import boto3


def lambda_handler(object, context):

    # Get list of regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]

    #Iterate over each region
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)

        print("Region:", region)

        # Get only running instances
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}, {'Name':'tag:NightWatcher', 'Values':['Yes']}])


        # Stop the Instances
        for instance in instances:
         #   instance.stop()
            print('stopped instance: ', instance.id)