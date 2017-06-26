from django.contrib.auth.backends import ModelBackend

class FacebookBackend:
    def authenticate(self, request, **kwargs):
        pass

    def get_user(self, user_id):
        pass