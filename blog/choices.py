from django.db.models import TextChoices


class PostStatusChoices(TextChoices):
    DRAFT = "Draft", "Draft"
    PENDING = "Pending", "Pending"
    APPROVED = "Approved", "Approved"
    REJECTED = "Rejected", "Rejected"


class CategoryChoices(TextChoices):
    TECHNOLOGY = "Technology", "Technology"
    LIFESTYLE = "Lifestyle", "Lifestyle"
    FOOD = "Food", "Food"
