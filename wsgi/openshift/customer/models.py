from django.db import models
from django.contrib.auth.models import User
#from django.utils.translation import ugettext_lazy as _

class DictModel(models.Model):
    '''
    Simple dictionary
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    phone = models.CharField(max_length=30, blank=True,
                             verbose_name='Phone number')

    def __str__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)

class QuestionKind(DictModel):
    pass

class QuestionStatus(DictModel):
    class Meta:
        verbose_name_plural = 'question statuses'

class Question(models.Model):
    profile = models.ForeignKey(Profile)
    number = models.PositiveIntegerField()
    kind = models.ForeignKey(QuestionKind)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Question date')
    status = models.ForeignKey(QuestionStatus)

    def __str__(self):
        return '{0} - No. {1}'.format(self.profile, self.number)

    class Meta:
        ordering = ['-created_at']

class OrderKind(DictModel):
    pass

class OrderStatus(DictModel):
    class Meta:
        verbose_name_plural = 'order statuses'

class Order(models.Model):
    profile = models.ForeignKey(Profile)
    number = models.PositiveIntegerField()
    kind = models.ForeignKey(OrderKind)
    dispatch_address = models.CharField(max_length=500)
    delivery_address = models.CharField(max_length=500)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Order date')
    status = models.ForeignKey(OrderStatus)

    def __str__(self):
        return '{0} - No. {1}'.format(self.profile, self.number)

    class Meta:
        ordering = ['-created_at']

class DangerCategory(DictModel):
    class Meta:
        verbose_name = 'dangerous goods class'
        verbose_name_plural = 'dangerous goods classes'

class Cargo(models.Model):
    order = models.ForeignKey(Order)
    number = models.PositiveIntegerField()
    number_of_units = models.PositiveIntegerField()
    number_of_boxes = models.PositiveIntegerField()
    weight_nett = models.FloatField()
    weight_gross = models.FloatField()
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    description = models.TextField(blank=True)
    danger_category = models.ForeignKey(DangerCategory)

    def __str__(self):
        return '{0}. Cargo {1}'.format(self.order, self.number)
