import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')

#     def __str__(self):
#         return self.question_text
    
#     def was_published_recently(self):
#         return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#     def __str__(self):
#         return self.choice_text

class Chemical(models.Model):
    cas = models.CharField(max_length=12) # includes hyphens
    formula = models.CharField(max_length=20) # will have notation like underscores for subscript, and if subscript>9 then use a=10, etc. Later will decide what max length should be
    name = models.CharField(max_length=50) # later will decide what max length should be
    # loc = models.CharField(max_length=10) # dk how to integrate yet, but options should be "TALI", "TMAC", and "MS" for now
    # state = models.CharField(max_length=20) # same as above, options: "solution", "granule", "strip" etc
    # init_vol = models.CharField(max_length=10) # initial max volume, used as cap & for user reference
    # min_thresh = models.CharField(max_length=10) # threshold for warning; user set
    safety = models.TextField()
    barcode = models.BinaryField() # might need this, not sure
    # unit = models.TextChoices() # removing til i figure out how choices work. choices will be mg, mL, bottles, etc -- whatever is the unit of transaction

    def __str__(self):
        return self.name
    
    # returns the current amount in stock
    def computeAmount(self):
        amount = 0
        for transaction in self.transaction_set.all():
            amount += transaction.amount
        return amount
    
    # returns transactions, sorted by recency
    def getTransactions(self):
        return self.transaction_set.all().order_by('-time')

class Transaction(models.Model):
    chemical = models.ForeignKey(Chemical, on_delete=models.CASCADE)
    amount = models.IntegerField() # amount in chemical's unit. negative if removing
    time = models.DateTimeField()
    # maybe also keep track of the user who made the transaction
    
    # return absolute value of amount field, i.e. how much was taken or how much was added
    def getAbsoluteAmount(self):
        return abs(self.amount)