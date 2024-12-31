from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class UserRole(models.TextChoices):
    USER = "user", "User"
    SELLER = "seller", "Seller"
    ADMIN = "admin", "Admin"


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, default="example@gmail.com")
    password = models.CharField(max_length=500)
    role = models.CharField(
        max_length=20, choices=UserRole.choices, default=UserRole.USER
    )

    class Meta:
        db_table = "users"

    @classmethod
    def is_correct_password(cls, user_password, actual_password):
        return check_password(user_password, actual_password)

    def save(self, *args, **kwargs):
        if self.password and (
            not self.pk
            or not User.objects.filter(pk=self.pk, password=self.password).exists()
        ):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
