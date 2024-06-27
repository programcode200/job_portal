from django.contrib import admin

from job.models import Job ,Postjob ,Emp_account, Profile ,Contact, Apply


# from django.contrib.auth.models import User

# admin.site.register(User)

# from django.contrib.auth.models import User

class JobAdmin(admin.ModelAdmin):
    list_display = ('company', 'location', 'category')
    search_fields = ('company', 'location', 'category')

class Emp_accountAdmin(admin.ModelAdmin):
    list_display=('user','emp_company','emp_nums','emp_name','emp_lastname','phone_no')

class PostjobAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'title', 'work_mode', 'city', 'minimum_salary', 'maximum_salary', 'rate_period', 'job_type', 'schedule', 'education', 'experience', 'skills', 'description','mobile_no', 'email')  
    search_fields = ('company_name', 'title', 'work_mode', 'city', 'job_type', 'schedule', 'education', 'experience')  

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('bio','first_name','last_name','image')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('help_detail','select_mode','first_name','last_name','email','phone','company_details','description')
    # search_fields = ('first_name','last_name')

class ApplyAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','email','phone','location','job_title','company_name','experience','resume')
    search_fields = ('first_name','last_name')


admin.site.register(Job, JobAdmin)
admin.site.register(Postjob, PostjobAdmin)
admin.site.register(Emp_account, Emp_accountAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Apply, ApplyAdmin)



# Register your models here.
