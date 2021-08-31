from Company.models import Offer
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import StudentInfo, IntermediateStudentStatus
from Student.models import Student, Eligibility
from . import College as CPP_College

# Create your views here.
@login_required
@user_passes_test(lambda u: u.groups.filter(name='College').exists())
def index(request):
	return render(request, 'index.html', { 'layout': 'College/layout.html' })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='College').exists())
def students(request):
	''' Displays Students Academic Information from College data '''
	students = StudentInfo.objects.all()
	return render(request, 'College/students.html', { 'layout': 'College/layout.html', 'students': students })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='College').exists())
def pending(request):
	''' Manage Pending Profiles Verification '''
	if request.method == 'POST':
		if 'prn' in request.POST:													# Manual Verification of Single Student
			verificationStatus = int(request.POST['verificationStatus'])
			prn = request.POST['prn']
			student = Student.objects.get(prn=prn)
			student.verificationStatus = verificationStatus
			student.save()
			return redirect('/college/pending')
		else:																		# Auto Verification of All Students
			c = CPP_College.College()
			updates = c.verify()
			Student.objects.filter(pk__in=updates[0]).update(verificationStatus=1)
			Student.objects.filter(pk__in=updates[1]).update(verificationStatus=2)
			return redirect('/college/pending')
	else:																			# Get Details of unverified students
		students = Eligibility.objects.select_related('studentId').filter(studentId__verificationStatus=3)
		return render(request, 'College/pending.html', { 'layout': 'College/layout.html', 'students': students })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='College').exists())
def approvals(request):
	''' Manage Placed Students Approvals '''
	if request.method == 'POST':
		if 'studentId' in request.POST:												# Manual Approval for single Student
			studentId = int(request.POST['studentId'])
			offerId = int(request.POST['offerId'])
			student = IntermediateStudentStatus.objects.select_related('studentId').get(studentId__pk=studentId)
			student.studentId.placedOffer = Offer.objects.get(pk=offerId)
			student.studentId.save()
		else:																		# Auto Approval for all Students
			c = CPP_College.College()
			c.updateStudentPlacedStatus()
		return redirect('/college/approvals')
	else:
		approvals = IntermediateStudentStatus.objects.select_related('studentId', 'offerId').filter(status__in=[1, 2], studentId__placedOffer__isnull=True)
		return render(request, 'College/approvals.html', { 'layout': 'College/layout.html', 'approvals': approvals })