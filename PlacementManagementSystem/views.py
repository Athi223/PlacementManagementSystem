from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from Student.models import Student, Eligibility
from Company.models import Company

# Create your views here.
def index(request):
	''' Handles homepage rendering/redirection '''
	user_group = request.user.groups
	if user_group.filter(name='Student').exists():									# Redirect to respective Index(Home)
		return redirect('/student')													# page based on user group,
	if user_group.filter(name='College').exists():									# i.e. Student, College, Company.
		return redirect('/college')
	if user_group.filter(name='Company').exists():
		return redirect('/company')													# Or render the guest Index page if no
	return render(request, 'index.html', { 'error': '', 'layout': 'layout.html' })	# user is logged in

def signin(request):
	''' Handles Login/Registration and Setting Session '''
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		if 'user_group' in request.POST:											# Existence of 'user_group' in request
			if username and password:												# indicates Registration scenario
				user, created = User.objects.get_or_create(username=username)		# Check if input username already exists
				if created:															# If it doesnt, set the input password
					user.set_password(password)										# for newly created user and save to db
					user.save()
					if request.POST['user_group'] == 'Student':
						student = Student.objects.create(studentId=user)			# If the newly created User is a
						student.save()												# Student, create correspoding
						eligiblity = Eligibility.objects.create(studentId=student)	# 'Student' and 'Eligibility'
						eligiblity.save()											# objects and save to the database
					elif request.POST['user_group'] == 'College':
						pass
					elif request.POST['user_group'] == 'Company':
						Company.objects.create(companyId=user).save()
					user_group = Group.objects.get(name=request.POST['user_group']) # Add the new user to respective group
					user_group.user_set.add(user)									# according to 'user_group' key from
					login(request, user)											# the request. Also Log the user in
					return redirect('/')
				else:																# Show relevant message if User exists
					return render(request, 'index.html', { 'error': 'User already exists', 'layout': 'layout.html' })
		else:
			user = authenticate(request, username=username, password=password)		# No 'user_group' indicates a Login
			if user is not None:													# scenario. Try to authenticate the
				login(request, user)												# input credentials and login the user
				return redirect('/')												# if authenticated.
			else:																	# Else, show relevant message
				return render(request, 'index.html', { 'error': 'Invalid Credentials', 'layout': 'layout.html' })
	else:
		return redirect('/')														# A GET request will redirect to Index

def signout(request):
	''' Handles Logout and Clearing Session '''
	logout(request)																	# Log the user out and redirect to Index
	return redirect('/')