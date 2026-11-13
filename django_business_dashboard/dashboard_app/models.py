from django.db import models

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Refunded', 'Refunded'),
    ]

    customer_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.customer_name} - ${self.amount}"
