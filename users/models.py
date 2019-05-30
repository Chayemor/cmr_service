from django.contrib.auth.models import AbstractUser
from django.db import models

"""
https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
If you’re starting a new project, it’s highly recommended to set up a custom user model, 
even if the default User model is sufficient for you.
"""

class User(AbstractUser):
    pass
