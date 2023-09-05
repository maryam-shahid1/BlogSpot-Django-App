from django.db.models import TextChoices


class UserRoleChoices(TextChoices):
    ADMIN = "Admin", "Admin"
    AUTHOR = "Author", "Author"


class RequestStatusChoices(TextChoices):
    PENDING = "Pending", "Pending"
    ACCEPTED = "Accepted", "Accepted"
    REJECTED = "Rejected", "Rejected"
