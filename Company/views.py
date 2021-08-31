from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.dateparse import parse_date
from .models import Company, Offer, Criteria
from College.models import IntermediateStudentStatus

# Create your views here.
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def index(request):
	return render(request, 'index.html', { 'layout': 'Company/layout.html' })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def offers(request):
	''' Manage Offers(JDs) by Company '''
	if request.method == 'POST':
		jobRole = request.POST['jobRole']
		jobLocation = request.POST['jobLocation']
		bond = int(request.POST['bond'])
		deadline = parse_date(request.POST['deadline'])								# Extract the Offer and its Criteria
		package = int(request.POST['package'])										# info from the form data and create
		cgpa = float(request.POST['cgpa'])											# respective Offer and Criteria objects
		liveBacklog = int(request.POST['liveBacklog'])								# and save both to database
		deadBacklog = int(request.POST['deadBacklog'])
		passingYear = int(request.POST['passingYear'])
		yearGap = int(request.POST['yearGap'])
		skillSet = request.POST['skillSet']
		company = Company.objects.get(companyId=request.user)
		offer = Offer.objects.create(companyId=company, jobRole=jobRole, jobLocation=jobLocation, bond=bond, deadline=deadline, package=package)
		offer.save()
		criteria = Criteria.objects.create(offerId=offer, cgpa=cgpa, liveBacklog=liveBacklog, deadBacklog=deadBacklog, passingYear=passingYear, yearGap=yearGap, skillSet=skillSet)
		criteria.save()
		offers = Criteria.objects.select_related('offerId')							# Inner Join between Offer and Criteria
		return render(request, 'Company/offers.html', { 'layout': 'Company/layout.html', 'offers': offers })
	else:
		offers = Criteria.objects.select_related('offerId')							# Inner Join between Offer and Criteria
		return render(request, 'Company/offers.html', { 'layout': 'Company/layout.html', 'offers': offers })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def enrollments(request):
	''' Lists Students Enrolled for Company Drive '''
	company = Company.objects.get(companyId=request.user)
	offers = Offer.objects.filter(companyId=company).values_list('id', flat=True)
	enrollments = IntermediateStudentStatus.objects.filter(offerId__in=offers).select_related('studentId')
	return render(request, 'Company/enrollments.html', { 'layout': 'Company/layout.html', 'enrollments': enrollments })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def results(request):
	''' Inform Drive Results to College '''
	if request.method == 'POST':
		studentId = int(request.POST['studentId'])
		status = int(request.POST['status'])
		student = IntermediateStudentStatus.objects.select_related('studentId').get(studentId__id=studentId)
		student.status = status
		student.save()
		return redirect('/company/results/')
	else:
		company = Company.objects.get(companyId=request.user)
		offers = Offer.objects.filter(companyId=company).values_list('id', flat=True)
		enrollments = IntermediateStudentStatus.objects.filter(offerId__in=offers, status=0).select_related('studentId')
		return render(request, 'Company/results.html', { 'layout': 'Company/layout.html', 'enrollments': enrollments })