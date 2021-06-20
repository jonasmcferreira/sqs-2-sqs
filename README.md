# Migrate SQS queues

Move all the messages from one SQS queue to another.
```
Usage: migrate_sqs_queues.py -s | --src-url=<SRC_QUEUE_NAME> -d | --dst-url=<DST_QUEUE_NAME>
       migrate_sqs_queues.py -h | --help
```

# Requirements

Needs to be run in a cli with a valid aws session (via aws-vault, exporting AWS_PROFILE, using AWSume)