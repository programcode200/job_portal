"""
URL configuration for joblink project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    
    path('logout/', views.logout, name='logout'),


    path('jobs/', views.jobs, name='jobs'),
    path('apply_job/', views.apply_job, name='apply_job'),


    path('resume/', views.resume, name='resume'),

    path('view_job/', views.view_job, name='view_job'),


    # for search operation
    path('search/', views.search_jobs, name='search_jobs'),

    path('postjob/', views.postjob, name='postjob'),
    path('savejob/', views.savejob, name='savejob'),

    path('emp_account/', views.emp_account, name='emp_account'),
    path('save_emp_account/', views.save_emp_account, name='save_emp_account'),

    # path('contact/', views.contact, name='contact'),

    path('user_profile/', views.user_profile, name='user_profile'),
    # path('access_denied/', views.access_denied, name='access_denied'),
    path('contact/', views.contact, name='contact'),

    
    path('emp_dashboard/', views.emp_dashboard, name='emp_dashboard'),



    path('applicant/<int:applicant_id>/', views.applicant, name='applicant'),
    # path('job_detail/<int:job_id>/', views.job_detail, name='job_detail'),

   

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
