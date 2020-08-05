#Author: Rounak Pashine And Pradeep Shinde
#Description: This lambda function deletes the volume which are not attached to any instance (are in available state) and without the tag "Do-Not-Delete=Yes".
#Trigger: Cloudwatch CRON and Cloudwatch "ec2Terminate" event

import boto3

Topic_Arn = 'arn:aws:sns:us-east-2:655824777623:lambda_functions'
account = "AWS Enterprise SandBox"

# Set the global variables
globalVars  = {}
globalVars['REGION_NAME']           = "us-east-2"
globalVars['TAG_NAME']            = "Do-Not-Delete"
globalVars['tagsToExclude']         = "Yes"

ec2       = boto3.resource('ec2', region_name = globalVars['REGION_NAME'] )

def lambda_handler(event, context):

    deletedVolumes=[]

    # Get all the volumes in the region
    for vol in ec2.volumes.all():
        if  vol.state=='available':

            # Check for Tags
            if vol.tags is None:
                vid=vol.id
                v=ec2.Volume(vol.id)
                v.delete()

                deletedVolumes.append({'VolumeId': vol.id,'Status':'Delete Initiated'})
                print "Deleted Volume: {0} for not having Tags".format( vid )

                continue

            # Find Value for Tag without Key as "Name"
            for tag in vol.tags:
                if tag['Key'] != globalVars['TAG_NAME']:
                    vid = vol.id
                    v = ec2.Volume(vol.id)
                    v.delete()
                    deletedVolumes.append( {'VolumeId': vol.id,'Status':'Delete Initiated'} )
                    print "Deleted Volume: {0} for not having Tags".format( vid )

            # Find Value for Tag with Key as "Name" and Value other than Yes
            for tag in vol.tags:
                if tag['Key'] == globalVars['TAG_NAME']:
                  value=tag['Value']
                  if value != globalVars['tagsToExclude'] and vol.state == 'available' :
                    vid = vol.id
                    v = ec2.Volume(vol.id)
                    v.delete()
                    deletedVolumes.append( {'VolumeId': vol.id,'Status':'Delete Initiated'} )
                    print "Deleted Volume: {0} for not having Tags".format( vid )

    # If no Volumes are deleted, to return consistent json output
    if not deletedVolumes:
        deletedVolumes.append({'VolumeId':None,'Status':None})

    publish_to_sns(deletedVolumes)

    #Publish to SNS
def publish_to_sns(message):
    sns = boto3.client('sns')
    sns_message = str(message)
    response = sns.publish(TopicArn=Topic_Arn, Subject="Available Volumes to be deleted " + account,
                               Message=sns_message)

    # Return the list of status of the snapshots triggered by lambda as list
    #return deletedVolumes
    #delete
