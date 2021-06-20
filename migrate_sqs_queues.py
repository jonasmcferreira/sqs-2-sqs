#!/usr/bin/env python
"""
Move all the messages from one SQS queue to another.

Usage: migrate_sqs_queues.py --src-queue=<SRC_QUEUE> --dst-queue=<DST_QUEUE>
       migrate_sqs_queues.py -s <SRC_QUEUE> -d <DST_QUEUE>
       migrate_sqs_queues.py -h | --help

"""
import argparse
import sys

import boto3


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Move all the messages from one SQS queue to another.")

    parser.add_argument("-s","--src-queue",required=True,help="Queue to read messages from")
    parser.add_argument("-d","--dst-queue",required=True,help="Queue to move messages to")

    return parser.parse_args()


def get_messages_from_queue(sqs_client, queue_url):
    """Generates messages from an SQS queue.

    Note: this continues to generate messages until the queue is empty.
    Every message on the queue will be deleted.

    :param queue_url: URL of the SQS queue to read.

    """
    while True:
        resp = sqs_client.receive_message(
            QueueUrl=queue_url, AttributeNames=["All"], MaxNumberOfMessages=10
        )

        try:
            yield from resp["Messages"]
        except KeyError:
            return

        entries = [
            {"Id": msg["MessageId"], "ReceiptHandle": msg["ReceiptHandle"]}
            for msg in resp["Messages"]
        ]

        resp = sqs_client.delete_message_batch(QueueUrl=queue_url, Entries=entries)

        if len(resp["Successful"]) != len(entries):
            raise RuntimeError(
                f"Failed to delete messages: entries={entries!r} resp={resp!r}"
            )

def main(args):

    # getting the account id of the current session
    account_id = boto3.client("sts").get_caller_identity()["Account"]

    src_queue_url = "https://sqs.amazonaws.com/" + account_id + "/"+args.src_queue
    dst_queue_url = "https://sqs.amazonaws.com/" + account_id + "/"+args.dst_queue

    if src_queue_url == dst_queue_url:
        sys.exit("Source and destination queues cannot be the same.")

    sqs_client = boto3.client("sqs")

    for message in get_messages_from_queue(sqs_client, queue_url=src_queue_url):
        sqs_client.send_message(QueueUrl=dst_queue_url, MessageBody=message["Body"])



if __name__ == "__main__":
    
    # parsing arguments
    main(parse_args())
