from datetime import datetime, timezone
from notices.models import Notice

def create_notice_data():
    Notice.objects.create(title='Notice1', content='content of notice1', date=datetime.now().astimezone())
    Notice.objects.create(title='Notice2', content='content of notice2', date=datetime.now().astimezone())