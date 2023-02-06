from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages


def dashboard(request):
    if not 'userid' in request.session:
        return redirect('/')
    hospital_id = request.session['userid']
    if request.method == 'POST':
        patientName = request.POST['patientName']
        sex = int(request.POST['sex'])
        patient.addPatient(patientName, sex, hospital_id)
        return redirect('/dashboard')
    else:
        context = {
            'all_patient': patient.objects.filter(doctorName=hospital_id).order_by('-id')
        }
        return render(request, 'home.html', context=context)


def basicInfo(request, id):
    if not 'userid' in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = basic_information.objects.basic_informatiom_validator(
            request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/dashboard/basicInfo/{id}')
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        birthDate = request.POST['birthDate']
        country = request.POST['country']
        address = request.POST['address']
        phone = int(request.POST['phone'])
        underTreatment = int(request.POST.get('underTreatment', False))
        treatment = request.POST['treatment']
        prescriptions = request.POST['prescriptions']
        alergies = request.POST['alergies']
        pregnant = int(request.POST.get('pregnant', False))
        diseases = request.POST['diseases']
        id = int(id)
        if (basic_information.check_if_exsists(id)):
            basic_information._update(id, firstName, lastName, birthDate, country, address,
                                      phone, underTreatment, treatment, prescriptions, alergies, pregnant, diseases)
        else:
            basic_information.add_basic_information(
                id, lastName, birthDate, country, address, phone, underTreatment, treatment, prescriptions, alergies, pregnant, diseases)
        return redirect('/dashboard')
    else:
        if (basic_information.check_if_exsists(id)):
            context = {
                'patient_id': patient.patient_by_id(id),
                'basic_information': basic_information.objects.filter(patient_info=id)[0]
            }
        else:
            context = {
                'patient_id': patient.patient_by_id(id),
                'basic_information': {}
            }
        return render(request, 'basic_info.html', context=context)


def MidNote(request, id):
    if not 'userid' in request.session:
        return redirect('/')
    if request.method == 'POST':
        desc = request.POST['desc']
        _id = patient.patient_by_id(id)
        MidNotes.addMidNotes(desc, _id)
        return redirect(f'/MidNotes/{id}')
    else:
        if (MidNotes.check_if_exsists(id)):
            context = {
                'id': id,
                'allNotes': MidNotes.get_notes(id)
            }
        else:
            context = {
                'id': id,
                'allNotes': {}
            }
        return render(request, 'MidNotes.html', context=context)


def billing_History(request, id):
    if not 'userid' in request.session:
        return redirect('/')
    if request.method == 'POST':
        type = int(request.POST.get('type', False))
        if type == 1:
            amount = int(request.POST['amount'])
            type='Cash'
            desc = request.POST['details']
            _id = patient.patient_by_id(id)
            billingHistory.add_billingHistory(type,amount, desc, _id)
        else:
            amount=0
            type='Private Insurance'
            desc=request.POST['details1']
            _id = patient.patient_by_id(id)
            billingHistory.add_billingHistory(type,amount, desc, _id)
        return redirect(f'/billingHistory/{id}')
    else:
        if (billingHistory.check_if_exsists(id)):
            context = {
                'id': id,
                'allBilling': billingHistory.get_all_billing(id),
                'Total2': billingHistory.sum_all_billing(id)
            }
        else:
            context = {
                'id': id,
                'allBilling': {}
            }
        return render(request, 'billingHistory.html', context=context)


def midPhoto(request, id):
    if not 'userid' in request.session:
        return redirect('/')
    if request.method == 'POST':
        pic = request.FILES['uploadPic']
        _id = patient.patient_by_id(id)
        photoGalleray.add_midPhoto(pic, _id,)
        return redirect(f'/midPhoto/{id}')
    else:
        if (photoGalleray.check_if_exsists(id)):
            context = {
                'id': id,
                'allPhoto': photoGalleray.get_all_photos(id),
            }
        else:
            context = {
                'id': id,
                'allPhoto': {}
            }
        return render(request, 'photoGallery.html', context=context)


def search(request):
    if not 'userid' in request.session:
        return redirect('/')
    if request.method == 'POST':
        doctor_id = request.session['userid']
        name = str(request.POST['search2'])
        if (patient.objects.filter(patientName__startswith=name).exists()):
            context = {
                'all_patient': patient.allPatients(doctor_id).filter(patientName__startswith=name)
            }
        else:
            context = {
                'all_patient': patient.allPatients(doctor_id)
            }
        return render(request, 'home.html', context=context)


def delete(request, id):
    if not 'userid' in request.session:
        return redirect('/')
    _id = patient.patient_by_id(id)
    if (photoGalleray.check_if_exsists(id)):
        photoGalleray.delete_patient(_id)
    if (MidNotes.check_if_exsists(id)):
        MidNotes.delete_patient(_id)
    if (billingHistory.check_if_exsists(id)):
        billingHistory.delete_patient(_id)
    if (basic_information.check_if_exsists(id)):
        basic_information.delete_patient(_id)
    patient.delete_patient(id)

    return redirect('/dashboard')


def destroy(request):
    del request.session['userid']
    del request.session['LoginAuth']
    return redirect('/')



def form_page(request):
    if request.method == 'GET':
        if 'LoginAuth' in request.session:
            return render(request, 'index.html')
    request.session['LoginAuth'] = ''
    return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        errors = Doctor.objects.basic_validtor(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        Register(request)
    return redirect('/')


def login(request):
    if request.method == "POST":
        if Login(request):
            return redirect('/dashboard')
        else:
            return redirect('/')

def clear(request):
    del request.session['LoginAuth']
    del request.session['userid']
    return redirect('/')
