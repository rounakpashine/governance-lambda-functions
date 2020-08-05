#Author: Rounak Pashine and Pradeep Shinde
#Description: This lambda function STOPS the EC2 instances w/o any attached tags or w/o proper required tags.
#Trigger: Cloudwatch CRON and Cloudwatch "ec2Launch" event

import boto3
import logging
import time

# setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)
value_null = []
Key_null = []
time.sleep(60)
account = "AWS Enterprise 1Platform"
# define the connection
ec2 = boto3.resource('ec2')
s = ""


def lambda_handler(event, context):
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    filters = [
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]

    # filter the instances
    instances = ec2.instances.filter(Filters=filters)
    for instance in instances:
        # print instance.id
        if not instance.tags:
            # print "No tags!!!"
            Key_null.append(instance.id)
        else:
            if 'Name' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
            if 'ProductTower' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
            if 'Application' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
            if 'SupportContact' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
            if 'Description' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
            if 'ApplicationOwner' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
            if 'Costcenter' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
            if 'Domain' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
            if 'Environment' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
            if 'Group' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
            if 'Owner' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
                # add and remove tags from here
            get_instance_name(instance.id)
            #   print list(set(value_null))
    print "Count of instance having one or more tags missing %d" % len(list(set(Key_null)))
    print "Count of all Instances having one or more key missing  %d" % len(list(set(value_null)))
    print " "
    untaggedInstances = Key_null + value_null
    untaggedInstances = list(set(untaggedInstances))
    s = ""
    if len(untaggedInstances) > 0:
        # perform the shutdown
        for instance in untaggedInstances:
            s += instance + "\n"
        print s
    #        stopInstance(untaggedInstances)
    #        publish_to_sns(s)
    else:
        print "Nothing to see here..!"


def stopInstance(instanceId):
    #    instanceId = ['TestingID']
    ec2.instances.filter(InstanceIds=instanceId).stop()


def get_instance_name(fid):
    # When given an instance ID as str e.g. 'i-1234567', return the instance 'Name' from the name tag.
    ec2instance = ec2.Instance(fid)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            name = tags["Value"]
            if len(name) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)
        if tags["Key"] == 'ProductTower':
            producttower = tags["Value"]
            if len(producttower) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)
        if tags["Key"] == 'Application':
            application = tags["Value"]
            if len(application) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)
        if tags["Key"] == 'SupportContact':
            supportcontact = tags["Value"]
            if len(supportcontact) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)
        if tags["Key"] == 'Description':
            description = tags["Value"]
            if len(description) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)
        if tags["Key"] == 'ApplicationOwner':
            applicationowner = tags["Value"]
            if len(applicationowner) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)
        if tags["Key"] == 'Costcenter':
            costcenter = tags["Value"]
            if len(costcenter) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)
        if tags["Key"] == 'Domain':
            domain = tags["Value"]
            if len(domain) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)
        if tags["Key"] == 'Environment':
            environment = tags["Value"]
            if environment != 'non-prod' or environment != 'prod':
                print ec2instance.id
                value_null.append(ec2instance.id)
        if tags["Key"] == 'Group':
            group = tags["Value"]
            if len(group) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)
        if tags["Key"] == 'Owner':
            owner = tags["Value"]
            if len(owner) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)

# add and remove tags from here