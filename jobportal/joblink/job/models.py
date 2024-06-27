from django.db import models
from django.contrib.auth.models import User

# User = get_user_model()

# Create your models here.


class Job(models.Model):
    company = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100)


# models.py
class Emp_account(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    emp_company = models.CharField(max_length=200)
    emp_nums = models.CharField(max_length=30)
    emp_name = models.CharField(max_length=20)
    emp_lastname = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=10)


class Postjob(models.Model):

    employer = models.ForeignKey(Emp_account, on_delete=models.CASCADE,null=True)  
    company_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    work_mode = models.CharField(max_length=50)
    city = models.CharField(max_length=50, null=True, blank=True)
    street_address = models.CharField(max_length=100)
    minimum_salary = models.IntegerField()
    maximum_salary = models.IntegerField()
    rate_period = models.CharField(max_length=20)
    benefits = models.TextField()
    job_type = models.CharField(max_length=50)
    schedule = models.CharField(max_length=50)
    education = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    skills = models.TextField()
    description = models.TextField()
    mobile_no = models.IntegerField()
    email = models.EmailField()


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='profile_pics', default='default.jpg')
#     bio = models.TextField(blank=True)
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=100, blank=True)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length = 100)
    bio = models.TextField(blank=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # email = models.EmailField(unique=True)
    image = models.ImageField(
        upload_to='dps/', default='user.png', blank=True, null=True)
    # date_of_birth = models.DateField(blank=True,null=True)

    def _str_(self): 
        return self.user.username


class Contact(models.Model):
    help_detail = models.CharField(max_length=50)
    select_mode = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    company_details = models.CharField(max_length=200)
    description = models.TextField()

    def _str_(self):
        return 'Message from ' + self.first_name + ' -' + self.email


class Apply(models.Model):

    job_id = models.ForeignKey(Postjob, on_delete=models.CASCADE,null=True) 
    applicant_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=30)
    job_title = models.CharField(max_length=30)
    company_name = models.CharField(max_length=30)
    experience = models.TextField(max_length=200)
    resume = models.FileField(upload_to='resumes/')  
