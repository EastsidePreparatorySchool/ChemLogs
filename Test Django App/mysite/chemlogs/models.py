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
    molar_mass = models.FloatField()
    # loc = models.CharField(max_length=10) # dk how to integrate yet, but options should be "TALI", "TMAC", and "MS" for now
    # state = models.CharField(max_length=20) # same as above, options: "solution", "granule", "strip" etc
    # init_vol = models.CharField(max_length=10) # initial max volume, used as cap & for user reference
    # min_thresh = models.CharField(max_length=10) # threshold for warning; user set
    safety = models.TextField()
    barcode = models.BinaryField() # might need this, not sure
    # unit = models.TextChoices() # removing til i figure out how choices work. choices will be mg, mL, bottles, etc -- whatever is the unit of transaction

    def __str__(self):
        return self.name

# used by Chemical and Container
class ChemicalState(models.Model):
    STATE_CHOICES = [
        ("S", "Solid"),
        ("L", "Liquid"),
        ("G", "Gas"), # may not be necessary
        ("AQ", "Aqueous")
    ]
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default="S")
    type = models.CharField(max_length=40, null=True, blank=True) # ex: strips, powder
    min_thresh = models.IntegerField(null=True, blank=True)
    chemical = models.ForeignKey(Chemical, on_delete=models.CASCADE)

    # returns the current amount in stock
    def computeAmount(self):
        amount = 0
        for container in self.container_set.all():
            amount += container.computeAmount()
        return amount
    
    def getInfo(self):
        output = ""
        if self.type:
            output += self.type
        else:
            output += self.state
        return output

# represents a container of a chemical
class Container(models.Model):
    LOC_CHOICES = [
        ("US", "Upper School"),
        ("MS", "Middle School"),
        ("TALI", "TALI")
    ]
    loc = models.CharField(max_length=4, choices=LOC_CHOICES, default="US") # where it is stored
    initial_value = models.IntegerField() # full bottle size, in mL or g of contents
    contents = models.ForeignKey(ChemicalState, on_delete=models.CASCADE)
    molarity = models.FloatField(null=True, blank=True) # often not applicable
    id = models.CharField(max_length=2, primary_key=True) # composed of capital letters. may need len=3
    
    # the header that will be shown for the bottle
    def getHeader(self):
        header = self.id
        if self.molarity:
            header += " - " + str(self.molarity) + "M"
        header += " - " + self.loc
        return header
    
    # returns transactions, sorted by recency
    def getTransactions(self):
        return self.transaction_set.all().order_by('-time')
    
    # returns the current mass, in grams, of the contents of this bottle
    def computeAmount(self):
        amount = 0
        for transaction in self.transaction_set.all():
            amount += transaction.amount
        if self.molarity:
            # convert from mL to g
            amount *= self.molarity / 1000
            amount *= self.contents.chemical.molar_mass
        return amount

class Transaction(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    amount = models.IntegerField() # amount in chemical's unit. negative if removing
    time = models.DateTimeField()
    new = models.BooleanField(default=False) # whether this is the initial transaction "filling" a new bottle for the first time
    # maybe also keep track of the user who made the transaction
    
    # return absolute value of amount field, i.e. how much was taken or how much was added
    def getAbsoluteAmount(self):
        return abs(self.amount)