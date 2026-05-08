from datetime import datetime
from zoneinfo import ZoneInfo


KST = ZoneInfo("Asia/Seoul")


def now_kst() -> datetime:
    return datetime.now(KST)


def now_kst_naive() -> datetime:
    return now_kst().replace(tzinfo=None)
