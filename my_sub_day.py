import time
import threading
from concurrent.futures import TimeoutError as PubSubTimeoutError
from google.cloud import pubsub_v1


def run_subscription(project: str, subscription: str, timeout: float = 3000.0):
    client = pubsub_v1.SubscriberClient()
    sub_path = client.subscription_path(project, subscription)
    message_counter = {'count': 0}
    lock = threading.Lock()

    def _on_message(message):
        with lock:
            message_counter['count'] += 1
        print(f"Message received: {message.data.decode('utf-8')}")
        message.ack()

    streaming_pull = client.subscribe(sub_path, callback=_on_message)
    start_time = time.time()

    with client:
        try:
            streaming_pull.result(timeout=timeout)
        except PubSubTimeoutError:
            streaming_pull.cancel()
            streaming_pull.result()

    elapsed = time.time() - start_time
    print(f"Total messages consumed: {message_counter['count']} in {elapsed:.2f} seconds")


if __name__ == '__main__':
    run_subscription("project_name", "my-sub")