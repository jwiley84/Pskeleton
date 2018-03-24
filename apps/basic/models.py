from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import time

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        results = {
            'status': False
        }
        errors = {};
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if not postData['first_name'].isalpha:
            errors['first_name_alpha'] = "First name must be letters only"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if not postData['last_name'].isalpha:
            errors['last_name_alpha'] = "First name must be letters only"
        if not re.match('[^@]+@[^@]+\.[^@]+',postData['email']):
            errors['email'] = "Emails must be in the Someone@Something.ending format"
        if postData['birthday'] > time.strftime("%Y-%m-%d"):
            errors['bday'] = 'Invalid birthday! Need to be from the past.'
        if len(postData['password']) < 8:
            errors['password_length'] = "Password must be at least 8 characters"
        if postData['password'] != postData['conf']:
            errors['unmatched'] = "Passwords do not match"
        results['errors'] = errors
        if len(errors) == 0:
            results['status'] = True
            hash_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            results['newUser'] = self.create(first_name=postData['first_name'],last_name=postData['last_name'], email=postData['email'], password=hash_pw)       
        print(results)
        return results
    def login_validator(self, postData):
        results = {
            'status': False
        }
        errors = {};
        check_user = User.objects.filter(email = postData['email'])
        check_pass = postData['password']
        if not check_user:
            errors['noUser'] = "No registered account under that email. Please check the spelling, or register to the left"    
        elif not bcrypt.checkpw(check_pass.encode(), check_user[0].password.encode()):
            errors['wrongPW'] = "Incorrect password. Please check spelling and try again. Password reset system is currently offline"
        results['errors'] = errors
        if len(errors) == 0:
            results['status'] = True;
            results['user'] = check_user[0]
        return results
        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    birthday = models.DateField(auto_now = False, auto_now_add = False, default= '1900-04-25')
    ### HI THIS IS SUPER IMPORTANT IF IT WORKS ###
    objects = UserManager()
    def __repr__(self):
        return self.first_name;

class quoteManager(models.Manager):
    def quote_validator(self, id, postData):
        results = {
            'status': False
        }
        errors = {}
        if len(postData['author']) < 3:
            errors['author'] = "Author name must be at least 3 letters long."
        if len(postData['content']) < 10:
            errors['quote'] = "Quote must be at least 10 characters long."
        results['errors'] = errors
        if len(errors) == 0:
            results['new_quote'] = self.create(author=postData['author'], content=postData['content'], posted_by = User.objects.get(id = id)) 
            results['status'] = True
        return results

    def faveQuote(self, id, postData):
        user = User.objects.get(id = id)
        quote = self.get(id = postData['this_quote'])
        quote.faved_by.add(user)
        return ("Added!")
    def unfaveQuote(self, id, postData):
        user = User.objects.get(id = id)
        quote = self.get(id = postData['this_quote'])
        quote.faved_by.remove(user)
        return ("Added!")

class Quote(models.Model):
    author = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="quotes")
    faved_by = models.ManyToManyField(User, related_name="faves")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = quoteManager()
    def __str__(self):
        return self.author


# one author has many quotes? DOn't bother, you'll break your DB, and THIS wireframe doesn't call for searching via author
# ----user has many quotes
# --user has many favorite quotes
# ---quote has one poster (user)
# quote has many faved users
