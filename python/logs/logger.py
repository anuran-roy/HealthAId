from typing import Literal, List, Dict, Optional, Any

# from dummy.kafka_demo import settings
from config import settings
from rich import print as rich_print
import time
from datetime import datetime


def log(
    alert_level: Literal["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"],
    message: Optional[Dict[str, Any] | str],
) -> None:
    try:
        TOPICS_MAP: Dict[str, str] = {
            "INFO": "HealthAidInfoLogs",  # Topic that retains data for 1 minute
            "DEBUG": "HealthAidDebugLogs",  # Topic that retains data for 5 minutes
            "WARNING": "HealthAidWarningLogs",  # Topic that retains data for 1 day
            "ERROR": "HealthAidErrorLogs",  # Topic that retains data forever
            "CRITICAL": "HealthAidCriticalLogs",  # Topic that retains data forever
        }

        generated_message = f"{str(datetime.now())} | {alert_level} | {message}"
        rich_print(generated_message)
        rich_print(generated_message.encode())
        rich_print(str(time.time()).encode())
        settings.PRODUCER.produce(
            topic=TOPICS_MAP[alert_level],
            key=str(time.time()).encode(),
            value=generated_message.encode(),
        )
    except Exception as e:
        rich_print("[red][bold][X][/bold] Error encountered while logging:")
        rich_print(f"[red]{e}[/red]")
    finally:
        settings.PRODUCER.flush()
