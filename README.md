# Migrate SQS queues

Move all the messages from one SQS queue to another.
```
Usage: sqs2sqs.py -s | --src-url=<SRC_QUEUE_NAME> -d | --dst-url=<DST_QUEUE_NAME>
       sqs2sqs.py -h | --help
```

# Requirements

Needs to be run in a cli with a valid aws session (via [aws-vault](https://github.com/99designs/aws-vault), exporting AWS_PROFILE, using [AWSume](https://awsu.me/))
