#!/bin/bash

# This file is managed by Ansible. Local changes will be lost!

# And now mangle the filename and upload to S3
ORIGINAL=`/usr/local/bin/prefix_filename.py "$1"`
FILENAME=`python -c "print(\"$ORIGINAL\").replace(' ', '_')"`
LOGFILE=/var/log/uploadscript.log
BUCKET={{ s3_weather_app_bucket }}

# Enable for debugging
#echo $1 received at `date` >> $LOGFILE
#echo -n "ORIGINAL set to: " >> $LOGFILE
#echo $ORIGINAL >> $LOGFILE
#echo -n "FILENAME set to: " >> $LOGFILE
#echo $FILENAME >> $LOGFILE

###############################################################################
# This block should not be touched. All the S3 work is taken care of through
# various Ansible configurations.

# ftp timestamp in filename generation - Adds timestamp to the csv file prior to sending to S3
# echo "Calling s3cmd with this command: s3cmd -c /etc/s3cfg put \"$ORIGINAL\" $BUCKET$FILENAME"
s3cmd -c /etc/s3cfg put "$ORIGINAL" $BUCKET$FILENAME # >> $LOGFILE


# TODO: This isn't ideal to upload the file twice. Need to create & config a SNS topic
# TODO: Then subscribe all the SQS queues to that SNS topic. Have the s3 bucket create event to sns topic.
# TODO: See s3 file uploaded message in multiple sqs
# Uncomment to Firehose UAT with prod FTP data. Hack here to send to <region>-weather-app-staging as well.
s3cmd -c /etc/s3cfg put "$ORIGINAL" s3://{{ REGION }}-weather-app-staging$FILENAME # >> $LOGFILE  # TODO


# Used to archive in NFS, now its in s3 backup so deleting file here
rm "$FILENAME" # >> $LOGFILE
echo "$(date) File uploaded to S3, $FILENAME" >> $LOGFILE


###############################################################################

# Script finish
exit 0
