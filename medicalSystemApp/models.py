from tkinter import Image
from django.db import models
# from LoginAndRegAPP.models import *
from django.db.models import Sum
from django import forms
import bcrypt
from datetime import datetime

class usersManger(models.Manager):
    def basic_validtor(self, post_data):
        errors = {}
        if len(post_data['firstName']) < 3:
            errors["firstName"] = "First name should be at least 3 characters"
        if len(post_data['lastName']) < 2:
            errors["lastName"] = "alias should be at least 3 characters"
        # if isinstance(post_data['birthdayDate'], str):
        #     errors["birthdayDate"] = "Invalid Date"
        if datetime.today() < datetime.strptime(post_data['birthdayDate'], "%Y-%m-%d"):
            errors["birthdayDate1"] = "Birthday Date should be in the past"
        if validate_date_less_25_Years(post_data):
            errors['birthdayDate2'] = "You are under 25 years old , sorry little kid :("
        if len(post_data['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if post_data['password'] != post_data['confrimPassword']:
            errors["confrimPassword"] = "No match password"
        if Doctor.objects.filter(email=post_data['email']).exists():
            errors["email"] = "Already existsed !!!!"
        return errors

    def basic_informatiom_validator(self, postData):
        error = {}
        if len(postData['firstName']) < 1:
            error['firstName'] = "First Name should be at least 1 character"
        if len(postData['lastName']) < 1:
            error['lastName'] = "Last Name should be at least 1 character"
        if len(postData['birthDate']) < 1:
            error['birthDate'] = "Invalid Birth Date"
        if (len(postData['phone']) == 0) or (len(postData['phone']) != 10):
            error['phone'] = "Invalid Phone Number"
        return error


def validate_date_less_25_Years(post_data):
    if int(((datetime.today() - datetime.strptime(post_data['birthdayDate'], "%Y-%m-%d")).days)/365) < 25:
        return True
    return False


class Doctor(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = usersManger()

    def retrive_Doctor_by_id(id):
        return Doctor.objects.get(id=id)


def Register(request):
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    email = request.POST['email']
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    if (request.POST['confrimPassword'] == password):
        return Doctor.objects.create(firstName=firstName, lastName=lastName, email=email, password=pw_hash)


def Login(request):
    doctor = Doctor.objects.filter(email=request.POST['email'])
    if doctor:
        loged_user = doctor[0]
        if bcrypt.checkpw(request.POST['password'].encode(), loged_user.password.encode()):
            request.session['userid'] = loged_user.id
            request.session['username'] = loged_user.firstName
            return True
        else:
            request.session['LoginAuth'] = "Username or password does not exist"
            return False
    else:
        request.session['LoginAuth'] = "Username or password does not exist"
        return False



class patient(models.Model):
    patientName = models.CharField(max_length=45, null=True)
    sex = models.IntegerField()
    doctorName = models.ForeignKey(
        Doctor, related_name='doctor_id', on_delete=models.CASCADE)

    def addPatient(patientName, sex, doctorId):
        doctorName = Doctor.objects.get(id=doctorId)
        return patient.objects.create(patientName=patientName, sex=sex, doctorName=doctorName)

    def allPatients(doctor_id):
        return patient.objects.filter(doctorName=doctor_id).order_by('-id')

    def patient_by_id(id):
        return patient.objects.get(id=id)

    def delete_patient(id):
        return patient.objects.get(id=id).delete()


class basic_information(models.Model):
    lastName = models.CharField(null=True, max_length=45)
    birthDate = models.DateField(null=True)
    country = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=25, null=True)
    phone = models.IntegerField(null=True)
    underTreatment = models.IntegerField(null=True, default=0)
    treatment = models.CharField(max_length=25, null=True)
    prescriptions = models.CharField(max_length=25, null=True)
    alergies = models.CharField(max_length=25, null=True)
    pregnant = models.IntegerField(null=True, default=0)
    diseases = models.CharField(max_length=25, null=True)
    patient_info = models.ForeignKey(
        patient, related_name='patients_info', on_delete=models.CASCADE)

    objects = usersManger()

    def _update(id, firstname, lastname, birthDate, country, address, phone, underTreatment, treatment, prescriptions, alergies, pregnant, diseases):
        _basic = basic_information.objects.get(patient_info=id)
        _basic.patient_info.patientName = firstname
        _basic.lastName = lastname
        _basic.birthDate = birthDate
        _basic.country = country
        _basic.address = address
        _basic.phone = phone
        _basic.underTreatment = underTreatment
        _basic.treatment = treatment
        _basic.prescriptions = prescriptions
        _basic.alergies = alergies
        _basic.pregnant = pregnant
        _basic.diseases = diseases
        _basic.save()

    def add_basic_information(id, lastName, birthDate, country, address, phone, underTreatment, treatment, prescriptions, alergies, pregnant, diseases):
        patient_info = patient.objects.get(id=id)
        return basic_information.objects.create(lastName=lastName, birthDate=birthDate, country=country, address=address,
                                                phone=phone, underTreatment=underTreatment, treatment=treatment, prescriptions=prescriptions,
                                                alergies=alergies, pregnant=pregnant, diseases=diseases,
                                                patient_info=patient_info
                                                )

    def check_if_exsists(id):
        if (basic_information.objects.filter(patient_info=id).exists()):
            return True
        return False

    def delete_patient(id):
        return basic_information.objects.get(patient_info=id).delete()


class MidNotes(models.Model):
    description = models.CharField(max_length=45, null=True)
    createAt = models.DateField(auto_now_add=True, null=True)
    patientMidNotes = models.ForeignKey(
        patient, related_name='patients_MidNotes', on_delete=models.CASCADE)

    def addMidNotes(desc, id):
        return MidNotes.objects.create(description=desc, patientMidNotes=id)

    def check_if_exsists(id):
        if (MidNotes.objects.filter(patientMidNotes=id).exists()):
            return True
        return False

    def get_notes(id):
        return MidNotes.objects.filter(patientMidNotes=id)

    def delete_patient(id):
        return MidNotes.objects.filter(patientMidNotes=id).delete()


class billingHistory(models.Model):
    type=models.CharField(max_length=25,null=True,default='NULL')
    amount = models.IntegerField()
    description = models.CharField(max_length=45, null=True)
    createAt = models.DateField(auto_now_add=True, null=True)
    patientBillingHistory = models.ForeignKey(
        patient, related_name='patients_BillingHistory', on_delete=models.CASCADE)

    def add_billingHistory(type,amount, desc, _id):
        return billingHistory.objects.create(type=type,amount=amount, description=desc, patientBillingHistory=_id)

    def check_if_exsists(id):
        if (billingHistory.objects.filter(patientBillingHistory=id).exists()):
            return True
        return False

    def get_all_billing(id):
        return billingHistory.objects.filter(patientBillingHistory=id)

    def sum_all_billing(id):
        return billingHistory.objects.values('patientBillingHistory').order_by('patientBillingHistory').annotate(total_price=Sum('amount')).filter(patientBillingHistory=id)[0]

    def delete_patient(id):
        return billingHistory.objects.filter(patientBillingHistory=id).delete()


class photoGalleray(models.Model):
    uploadPic = models.ImageField(null=True, blank=True, upload_to="images/")
    createAt = models.DateField(auto_now_add=True, null=True)
    patientmidPhoto = models.ForeignKey(
        patient, related_name='patients_midPhoto', on_delete=models.CASCADE,default=1)

    def add_midPhoto(pic, id):
        return photoGalleray.objects.create(uploadPic=pic, patientmidPhoto=id)

    def check_if_exsists(id):
        if (photoGalleray.objects.filter(patientmidPhoto=id).exists()):
            return True
        return False

    def get_all_photos(id):
        return photoGalleray.objects.filter(patientmidPhoto=id)

    def delete_patient(id):
        return photoGalleray.objects.filter(patientmidPhoto=id).delete()


# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = photoGalleray
#         fields = ('uploadPic', 'patientPhotoGalleray')
