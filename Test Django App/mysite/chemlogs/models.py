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
    molar_mass = models.FloatField(default=0, null=True) # in g/mol
    safety = models.TextField(default="", null=True)

    def __str__(self):
        return self.name
    
    # def is_valid():
        

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
    # note: chemical and (type or state) should together be able to uniquely identify a chemicalstate

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

    def needMore(self):
        if self.min_thresh and self.computeAmount() < self.min_thresh:
            return True
        return False
    
    # human-readable notification for if this is low
    def getNotification(self):
        notification = "\n\t\u2022 " + self.chemical.name + " " + self.getInfo()
        notification += ": Total supply is "
        notification += str(round(self.computeAmount(), 2))
        notification += "g. Minimum threshold is "
        notification += str(self.min_thresh) + "g."
        return notification

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
    
    # returns transactions, excluding any that are not supposed to be visible (e.g., type new)
    def getTransactionsToDisplay(self):
        return self.getTransactions().exclude(type="N").exclude(type="I")
    
    def getRecentDisplayableTransactions(self):
        return self.getTransactionsToDisplay()[:7]
    
    # returns whether there is not at least one displayable transaction
    def noDisplayableTransactions(self):
        return len(self.getTransactionsToDisplay()) == 0
    
    # returns g or mL, whichever is more appropriate
    def getUnits(self):
        if self.molarity:
            return 'mL'
        else:
            return 'g'
    
    # returns current amount, in either mL or g (whichever is more fitting)
    def computeRawAmount(self):
        amount = 0
        for transaction in self.transaction_set.all().order_by('time'):
            if transaction.type in {"T", "N"}:
                amount += transaction.amount
            elif transaction.type == "R":
                amount = transaction.amount
        return amount
    
    # returns the current mass, in grams, of the contents of this bottle.
    # if amount is specified, that raw amount is used instead.
    def computeAmount(self, amount=None):
        if not amount:
            amount = self.computeRawAmount()
        if self.molarity:
            # convert from mL to g
            amount *= self.molarity / 1000
            amount *= self.contents.chemical.molar_mass
        return amount
    
    # return amount in g, with units. if aqueous, also add amount in mL, in parentheses.
    # if amount is specified, it is used instead of self.computeRawAmount.
    # amounts are rounded to two decimal places.
    def getDisplayableAmount(self, amount=None):
        if not amount:
            amount = self.computeRawAmount()
        display = str(round(self.computeAmount(amount), 2)) + 'g'
        if self.molarity:
            display = str(round(amount, 2)) + 'mL (' + display + ')'
        return display
    
    def getInitialDisplayableAmount(self):
        return self.getDisplayableAmount(self.initial_value)

class Transaction(models.Model):
    TYPE_CHOICES = [
        ("T", "TRANSACT"), # normal transaction
        ("N", "NEW"), # auto-generated "transaction" when a new bottle is added to inventory
        ("R", "RESET"), # override previous transactions; set new current amount
        ("I", "IGNORED") # basically deleted, except it can be restored
    ]

    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default="T")
    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    amount = models.IntegerField() # amount in chemical's unit. negative if removing
    time = models.DateTimeField()
    user = models.CharField(max_length=50) # username
    
    # return absolute value of amount field, i.e. how much was taken or how much was added
    def getAbsoluteAmount(self):
        return abs(self.amount)

# this might not be necessary (not really used i think)
class TransactionEdit(models.Model): # table of historical user actions to modify a transaction
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    date = models.DateTimeField()
    # what is was changed from and to
    old_amount = models.IntegerField()
    new_amount = models.IntegerField()
    old_type = models.CharField(max_length=1, choices=Transaction.TYPE_CHOICES)
    new_type = models.CharField(max_length=1, choices=Transaction.TYPE_CHOICES)
    user = models.CharField(max_length=50) # username