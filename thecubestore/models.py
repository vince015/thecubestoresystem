from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Profile(models.Model):

    # Validator for phone number
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:\
                                          '+999999999'. Up to 15 digits allowed.")

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=True)

    contact_number = models.CharField(max_length=15,
                                      validators=[phone_regex],
                                      blank=False)
    birthday = models.DateField(null=True)
    primary_address = models.CharField(max_length=2048,
                                       blank=False)
    alternate_address = models.CharField(max_length=2048,
                                         blank=False)

class Store(models.Model):

    profile = models.ForeignKey('Profile',
                                null=True,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=256,
                            blank=False)
    facebook = models.CharField(max_length=128,
                                blank=False)
    instagram = models.CharField(max_length=128,
                                 blank=False)
    website = models.CharField(max_length=256,
                               blank=False)

class Cube(models.Model):

    profile = models.ForeignKey('Profile',
                                on_delete=models.CASCADE,
                                null=True)
    unit = models.CharField(blank=False,
                            max_length=10,
                            null=True)
    duration = models.PositiveSmallIntegerField(blank=False)
    promo = models.PositiveSmallIntegerField(blank=False,
                                             default=0)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    next_due_date = models.DateField(null=True)

class Payment(models.Model):

    # Variables for payment modes
    cash = 'ca'
    cheque = 'ch'
    payment_mode = ((cash, 'CASH'), (cheque, 'CHECK'))

    profile = models.ForeignKey('Profile',
                                on_delete=models.CASCADE,
                                null=True)
    mode = models.CharField(max_length=2,
                            choices=payment_mode,
                            default=cash,
                            blank=False)
    bank = models.CharField(max_length=128,
                            blank=False)
    account = models.CharField(max_length=128,
                               blank=False)

class Lease(models.Model):

    profile = models.OneToOneField(Profile,
                                   on_delete=models.CASCADE,
                                   blank=False,
                                   null=True)
    duration = models.PositiveSmallIntegerField(blank=False)
    promo = models.PositiveSmallIntegerField(blank=False,
                                             default=0)
    vat = models.DecimalField(default=0,
                              max_digits=3,
                              decimal_places=2)
    sales = models.DecimalField(default=0,
                                max_digits=3,
                                decimal_places=2)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    next_due_date = models.DateField(null=True)

class Item(models.Model):

    cube = models.ForeignKey('Cube',
                             on_delete=models.CASCADE,
                             blank=False)
    name = models.CharField(max_length=32,
                            null=True)
    quantity = models.PositiveSmallIntegerField(blank=False)
    price = models.DecimalField(max_digits=7,
                                decimal_places=2)
    vat = models.DecimalField(default=0,
                              max_digits=3,
                              decimal_places=2)
    commission = models.DecimalField(default=0,
                                     max_digits=3,
                                     decimal_places=2)

class Sales(models.Model):

    item = models.ForeignKey('Item',
                             on_delete=models.CASCADE,
                             blank=False)
    date = models.DateField(blank=False)
    quantity = models.PositiveSmallIntegerField(blank=False)
    net = models.DecimalField(max_digits=7,
                              decimal_places=2)
