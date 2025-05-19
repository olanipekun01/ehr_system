from django.db import models

from .utils import *
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.


class Department(models.Model):
    dept_name = models.CharField(max_length=70)

    def __str__(self):
        return self.dept_name
    
class Units(models.Model):
    unit_name = models.CharField(max_length=500)
    unit_code = models.CharField(max_length=500)

    def __str__(self):
        return self.unit_name


class Supplier(models.Model):
    supp_name = models.CharField(max_length=500)

    def __str__(self):
        return self.supp_name




class Items(models.Model):
    item_id = models.UUIDField(
        primary_key=True,
        editable=False)
    item_name = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=15, decimal_places=1, default=0.0)
    pack_amount = models.DecimalField(max_digits=15, decimal_places=1, default=0.0)
    dept = models.ManyToManyField(Department, related_name='items')
    unit_issue = models.CharField(max_length=200, null=True, blank=True)
    unit_rate = models.DecimalField(
        max_digits=15, decimal_places=1, default=0.0)
    slug = models.SlugField(max_length=2000, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.item_name
    class Meta:
        ordering = [
            'modified_at'
        ]

class Disbursement(models.Model):
    user_type = models.CharField(max_length=500, null=True, blank=True)  # staff or student
    user_name =  models.CharField(max_length=500, null=True, blank=True)
    mat_staff_no = models.CharField(max_length=500, null=True, blank=True) 
    user_dept = models.CharField(max_length=500, null=True, blank=True) 
    file_no = models.CharField(max_length=500, null=True, blank=True) 
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Disbursement #{self.id} by {self.user_name}"

class DisbursementItem(models.Model):
    disbursement = models.ForeignKey(Disbursement, related_name='items', on_delete=models.CASCADE)
    user_type = models.CharField(max_length=500, null=True, blank=True)  # staff or student
    user_name =  models.CharField(max_length=500, null=True, blank=True)
    mat_staff_no = models.CharField(max_length=500, null=True, blank=True) 
    user_dept = models.CharField(max_length=500, null=True, blank=True) 
    file_no = models.CharField(max_length=500, null=True, blank=True) 
    item_name =  models.CharField(max_length=500, null=True, blank=True)
    item = models.ForeignKey('Items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_issue = models.CharField(max_length=200, null=True, blank=True)
    unit_rate = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now=True)
    dateCreated = models.DateField(auto_now=True)
    bal = models.CharField(max_length=500, null=True, blank=True)

    def total_price(self):
        return self.unit_price * self.quantity

class SupplyHistory(models.Model):
    # turn to to a froenign key later
    item_id = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now=True)
    dateCreated = models.DateField(auto_now=True)
    item_name = models.CharField(max_length=500)
    voucher_no = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    action = models.CharField(max_length=200, blank=True, null=True)
    amount = models.CharField(max_length=500)
    bal = models.CharField(max_length=500, null=True, blank=True)
    unit_issue = models.CharField(max_length=200, null=True, blank=True)
    unit_rate = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.item_name

@receiver(pre_save, sender=Items)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
