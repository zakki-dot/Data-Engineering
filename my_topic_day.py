import json
import time
from google.cloud import pubsub_v1


def publish_daily_records(project: str, topic: str, filename: str = "bcdaily.json"):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic)

    with open(filename, 'r', encoding='utf-8') as file:
        payloads = json.load(file)

    start_time = time.time()
    for record in payloads:
        data = json.dumps(record).encode('utf-8')
        publisher.publish(topic_path, data).result()
    duration = time.time() - start_time

    print(f"Published {len(payloads)} messages in {duration:.2f} seconds")


if __name__ == '__main__':
    publish_daily_records("project_name", "my-topic")
