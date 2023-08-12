# from typing import Any, Dict
# import socket

# from confluent_kafka import Producer, Consumer
# from confluent_kafka.admin import AdminClient, NewTopic, NewPartitions
from rich import print as rich_print
from pathlib import Path

# # from pykafka import KafkaClient

BASE_DIR = Path(".").parent.parent.resolve(strict=False)


# def read_ccloud_config(config_file) -> Dict[str, Any]:
#     conf = {}
#     with open(config_file, "r") as fh:
#         for line in fh:
#             line = line.strip()
#             if len(line) != 0 and line[0] != "#":
#                 parameter, value = line.strip().split("=", 1)
#                 conf[parameter] = value.strip()
#     return conf


# def producer_ack_callback(error, message) -> None:
#     if error is not None:
#         rich_print(
#             f"[red]Failed to deliver message `[green]{message}[/green]`, error details: [bold]{error}[/bold][/red]"
#         )
#     else:
#         # rich_print(f"[green]Message produced = {message}[/green]")
#         rich_print(f"[yellow][bold][+][/bold]Message produced by producer: [/yellow]")
#         rich_print(str(message.value().decode("utf-8")))


# PRODUCER_CONF: Dict[str, Any] = {
#     "bootstrap.servers": "PLAINTEXT://localhost:29092",  # "host1:9092,host2:9092",
#     "client.id": socket.gethostname(),
#     "on_delivery": producer_ack_callback,
# }  # read_ccloud_config("./client.properties")

# PRODUCER: Producer = Producer(PRODUCER_CONF)

# ADMIN_CONF: Dict[str, Any] = {
#     "bootstrap.servers": "PLAINTEXT://localhost:29092",  # "vps01:9092,vps02:9092,vps03:9092"
# }

# ADMIN: AdminClient = AdminClient(ADMIN_CONF)


# def consumer_commit_callback(error, partitions) -> None:
#     if error is not None:
#         rich_print(f"[red]Exception occured. Error details: [bold]{error}[/bold][/red]")
#     else:
#         rich_print(f"{str(partitions)}")


# CONSUMER_CONF: Dict[str, Any] = {
#     "bootstrap.servers": "PLAINTEXT://localhost:29092",  # "host1:9092,host2:9092",
#     "group.id": "hackrx",
#     "enable.auto.commit": False,
#     "auto.offset.reset": "earliest",
#     "on_commit": consumer_commit_callback,
# }  # PRODUCER_CONF

# CONSUMER: Consumer = Consumer(
#     CONSUMER_CONF
#     | {
#         "group.id": "hackrx",
#         "auto.offset.reset": "earliest",
#         "on_commit": consumer_commit_callback,
#     }
# )


# def default_message_handler(message, *args, **kwargs) -> None:
#     print(message.value())
