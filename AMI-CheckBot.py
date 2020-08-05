# Author: Rounak Pashine and Pradeep Shinde
# Description: This lambda function checks the AMI compliance for all the running EC2 instances in all the regions, and tags it as
#     "AMI-Compliant=Yes" or "AMI-Compliant=No" based on the validation.
#Trigger: Cloudwatch CRON and Cloudwatch "ec2Launch" event

import boto3

Topic_Arn = ''
account = ""

def lambda_handler(object, context):
    # Get list of regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]
    compliant_instances_list=[]

    # Iterate over each region
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)

        print("Region:", region)

        # Get a list of all the running instances
        all_running_instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

        # for instance in all_running_instances:
        # print("Running instance : %s" % instance.id)

        # Get instances with filter of running + with valid AMI-ids
        compliant_instances = ec2.instances.filter(Filters=[{'Name': 'image-id', 'Values': ['']},
                                                            {'Name': 'instance-state-name', 'Values': ['running']}])

        for instance in compliant_instances:
            print("Compliant instances (running) : %s" % instance.id)
            compliant_instances_list.append({'InstanceId': instance.id, 'Status': 'Compliant'})
            response = instance.create_tags(
                DryRun=False,
                Tags=[
                    {
                        'Key': 'AMI-Compliant',
                        'Value': 'Yes'
                    },
                ]
            )

        # Filter from all instances the instance that are not in the filtered list of compliant instances
        non_compliant_instances = [non_compliant for non_compliant in all_running_instances if
                                   non_compliant.id not in [compliant.id for compliant in compliant_instances]]

        for instance in non_compliant_instances:
            print("Non-Compliant instances (running) : %s" % instance.id)
            #non_compliant_instances.stop()
    publish_to_sns(compliant_instances)

def publish_to_sns(message):
    sns = boto3.client('sns')
    sns_message = str(message)
    response = sns.publish(TopicArn=Topic_Arn, Subject="Compliant " + account,
                               Message=sns_message)

