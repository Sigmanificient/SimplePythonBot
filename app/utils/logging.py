from datetime import datetime

LOG_FORMAT = '%d/%b/%Y:%H:%M:%S'

def log(*args):
    print(f"[{datetime.now().strftime(LOG_FORMAT)}]", *args)
