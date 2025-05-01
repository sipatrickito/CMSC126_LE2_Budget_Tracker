from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as g


class WithUpdateInfo(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BudgetCategory(WithUpdateInfo):
    owner = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ("owner", "name")

    def __str__(self):
        return self.name


class BudgetEntry(WithUpdateInfo):
    class EntryType(models.TextChoices):
        INCOME = "inc", g("income")
        EXPENSE = "exp", g("expense")

    owner = models.ForeignKey(User, models.CASCADE)
    name = models.TextField()
    category = models.ForeignKey(BudgetCategory, models.SET_NULL, null=True, blank=True)
    entry_type = models.CharField(
        max_length=3, choices=EntryType, default=EntryType.INCOME
    )
    entry_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Budget Entries"

    def __str__(self):
        return self.name


def must_be_current_month(month):
    if month < timezone.now().month:
        raise ValidationError("Must be the current month.")


def must_be_current_year(year):
    if year < timezone.now().year:
        raise ValidationError("Must be the current year.")


class BudgetSetting(WithUpdateInfo):
    owner = models.ForeignKey(User, models.CASCADE)
    category = models.ForeignKey(BudgetCategory, models.CASCADE)
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12), must_be_current_month]
    )
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1970), must_be_current_year]
    )

    class Meta:
        unique_together = ("owner", "category", "month", "year")

    def __str__(self):
        return f"{self.category} {self.month}-{self.year}"
