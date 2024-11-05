from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .sms_service import SMSService
#******************************************************************************
#define networks
class Network(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
#******************************************************************************
#transactions
class Transaction(models.Model):
    ACTION_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]

    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    customer = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phonenumber = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits.")]
    )

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.amount}"
#******************************************************************************
#send SMS  on CRUD  operations
@receiver(post_save, sender=Transaction)
def send_sms_on_create_update(sender, instance, created, **kwargs):
    sms_service = SMSService()
    
    if created:
    # Message for new transaction
     message = (
        f"Dear {instance.customer}, your transaction of {instance.action} has been successfully registered. "
        f"Transaction ID: {instance.id}, Amount: Tsh {instance.amount:,.2f} on "
        f"{instance.created_date.strftime('%A, %d %B %Y')} on network {instance.network}."
    )
    else:
     # Message for updated transaction
     message = (
        f"Dear {instance.customer}, your transaction of {instance.action} has been updated successfully. "
        f"Transaction ID: {instance.id}, New Amount: Tsh {instance.amount:,.2f} on "
        f"{instance.updated_date.strftime('%A, %d %B %Y')} on network {instance.network}."
    )

    sms_service.send_sms(instance.phonenumber, message)

@receiver(post_delete, sender=Transaction)
def send_sms_on_delete(sender, instance, **kwargs):
    sms_service = SMSService()
    
    message = (
        f"Dear {instance.customer}, we regret to inform you that your transaction of {instance.action} has been deleted successfully. "
        f"Transaction ID: {instance.id}, Amount: Tsh {instance.amount:,.2f} on "
        f"{instance.created_date.strftime('%A, %d %B %Y')} on network {instance.network}."
    )
    sms_service.send_sms(instance.phonenumber, message)
#******************************************************************************
class Tax(models.Model):
    tax_collection = models.IntegerField(default=0)

    def __str__(self):
        return f"Tax: {self.tax_collection}%"
#******************************************************************************
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
#******************************************************************************
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_description = models.TextField(blank=True, null=True)
    purchasing_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_collection = models.ForeignKey(Tax, on_delete=models.CASCADE, default=1)
    expected_profit = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate expected profit: selling_price - purchasing_price - tax_collection
        tax_value = self.tax_collection.tax_collection if self.tax_collection else 0
        self.expected_profit = self.selling_price - self.purchasing_price - tax_value
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name
#******************************************************************************
class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    profit = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate profit: selling_price - purchasing_price - tax_collection
        tax_value = self.product.tax_collection.tax_collection if self.product.tax_collection else 0
        self.profit = self.product.selling_price - self.product.purchasing_price - tax_value
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f'Sale of {self.product.product_name} by {self.user.username}'

#******************************************************************************
class SoldProduct(models.Model):
    product_name = models.CharField(max_length=200)
    product_description = models.TextField(blank=True, null=True)
    purchasing_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_collection = models.ForeignKey(Tax, on_delete=models.CASCADE, default=1)
    expected_profit = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    profit = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate expected profit
        self.expected_profit = self.selling_price - self.purchasing_price - self.tax_collection.tax_collection
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} sold by {self.user.username}"
