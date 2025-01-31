from pyfcm import FCMNotification

from django.conf import settings

def send_notification(fcm_token:str, title, body, image=None):
    push_service = FCMNotification(settings.FCM_KEY)
    return push_service.notify(
        fcm_token=fcm_token, 
        notification_title=title, 
        notification_body=body,
        notification_image=None,
    )
