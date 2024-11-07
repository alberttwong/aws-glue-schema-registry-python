import logging
import boto3

session = boto3.Session(region_name='us-west-2')

glue_client = session.client('glue')

from aws_schema_registry import DataAndSchema, SchemaRegistryClient
from aws_schema_registry.avro import AvroSchema

# In this example we will use kafka-python as our Kafka client,
# so we need to have the `kafka-python` extras installed and use
# the kafka adapter.
from aws_schema_registry.adapter.kafka import KafkaSerializer
from kafka import KafkaProducer

# Create the schema registry client, which is a façade around the boto3 glue client
client = SchemaRegistryClient(glue_client,
                              registry_name='ajaxavro')

# Create the serializer
serializer = KafkaSerializer(client)

# Create the producer
producer = KafkaProducer(value_serializer=serializer)

# Our producer needs a schema to send along with the data.
# In this example we're using Avro, so we'll load an .avsc file.
with open('user.avsc', 'r') as schema_file:
    schema = AvroSchema(schema_file.read())

# Send message data along with schema
data = {
    'name': 'John Doe',
    'favorite_number': 6
}
producer.send('my-topic', value=(data, schema))
# the value MUST be a tuple when we're using the KafkaSerializer
