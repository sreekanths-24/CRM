from django.db import models

# Create your models here.
class FeedbackTable(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class SupplierRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    Product = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class delivery(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.IntegerField()

    def __str__(self):
        return str(self.order_id)