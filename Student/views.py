from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student, Eligibility
from Company.models import Offer
from College.models import IntermediateStudentStatus
from . import Student as CPP_Student
from . import Eligibility as CPP_Eligibility

# Create your views here.
@login_required																	# Check if user is logged in
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())			# and the user is a student
def index(request):
	return render(request, 'index.html', { 'layout': 'Student/layout.html' })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())
def profile(request):
	''' Handles Student Profile Management '''
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		dob = request.POST['dob']
		prn = request.POST['prn']
		department = request.POST['department']									# For a POST request, extract all the
		phoneNumber = request.POST['phoneNumber']								# personal and academic details of
		email = request.POST['email']											# student from the form data
		cgpa = float(request.POST['cgpa'])
		liveBacklog = int(request.POST['liveBacklog'])
		deadBacklog = int(request.POST['deadBacklog'])
		passingYear = int(request.POST['passingYear'])
		yearGap = int(request.POST['yearGap'])
		skillSet = request.POST['skillSet']
		user = User.objects.get(pk=request.user.pk)								# Get the User from database and update
		user.first_name = first_name											# the relevant fields and save it to db
		user.last_name = last_name
		user.email = email
		user.save()
		profile = Student.objects.get(studentId=request.user)					# Get the Student info of current
		profile.dob = parse_date(dob)											# student and update the relevant fields
		profile.prn = prn														# and save the updates to database
		profile.department = department											# and save the updates to database
		profile.phoneNumber = phoneNumber
		profile.verificationStatus = 3
		profile.save()
		academic = Eligibility.objects.get(studentId=profile)					# Get the Eligibility info of current
		academic.cgpa = cgpa													# student and update the relevant fields
		academic.passingYear = passingYear										# and save the updates to database
		academic.yearGap = yearGap
		academic.liveBacklog = liveBacklog
		academic.deadBacklog = deadBacklog
		academic.skillSet = skillSet
		academic.save()
		return render(request, 'Student/profile.html', { 'layout': 'Student/layout.html', 'profile': profile, 'academic': academic })
	else:
		profile = Student.objects.get(studentId=request.user)					# Get the Student's Personal and
		academic = Eligibility.objects.get(studentId=profile)					# Academic info to display on profile
		return render(request, 'Student/profile.html', { 'layout': 'Student/layout.html', 'profile': profile, 'academic': academic })

@login_required																	# Check if user is logged in
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())			# and the user is a student
def available(request):
	profile = Student.objects.get(studentId=request.user)						# Get the Student's Personal info
	visible = ''
	offers = None
	if profile.placedOffer is not None:
		visible = 'You cannot view Offers as you are already Placed!'
	if profile.verificationStatus == 1:
		academic = Eligibility.objects.get(studentId=profile)					# Academic info to display on profile
		e = CPP_Eligibility.Eligibility(academic.cgpa, academic.liveBacklog, academic.deadBacklog ,academic.passingYear ,academic.yearGap ,academic.skillSet)
		s = CPP_Student.Student(
			request.user.first_name+' '+request.user.last_name,
			profile.id,															# Create student object (CPP) to
			request.user.email,													# use the CPP side logic for listing
			profile.phoneNumber,												# out offers for which the Student is
			str(profile.dob),													# Eligible according to the company
			profile.department,													# criteria
			e
		)
		offerids = s.getApplicableOffers()
		offers = Offer.objects.filter(pk__in=offerids).select_related('companyId')
		if request.method == 'POST':
			offerId = int(request.POST['offerId'])								# Apply for an offer as per Student's
			s.apply(offerId)													# selection, from the POST request
			return redirect('/student/applied/')
	else:
		visible = 'You can view Available Offers only after your Profile gets Verified'
	return render(request, 'Student/available.html', { 'layout': 'Student/layout.html', 'visible': visible, 'offers': offers })

@login_required																	# Check if user is logged in
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())			# and the user is a student
def applied(request):
	profile = Student.objects.get(studentId=request.user)						# Get the Student's Personal and
	visible = False
	offers = None
	if profile.verificationStatus == 1:
		visible = True
		offers = IntermediateStudentStatus.objects.filter(studentId=profile).select_related('offerId')
	return render(request, 'Student/applied.html', { 'layout': 'Student/layout.html', 'visible': visible, 'offers': offers })