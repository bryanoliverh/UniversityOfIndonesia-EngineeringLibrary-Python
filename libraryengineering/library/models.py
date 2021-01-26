from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.urls import reverse



class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)
    #used in issue book
    def __str__(self):
        return self.user.first_name+'['+str(self.enrollment)+']'
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id
  
    
    class Meta:
        ordering = ["enrollment"]

class Book(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('thesis', 'Thesis'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('essay', 'Essay'),
        ('paper/article', 'Paper/Article'),
        ]

    name=models.CharField(max_length=100)
    isbn=models.CharField('ISBN', max_length=14,
                            unique=True,
                            help_text='14 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')

    author=models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    category=models.CharField(max_length=30,choices=catchoice,default='education')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, help_text="Select Book Language")
  
    
    class Meta:
        ordering = ["name"]
    
    def __str__(self):
        return str(self.name)+"["+str(self.isbn)+']'

class Author(models.Model):
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ["first_name"]
    def __str__(self):

        return '{0}, {1}'.format(self.last_name, self.first_name)


class Language(models.Model):
    
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    class Meta:
        ordering = ["name"]
    def __str__(self):
   
        return self.name


def get_expiry():
    return datetime.today() + timedelta(days=15)
class IssuedBook(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    enrollment=models.CharField(max_length=30)
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    class Meta:
        ordering = ["expirydate"]
    def __str__(self):
        return self.isbn
