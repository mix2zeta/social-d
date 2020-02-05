from dataclasses import dataclass
import os


@dataclass
class settings:
    @dataclass
    class DATABASE:
        PGHOST: str = os.environ["PGHOST"]
        PGPORT: str = os.environ["PGPORT"]
        PGDBNAME: str = os.environ["PGDBNAME"]
        PGUSER: str = os.environ["PGUSER"]
        PGPASSWORD: str = os.environ["PGPASSWORD"]

    REDIS_URL: str = os.environ["REDIS_URL"]
    BASE_URL: str = os.environ["BASE_URL"]
    CSV_LINE_LIMIT = 50000
    RAW_DATA_PATH = '/usr/src/raw_data'
    SPLIT_DATA_PATH = '/usr/src/spilt_data'
    MEDIA_PATH = '/usr/src/media'
