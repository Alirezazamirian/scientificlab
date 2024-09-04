from accounts.models import User, Code
import datetime

def code_expiration(phone):
    code = Code.objects.get(user__phone=phone)
    diff_seconds = datetime.datetime.now().timestamp() - code.created_at.timestamp()
    if diff_seconds >= 120:
        return True
    else:
        return False
