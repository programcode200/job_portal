from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import Job, Postjob, Emp_account, Profile, Contact, Apply
from django.contrib.auth.hashers import check_password


# Create your views here.
def home(request):
    jobData = Postjob.objects.all().order_by("-id")

    data = {"jobData": jobData}
    return render(request, "index.html", data)


# for about page
def about(request):
    return render(request, "about.html")


# for signup page


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        type = request.POST.get("type")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        # Check if the passwords match
        if password != confirm_password:
            # Passwords do not match
            messages.error(request, "password do not match")
            return render(request, "signup.html")

        # Check if the username or email already exist
        if User.objects.filter(username=username).exists():
            messages.error(request, "username already exist")
            return render(request, "signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exist")
            return render(request, "signup.html")

        # Create a new user
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        if type == "employer":
            user.is_staff = True
        user.save()
        # messages.success(request, "User signup successful. Confirmation email sent.")

        subject = "Registration Successful"
        message = f"Hi {username},\n\nYou have successfully registered on joblink."
        recipient_list = [email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        messages.success(request, "Signup successful. Confirmation email sent.")

        return redirect("signin")
        # return HttpResponse("Signup page content")

    return render(request, "signup.html")


def signin(request):
    user = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            user = request.user
            request.session["is_login"] = "true"
            messages.success(request, "Signin successful.")

            return redirect("/")
        else:
            # User does not exist
            messages.error(request, "Invalid username or password.")
            return render(request, "signin.html")
    return render(request, "signin.html")


def logout(request):
    auth_logout(request)
    return redirect("home")


def view_job(request):
    id = request.GET.get("id")
    job = Postjob.objects.filter(id=id).first()

    # return redirect('apply_job')

    return render(request, "view_job.html", {"job": job})


def jobs(request):

    if request.method == "GET":
        company_query = request.GET.get("company")
        location_query = request.GET.get("location")
        category_query = request.GET.get("categories")

        # Start with an empty queryset
        jobs = Postjob.objects.none()

        # Define Q objects for each query parameter
        company_filter = (
            Q(company_name__icontains=company_query) if company_query else Q()
        )
        location_filter = Q(city__icontains=location_query) if location_query else Q()
        category_filter = Q(skills__icontains=category_query) if category_query else Q()

        # Combine filters using OR operator
        filter_query = company_filter | location_filter | category_filter

        # Apply filter to get jobs
        jobs = Postjob.objects.filter(filter_query)

        print(jobs)  # Print the filtered queryset for debugging

        return render(request, "jobs.html", {"jobs": jobs})


def resume(request):
    return render(request, "resume.html")


@login_required(login_url="/signin/")
def apply_job(request):
    job_id = request.GET.get("id")
    if request.method == "POST":
        # Retrieve form data

        job_id = request.POST.get("job_id")
        Job = Postjob.objects.get(id=job_id)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        location = request.POST.get("location")
        job_title = request.POST.get("job_title")
        company_name = request.POST.get("company_name")
        experience = request.POST.get("experience")
        resume = request.FILES.get("resume")
        # job = Postjob.objects.get(id=request.POST.get('job_id'))
        # job_id = request.POST.get('job_id')
        # job = Postjob.objects.get(id=job_id)
        # print(f'Job ID: {job_id}')
        # job = Postjob.objects.get(id=request.POST.get('job_id'))

        # try:
        #     job = Postjob.objects.get(id=request.POST.get('job_id'))
        # except Postjob.DoesNotExist:
        #     return HttpResponse("The job you're trying to apply for does not exist.")

        # job_id = request.POST.get('job_id')
        # try:
        #     job = Postjob.objects.get(id=job_id)
        # except Postjob.DoesNotExist:
        #     return HttpResponse("The job you're trying to apply for does not exist.")

        # job_id = request.POST.get('job_id')
        # if not job_id:
        #     return HttpResponse("Job ID is required.")
        # try:
        #     job = Postjob.objects.get(id=job_id)
        # except Postjob.DoesNotExist:
        #     return HttpResponse("The job you're trying to apply for does not exist.")

        apply_data = Apply(
            job_id=Job,
            applicant_id=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            location=location,
            job_title=job_title,
            company_name=company_name,
            experience=experience,
            resume=resume,
        )

        apply_data.save()

        # employer_dashboard_data = EmployerDashboard(
        #     employer=request.user,
        #     applied_job=job_id,  # Save the applied job
        #     applicant_name=f"{first_name} {last_name}",  # Save the applicant's name
        #     applicant_email=email,  # Save the applicant's email
        #     resume=resume  # Save the applicant's resume
        # )
        # employer_dashboard_data.save()

        # Send email
        subject = "Job Application Submitted Successfully"
        message = f"Hello {first_name} {last_name},\n\nYour job application has been successfully submitted. <hr> Good luck!"
        recipient_list = [email]
        sender_name = "joblink"
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        success_message = "Your application has been submitted successfully. Good luck!"
        messages.success(request, "Your application send successfully.")

        # Redirect to a thank you page or any other page
        # Replace 'thank_you' with your URL name for the thank you page
        return redirect("/")
    # else:
    #     messages.error(request, 'Please log in first.')
    #     return redirect('/signin/')

    return render(request, "apply_job.html", {"job_id": job_id})


def search_jobs(request):
    jobs = Job.objects.all()
    company_query = request.GET.get("company")
    location_query = request.GET.get("location")
    category_query = request.GET.get("categories")

    jobs = Job.objects.filter(
        company__icontains=company_query,
        location__icontains=location_query,
        category__icontains=category_query,
    )

    return render(request, "index.html", {"jobs": jobs})


def postjob(request):
    # messages.success(request,'hello')

    if Emp_account.objects.filter(user=request.user).exists():
        # User has an associated Emp_account, so direct them to the job posting form
        return render(request, "postjob.html")
    else:
        # User does not have an associated Emp_account, so redirect them to fill out the Emp_account form
        messages.error(request, "You must create an Employer Account to post a job.")

    # return render(request, "postjob.html")


def savejob(request):
    if request.method == "POST":
        company_name = request.POST.get("company_name")
        job_title = request.POST.get("job-title")
        location = request.POST.get("location")
        city = request.POST.get("cityname")
        address = request.POST.get("address")
        minimum_sal = request.POST.get("min-sal")
        maximum_sal = request.POST.get("max-sal")
        rate_period = request.POST.get("rate-per")
        benefits = request.POST.get("benefits")
        job_type = request.POST.get("jobtype")
        schedule = request.POST.get("schedule")
        education = request.POST.get("education")
        experience = request.POST.get("experience")
        skills = request.POST.get("skills")
        description = request.POST.get("description")
        mobile_no = request.POST.get("mobile-no")
        email = request.POST.get("email-id")
        employer = Emp_account.objects.get(user=request.user)

    data = Postjob(
        company_name=company_name,
        title=job_title,
        work_mode=location,
        city=city,
        street_address=address,
        minimum_salary=minimum_sal,
        maximum_salary=maximum_sal,
        rate_period=rate_period,
        benefits=benefits,
        job_type=job_type,
        schedule=schedule,
        education=education,
        experience=experience,
        skills=skills,
        description=description,
        mobile_no=mobile_no,
        email=email,
        employer=employer,
    )

    data.save()

    subject = "Job Application Submitted Successfully"
    message = f"Hello ,\n\nYour job posted successfully."
    recipient_list = [email]
    sender_name = "joblink"
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

    success_message = "Your application has been submitted successfully. Good luck!"
    # messages.success(request, 'Your application send successfully.')

    messages.success(request, f"Job Posted Successfully!")
    return redirect("home")

    return render(request, "index.html")


@login_required(login_url="/signin/")
def emp_account(request):
    if request.method == "POST":
        return save_emp_account(request)

    if Emp_account.objects.filter(user=request.user).exists():
        # If user already has an Emp_account, redirect them to post job form
        return redirect("postjob")
    else:
        # Otherwise, render the Emp_account form for the user to fill out
        return render(request, "emp_account.html")

        messages.error(request, "You need to do first Login or Signup")
        return render(request, "signin")


def save_emp_account(request):
    if request.method == "POST":
        emp_company = request.POST.get("company_name")
        emp_nums = request.POST.get("employees")
        emp_name = request.POST.get("f_name")
        emp_lastname = request.POST.get("l_name")
        phone_no = request.POST.get("phone")

        # Create and save the emp_account
        emp_data = Emp_account(
            emp_company=emp_company,
            emp_nums=emp_nums,
            emp_name=emp_name,
            emp_lastname=emp_lastname,
            phone_no=phone_no,
            user=request.user,  # Associate the emp_account with the current user
        )
        emp_data.save()

        # Redirect to the postjob form
        return redirect("postjob")
    else:
        return render(request, "emp_account.html")


def user_profile(request):
    try:
        # Try to retrieve the user's profile
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # If the profile doesn't exist, create a new one
        user_profile = Profile.objects.create(user=request.user)

    user_model = request.user

    if request.method == "POST":

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        # bio = request.POST['bio']

        if request.FILES.get("dp") == None:
            dp = user_profile.image
        else:
            dp = request.FILES.get("dp")

        user_profile.image = dp
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.email = email
        # user_model.bio = bio

        if "bio" in request.POST and request.POST["bio"]:
            user_profile.bio = request.POST["bio"]

    user_model.save()
    user_profile.save()

    return render(
        request,
        "user_profile.html",
        {"user_profile": user_profile, "user_model": user_model},
    )


def contact(request):
    if request.method == "POST":
        help_detail = request.POST.get("help_detail")
        select_mode = request.POST.get("select_mode")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        company_details = request.POST.get("company_details")
        description = request.POST.get("description")

        contact_data = Contact(
            help_detail=help_detail,
            select_mode=select_mode,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            company_details=company_details,
            description=description,
        )

        contact_data.save()

        messages.success(request, "Your were details sent successfully")
        return redirect("home")
    else:
        return render(request, "contact.html")


def emp_dashboard(request):
    id = Emp_account.objects.get(user=request.user)
    print(">>>>>>>", id, id.id)
    postjob_queryset = Postjob.objects.filter(employer=id)
    postjob_ids = postjob_queryset.values_list("id", flat=True)
    print("postjob_ids : ",postjob_ids)
    applicants = Apply.objects.filter(job_id__in=postjob_ids)  # Fetch all applicants
    print("applicant : ", applicants)
    # jobs_posted_by_employer = Job.objects.filter(employer=request.user)  # Fetch jobs posted by the employer
    # applicants = Apply.objects.filter(job__in=jobs_posted_by_employer)  #
    # Assuming the employer is logged in and request.user is the employer
    # jobs_posted_by_employer = Postjob.objects.filter(employer__user=request.user)  # Fetch jobs posted by the employer
    # applicants = Apply.objects.filter(job__in=jobs_posted_by_employer)  # Fetch applicants who applied for these jobs
    # print(f'Applicants: {applicants}')

    # posted_jobs = Postjob.objects.filter(employer=request.user)

    # # Get the applications for the jobs posted by the current logged in employer
    # applications = Apply.objects.filter(job__in=posted_jobs)

    # # Get the employer's account
    # employer_account = Emp_account.objects.get(user=request.user)

    # # Get the jobs posted by the employer
    # posted_jobs = Postjob.objects.filter(employer=employer_account)

    # # Get the applications for the jobs posted by the employer
    # applications = Apply.objects.filter(job__in=posted_jobs)

    return render(request, "emp_dashboard.html", {"applicants": applicants})

    # return render(request, "emp_dashboard.html")


def applicant(request, applicant_id):
    applicant = Apply.objects.get(pk=applicant_id)  # Fetch applicant by ID
    return render(request, "applicant.html", {"applicant": applicant})

    # return render(request, "applicant.html")


# def job_detail(request, job_id):
#     # Get the job by id
#     job = Postjob.objects.get(id=job_id)

#     # Pass the job to the template
#     return render(request, 'apply_job.html', {'job': job})
