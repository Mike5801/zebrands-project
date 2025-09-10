from django.core.mail import send_mail
from main.settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model

User = get_user_model()

def notify_via_email(product_id, product_name, owner, action, fail_silently=True):
    """
    Sends email notifications to all existing users in the database
    """
    try:
        users = User.objects.all()
        receiver_list = [user.email for user in users if user.email]
        formatted_subject = f"Product catalog has been recently changed by: {owner}"
        formatted_message = f"""
        Summary:
        - Action: {action}
        - Product_id: {product_id}
        - Product_name: {product_name}
        - Changed by: {owner}
        """
        send_mail(formatted_subject, formatted_message, EMAIL_HOST_USER, receiver_list, fail_silently)
    except Exception as e:
        raise Exception("Sending email failed", e)