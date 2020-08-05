#Author: Rounak Pashine and Pradeep Shinde
#Description: This lambda function deletes the "*launch-wizard*" security groups which are not associated to any instances.
#Trigger: Cloudwatch CRON and Cloudwatch "ec2Launch" event

import boto3
import logging
from botocore.exceptions import ClientError

# Customize the global variables as needed
globalVars  = {}
globalVars['REGION_NAME']           = "us-east-2"
globalVars['findNeedle']            = "*launch-wizard*"

ec2 = boto3.client('ec2', region_name = globalVars['REGION_NAME'] )

filters = [
    {'Name': 'group-name', 'Values': [ globalVars['findNeedle'] ] }
]

def janitor_for_security_groups():
    sg_deleted = { 'TotalSecurityGroupsDeleted':'','SecurityGroups': [] }
    sgs = ec2.describe_security_groups(Filters=filters).get('SecurityGroups')
    for sg in sgs:
        logging.info("Attempting to delete security group: {0}, ID: {1}".format(sg.get('GroupName'), sg.get('GroupId') ))
        try:
            #ec2.delete_security_group(GroupName=sg.get('GroupName'))
            sg_deleted.get('SecurityGroups').append(
                {'GroupName': sg.get('GroupName'), 'GroupId': sg.get('GroupId'),
                'Description': sg.get('Description'), 'VpcId': sg.get('VpcId')})

        except ClientError as e:
            print(str(e.response))
            logging.error('Unable to delete Security Group with id: {0}'.format(sg.get('GroupId')) )
            logging.error('ERROR: {0}'.format( str(e.response)) )

    # Get the count of security groups deleted to provide a descriptive message
    if sg_deleted['SecurityGroups']:
        sg_deleted['TotalSecurityGroupsDeleted'] = len( sg_deleted['SecurityGroups'] )
    else:
        sg_deleted['TotalSecurityGroupsDeleted'] = 0

    return sg_deleted

def lambda_handler(event, context):
    return janitor_for_security_groups()

if __name__ == '__main__':
    lambda_handler(None, None)