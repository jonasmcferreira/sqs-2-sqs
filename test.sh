#!/bin/sh
set -e

account_id=$(aws sts get-caller-identity --query "Account" --output text)
queue_in="delete-this-queue-in-$RANDOM"
queue_out="delete-this-queue-in-$RANDOM"

echo "Setting up"
aws sqs create-queue --queue-name $queue_in
aws sqs create-queue --queue-name $queue_out
aws sqs send-message --queue-url https://sqs.eu-central-1.amazonaws.com/$account_id/$queue_in --message-body "Test successful"

echo "running the script"
pip3 install -r requirements.txt > /dev/null
python3 migrate_sqs_queues.py -s $queue_in -d $queue_out

echo "check if message is there"
aws sqs receive-message --queue-url https://sqs.eu-central-1.amazonaws.com/$account_id/$queue_out \
    --attribute-names All --message-attribute-names All --max-number-of-messages 1 \
    --query "Messages[0].Body" \
    --output text

echo "cleaning up"
aws sqs delete-queue --queue-url https://sqs.eu-central-1.amazonaws.com/$account_id/$queue_in
aws sqs delete-queue --queue-url https://sqs.eu-central-1.amazonaws.com/$account_id/$queue_out

echo "done"