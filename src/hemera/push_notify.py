import datetime
import os

import requests

from hemera.standard_logger import logging


def push_job_run(name, status="Complete", runtime: datetime.timedelta = None):
    if runtime:
        runtime = datetime.timedelta(seconds=runtime.seconds)
        runtime = str(runtime)
    else:
        runtime = "Unknown"

    headline = f"Run {name} {status}"
    body = f"Job ran for {runtime}"
    ifttt_push_notification(headline, body)


def ifttt_push_notification(headline: str, body: str = "-"):
    IFTTT_KEY = os.environ.get("IFTTT_KEY", None)
    if not IFTTT_KEY:
        logging.warning("No IFTTT key set, message not set")
    msg = {"value1": headline, "value2": body}
    requests.post(f"https://maker.ifttt.com/trigger/exper_done/with/key/{IFTTT_KEY}", data=msg)
