from django.contrib.auth.tokens import PasswordResetTokenGenerator  
from six import text_type 
#https://www.javatpoint.com/django-user-registration-with-email-confirmation
#https://studygyaan.com/django/how-to-signup-user-and-send-confirmation-email-in-django

class TokenGenerator(PasswordResetTokenGenerator):  
    def _make_hash_value(self, user, timestamp):  
        return (  
            text_type(user.pk) + text_type(timestamp) +  
            text_type(user.is_active)  
        )  
account_activation_token = TokenGenerator()