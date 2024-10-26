import json
import os
import sys

import six

sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaProducer


class RedPanda:
    def __init__(self, topic):
        server = os.getenv("REDPANDA_SERVER")
        user = os.getenv("REDPANDA_USER")
        pwd = os.getenv("REDPANDA_PWD")
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=server,
            security_protocol="SASL_SSL",
            sasl_mechanism="SCRAM-SHA-256",
            sasl_plain_username=user,
            sasl_plain_password=pwd,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    @staticmethod
    def on_error(e):
        print(f"Error sending message: {e}")

    def produce(self, key, data):
        future = self.producer.send(
            self.topic,
            key=key.encode('utf-8'),
            value=data
        )
        future.add_errback(self.on_error)
        self.producer.flush()

    def close(self):
        self.producer.close()
