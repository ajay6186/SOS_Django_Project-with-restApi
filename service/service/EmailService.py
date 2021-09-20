from django.core.mail import send_mail, EmailMessage
from SOS_django_projects.settings import EMAIL_HOST_USER, BASE_DIR
from string import Template
from .EmailBuilder import EmailBuilder


class EmailService:

    @staticmethod
    def send(msg, sendingMail, user):

        if (sendingMail == "changePassword"):
            text = EmailBuilder.change_password(user)
            email = EmailMessage(msg.subject, text, msg.frm, msg.to)
            email.content_subtype = "html"
            try:
                res = email.send()
            except Exception as e:
                res = e
            return res
        elif (sendingMail == "signUp"):
            text = EmailBuilder.sign_up(user)
            email = EmailMessage(msg.subject, text, msg.frm, msg.to)
            email.content_subtype = "html"
            try:
                res = email.send()
            except Exception as e:
                res = e
            return res
        elif (sendingMail == "forgotPassword"):
            text = EmailBuilder.forgot_password(user)
            email = EmailMessage(msg.subject, text, msg.frm, msg.to)
            email.content_subtype = "html"
            try:
                res = email.send()
            except Exception as e:
                res = e
            return res

        elif (sendingMail == "updateprofile"):
            text = EmailBuilder.update_profile(user)
            email = EmailMessage(msg.subject, text, msg.frm, msg.to)
            email.content_subtype = "html"
            try:
                res = email.send()
            except Exception as e:
                res = e
            return res
        else:
            return None
