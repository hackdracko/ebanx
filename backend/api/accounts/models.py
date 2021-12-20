from django.db import models

class Accounts(models.Model):
    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.type

    id = models.UUIDField(primary_key=True, editable=False)
    type = models.CharField(max_length=20)
    amount = models.CharField(max_length=5)