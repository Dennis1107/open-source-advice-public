from django.shortcuts import render
from .models import CustomUser, ServiceOffer, ServiceAreas, ServiceTechnology, ServiceOfferTechExpert, ServiceAreasTechExpert, ServiceAreasRole
from .forms import CustomUserForm, ServiceOfferForm, CustomUserChangeForm, ServiceOfferTechExpertForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import get_template

from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site 
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text  

import cloudinary
import cloudinary.uploader
import cloudinary.api

# Create your views here.
def registered_check(user):
    """This is a decorater function. Querys the UserProfileInfo Model and checks if it is empty.
    Is used because of social authentification. When the user sings in with his linkedin account the user is already created in my database.
    But the registration process is not finished until the UserProfilInfo is filled as well. To prevent that a user can access the app before finishing
    the registration process this function checks if the user has an entry in the UserProfileInfo database.

    Parameters
    ----------
    user : str
        username of the requesting person

    Returns
    -------
    Boolean
        Returns True if the registration process is done properly
    """
    isRegistered = CustomUser.objects.filter(email=user).exists()
    return isRegistered



def registration_personal(request):
    if request.method == "POST":
        form_response = CustomUserForm(request.POST, request.FILES)

        if form_response.is_valid():
            #Save to database
            user = form_response.save()
            user.set_password(user.password)
            user.is_active = False  
            user.save()

            #Start Email Activation Workflow
            current_site = get_current_site(request)  
            mail_subject = 'Activation link open-source-advice.com'  
            message = render_to_string('seekadvice_app/registration/registration_activate_email.html', {  
                'user': user.displayname,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form_response.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.content_subtype = 'html'
            email.send()  

            return redirect('/activatemail')
        else:
            print(form_response.errors)
            user_form = CustomUserForm(data=request.POST)
            context = {
                'profile_form' : user_form,
            }
            return render(request, 'seekadvice_app/registration/registration_personal.html', context)    
    else:
        user_form = CustomUserForm()

        context = {
            'profile_form' : user_form,
        }    
        return render(request, 'seekadvice_app/registration/registration_personal.html', context)


def activate(request, uidb64, token):  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = CustomUser.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()

        # #Login imideately
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')       
        return redirect('/registerintercept') 
    else:  
        return HttpResponse('Activation link is invalid!')  

def pre_activate(request):
    if request.method == "GET":
        return render(request, 'seekadvice_app/registration/registration_activate_preActivation.html')


@login_required
def registration_service_intercept(request):
    if request.method == "GET":
        return render(request, 'seekadvice_app/registration/registration_service_intercept.html')


def faq(request):
    if request.method == "GET":
        context = {
            'faqActive' : True,
        }
        return render(request, 'seekadvice_app/others/faq.html', context)

def about(request):
    if request.method == "GET":
        context = {
            'aboutActive' : True,
        }
        return render(request, 'seekadvice_app/others/about.html', context)

def privacy(request):
    if request.method == "GET":
        context = {
            'faqActive' : True,
        }
        return render(request, 'seekadvice_app/others/privacy.html', context)

def terms(request):
    if request.method == "GET":
        context = {
            'faqActive' : True,
        }
        return render(request, 'seekadvice_app/others/terms.html', context)


@login_required
def registration_questions(request):
    if request.method == "GET":
        return render(request, 'seekadvice_app/registration/registration_questions.html')
        

def htmx_test(request):
    return render(request, 'seekadvice_app/htmx.html')

def redirect_to_login(request):
    return redirect('/login')

def htmx_check_mail(request):
    user = request.POST.get("email")
    mailExists = CustomUser.objects.filter(email=user).exists()

    if mailExists:
        return HttpResponse("<div style='color: red;'>Already in Use</div>")
    else:
        return HttpResponse("<div style='color: green;'>Looks great!</div>")


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/seekadvice') 

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        #next parameter enthält nächste Seite, wenn man direkt eine Seite aufruft
        nxt = request.POST.get("next")

        user = authenticate(email=email, password=password)
        #User wird authentifiziert

        if user:
            if user.is_active:
                login(request,user)

                if (nxt == "") or (nxt == None):
                    return redirect('/seekadvice')
                else:
                    return HttpResponseRedirect(nxt)                    
            else:
                return render(request, 'seekadvice_app/registration/login.html', {'error_message': 'User is not active anymore'})
        else:
            #return HttpResponse("LOGIN FAILED")
            return render(request, 'seekadvice_app/registration/login.html', {'error_message': 'User or Password invalid'})
    else:
        return render(request, 'seekadvice_app/registration/login.html', {})

@login_required
def app_home(request):
    context = {
        'userObject' : request.user,
        'homeActive' : True
    }
    return render(request, 'seekadvice_app/app_home.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('/login')


def seekadvice_list_helper(request, serviceOfferType):
    """Querys database column depending on serviceOfferType

    Args:
        request (GET): user request
        serviceOfferType (str): Containing either OpenSource or TechExpert

    Returns:
        dict: context variable
    """
    if(serviceOfferType == "OpenSource"):
        serviceOffers = ServiceOffer.objects.all()
        servicetype = "Open Source Packages"
        htmxPostURL = "/seekadviceupdate"
        addMeURL = "/selfseekadvice"
        isSeekAdviceActive = True
        isTechExpertsActive = False
    else:
        serviceOffers = ServiceOfferTechExpert.objects.all()
        servicetype = "Areas"
        htmxPostURL = "/seekadvicetechexpertsupdate"
        addMeURL = "/selfseekadvicetechexperts"
        isSeekAdviceActive = False
        isTechExpertsActive = True

    paginator = Paginator(serviceOffers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'userObject' : request.user,
        'serviceOffers' : page_obj,
        'seekAdviceActive' : isSeekAdviceActive,
        'techExpertsActive': isTechExpertsActive,
        'emptyQuery' : "",
        'servicetype' : servicetype,
        'htmxPostURL' : htmxPostURL,
        'addMeURL': addMeURL
    }
    return context



def seekadvice_list(request):
    context = seekadvice_list_helper(request=request, serviceOfferType="OpenSource")
    return render(request, 'seekadvice_app/seekadvice.html', context)

def seekadvice_list_techexpert(request):
    context = seekadvice_list_helper(request=request, serviceOfferType="TechExpert")
    return render(request, 'seekadvice_app/seekadvice.html', context)


def seekadvice_list_update_htmx_helper(request, serviceOfferType):
    searchquery = request.POST.get("searchquery")

    if(serviceOfferType == "OpenSource"):
        servicetype = "Open Source Packages"
        if searchquery != "":
            serviceOffers = ServiceOffer.objects.filter(
                Q(user_service_areas__serviceareas__icontains=searchquery) | Q(user_service_technology__servicetechnology__icontains=searchquery)
                ).distinct()
        else:
            serviceOffers = ServiceOffer.objects.all()
    else:
        servicetype = "Areas"
        if searchquery != "":
            serviceOffers = ServiceOfferTechExpert.objects.filter(
                Q(user_service_areas__serviceareas__icontains=searchquery) | Q(user_service_technology__servicetechnology__icontains=searchquery)
                ).distinct()
        else:
            serviceOffers = ServiceOfferTechExpert.objects.all()
    
    
    if len(serviceOffers) == 0:
        emptyQuery = "Nothing found. Try another search query!"
    else:
        emptyQuery = ""


    context = {
        'userObject' : request.user,
        'serviceOffers' : serviceOffers,
        'emptyQuery': emptyQuery,
        'servicetype' : servicetype
    }
    return context


def seekadvice_list_update_htmx(request):
    context = seekadvice_list_update_htmx_helper(request=request, serviceOfferType="OpenSource")
    return render(request, 'seekadvice_app/searchSeekAdvice.html', context)

def seekadvice_list_update_htmx_techexpert(request):
    context = seekadvice_list_update_htmx_helper(request=request, serviceOfferType="TechExpert")
    return render(request, 'seekadvice_app/searchSeekAdvice.html', context)




@login_required
def change_personal(request):
    if request.method == "POST":
        userObjectInstance = CustomUser.objects.get(email=request.user)

        if 'user_avatar' in request.FILES:
            form_response = CustomUserChangeForm(request.POST, request.FILES, instance=userObjectInstance)
            try:
                print("Deleted")                
                cloudinary.uploader.destroy(userObjectInstance.user_avatar.public_id, invalidate=True)
            except:
                pass
        else:
            form_response = CustomUserChangeForm(request.POST, instance=userObjectInstance)


        if form_response.is_valid():
            form_response.save()            
            return redirect('/seekadvice')
        else:
            context = {
                'profile_form' : form_response,
            }
            return render(request, 'seekadvice_app/registration/registration_personal.html', context)    
    else:
        userObjectInstance = CustomUser.objects.get(email=request.user)
        user_form = CustomUserChangeForm(instance=userObjectInstance)
        context = {
            'profile_form' : user_form,
        }    
        return render(request, 'seekadvice_app/personal/change_personal.html', context)



def helper_register(request, post_return_template, post_error_return_template, get_return_template):
    #Existing entries
    serviceAreasObjects = ServiceAreas.objects.all()
    serviceAreasList = list(serviceAreasObjects.values_list('serviceareas', flat=True))

    serviceTechnologyObjects = ServiceTechnology.objects.all()
    serviceTechnologyList = list(serviceTechnologyObjects.values_list('servicetechnology', flat=True))


    if request.method == "POST":
        current_user = request.user
        serviceObject = ServiceOffer.objects.filter(user=current_user)
        serviceAlreadyExists = serviceObject.exists()

        #alreay existing entries
        maintainerObject = ServiceOffer.objects.filter(serviceareasrole__role = "Maintainer", user=request.user)
        user_areas_maintainer = list(maintainerObject.values_list('user_service_areas__serviceareas', flat=True))
        contributorObject = ServiceOffer.objects.filter(serviceareasrole__role = "Contributor", user=request.user)
        user_areas_contributor = list(contributorObject.values_list('user_service_areas__serviceareas', flat=True))
        expertObject = ServiceOffer.objects.filter(serviceareasrole__role = "Expert", user=request.user)
        user_areas_expert = list(expertObject.values_list('user_service_areas__serviceareas', flat=True))
        
        allAreasObject = ServiceOffer.objects.filter(user=request.user)
        user_areas_all = list(allAreasObject.values_list('user_service_areas__serviceareas', flat=True))
        user_technologies_all = list(allAreasObject.values_list('user_service_technology__servicetechnology', flat=True))



        #New entry of form
        requestServiceAreasMaintainer = request.POST.getlist('serviceareas')
        requestServiceAreasContributor = request.POST.getlist('serviceareas2')
        requestServiceAreasExperts = request.POST.getlist('serviceareas3')
        requestServiceAreasAll = requestServiceAreasMaintainer + requestServiceAreasContributor + requestServiceAreasExperts
        requestServiceTechnology = request.POST.getlist('servicetechnology')

        if serviceAlreadyExists:
            serviceObjectInstance = ServiceOffer.objects.get(user=request.user)
            form_response = ServiceOfferForm(data=request.POST, instance=serviceObjectInstance)
        else:
            form_response = ServiceOfferForm(data=request.POST)

        if form_response.is_valid():
            service_form = form_response.save(commit=False)
            service_form.user = current_user
            service_form.save()

            #Technology löschen
            for item in user_technologies_all:
                if ((item not in requestServiceTechnology) and (item != None)):
                    origin_object = ServiceOffer.objects.get(user=request.user)
                    remove_object = ServiceTechnology.objects.get(servicetechnology=item)
                    origin_object.user_service_technology.remove(remove_object)

            #Zuerst alle löschen, die nicht requestet werden
            for item in user_areas_all:
                if ((item not in requestServiceAreasAll) and (item != None)):
                    origin_object = ServiceOffer.objects.get(user=request.user)
                    remove_object = ServiceAreas.objects.get(serviceareas=item)
                    origin_object.user_service_areas.remove(remove_object)

            #Expert löschen
            for item in user_areas_expert:
                if ((item in requestServiceAreasMaintainer) or (item in requestServiceAreasContributor) or (item not in requestServiceAreasExperts)):
                    origin_object = ServiceOffer.objects.get(user=request.user)
                    remove_object = ServiceAreas.objects.get(serviceareas=item)
                    origin_object.user_service_areas.remove(remove_object)

            #Contributor löschen
            for item in user_areas_contributor:
                if ((item in requestServiceAreasMaintainer) or (item not in requestServiceAreasContributor)):
                    origin_object = ServiceOffer.objects.get(user=request.user)
                    remove_object = ServiceAreas.objects.get(serviceareas=item)
                    origin_object.user_service_areas.remove(remove_object)

            #Maintainer löschen
            for item in user_areas_maintainer:
                if ((item not in requestServiceAreasMaintainer)):
                    origin_object = ServiceOffer.objects.get(user=request.user)
                    remove_object = ServiceAreas.objects.get(serviceareas=item)
                    origin_object.user_service_areas.remove(remove_object)


            #Wenn jemand ein Package mehrmals eingibt gilt: Maintainer > Contributor > Expert
            #Maintainer
            for item in requestServiceAreasMaintainer:
                print(item, "is added to maintainer")
                if item not in serviceAreasList:
                    newServiceArea = ServiceAreas.objects.create(serviceareas=item)
                else:
                    newServiceArea = ServiceAreas.objects.get(serviceareas=item)
                service_form.user_service_areas.add(newServiceArea, through_defaults={'role': 'Maintainer'})

            #Contributor
            for item in requestServiceAreasContributor:
                print(item, "is added to contributor")
                if item not in serviceAreasList:
                    newServiceArea = ServiceAreas.objects.create(serviceareas=item)
                else:
                    newServiceArea = ServiceAreas.objects.get(serviceareas=item)
                service_form.user_service_areas.add(newServiceArea, through_defaults={'role': 'Contributor'})

            #Expert
            for item in requestServiceAreasExperts:
                if item not in serviceAreasList:
                    newServiceArea = ServiceAreas.objects.create(serviceareas=item)
                else:
                    newServiceArea = ServiceAreas.objects.get(serviceareas=item)
                service_form.user_service_areas.add(newServiceArea, through_defaults={'role': 'Expert'})   

            for item in requestServiceTechnology:
                if item not in serviceTechnologyList:
                    newServiceTechnology = ServiceTechnology.objects.create(servicetechnology=item)
                else:
                    newServiceTechnology = ServiceTechnology.objects.get(servicetechnology=item)
                service_form.user_service_technology.add(newServiceTechnology)
            return redirect(post_return_template)
        else:
            user_form = ServiceOfferForm(data=request.POST)
            context = {
                'profile_form' : user_form,
                'service_areas_list' : serviceAreasList,
                'service_technology_list' : serviceTechnologyList,
            }    
            return render(request, post_error_return_template, context)    
    else:
        current_user = request.user
        serviceObject = ServiceOffer.objects.filter(user=current_user)
        serviceAlreadyExists = serviceObject.exists()

        if serviceAlreadyExists:
            serviceObjectInstance = ServiceOffer.objects.get(user=request.user)
            user_form = ServiceOfferForm(instance=serviceObjectInstance)

            maintainerObject = ServiceOffer.objects.filter(serviceareasrole__role = "Maintainer", user=request.user)
            selected_areas_maintainer = list(maintainerObject.values_list('user_service_areas__serviceareas', flat=True))

            contributorObject = ServiceOffer.objects.filter(serviceareasrole__role = "Contributor", user=request.user)
            selected_areas_contributor = list(contributorObject.values_list('user_service_areas__serviceareas', flat=True))

            expertObject = ServiceOffer.objects.filter(serviceareasrole__role = "Expert", user=request.user)
            selected_areas_expert = list(expertObject.values_list('user_service_areas__serviceareas', flat=True))
            
            selected_technologies = list(serviceObject.values_list('user_service_technology__servicetechnology', flat=True))
        else:
            user_form = ServiceOfferForm()
            selected_areas_maintainer = []
            selected_areas_contributor = []
            selected_areas_expert = []
            selected_technologies = []


        context = {
            'profile_form' : user_form,
            'service_areas_list' : serviceAreasList,
            'service_technology_list' : serviceTechnologyList,
            'selected_areas_maintainer' : selected_areas_maintainer,
            'selected_areas_contributor' : selected_areas_contributor,
            'selected_areas_expert' : selected_areas_expert,
            'selected_technologies' : selected_technologies
        }    
        return render(request, get_return_template, context)


@login_required
def registration_service(request):
     return helper_register(
       request=request, 
       post_return_template="/seekadvice", 
       post_error_return_template="seekadvice_app/registration/registration_service.html", 
       get_return_template="seekadvice_app/registration/registration_service.html"
    )

@login_required
def self_seekadvice(request):
   return helper_register(
       request=request, 
       post_return_template="/seekadvice", 
       post_error_return_template="seekadvice_app/personal/self_seekadvice.html", 
       get_return_template="seekadvice_app/personal/self_seekadvice.html"
       )


@login_required
def self_seekadvice_techexpert(request):
    #Existing entries
    serviceAreasObjects = ServiceAreasTechExpert.objects.all()
    serviceAreasList = list(serviceAreasObjects.values_list('serviceareas', flat=True))

    serviceTechnologyObjects = ServiceTechnology.objects.all()
    serviceTechnologyList = list(serviceTechnologyObjects.values_list('servicetechnology', flat=True))


    if request.method == "POST":
        current_user = request.user
        serviceObject = ServiceOfferTechExpert.objects.filter(user=current_user)
        serviceAlreadyExists = serviceObject.exists()
        
        
        #New entry of form
        requestServiceAreas = request.POST.getlist('serviceareas')
        requestServiceTechnology = request.POST.getlist('servicetechnology')

        if serviceAlreadyExists:
            serviceObjectInstance = ServiceOfferTechExpert.objects.get(user=request.user)
            form_response = ServiceOfferTechExpertForm(data=request.POST, instance=serviceObjectInstance)
        else:
            form_response = ServiceOfferTechExpertForm(data=request.POST)

        if form_response.is_valid():
            service_form = form_response.save(commit=False)
            service_form.user = current_user
            service_form.save()

            for item in requestServiceAreas:
                if item not in serviceAreasList:
                    newServiceArea = ServiceAreasTechExpert.objects.create(serviceareas=item)
                else:
                    newServiceArea = ServiceAreasTechExpert.objects.get(serviceareas=item)
                service_form.user_service_areas.add(newServiceArea)

            for item in requestServiceTechnology:
                if item not in serviceTechnologyList:
                    newServiceTechnology = ServiceTechnology.objects.create(servicetechnology=item)
                else:
                    newServiceTechnology = ServiceTechnology.objects.get(servicetechnology=item)
                service_form.user_service_technology.add(newServiceTechnology)
            return redirect('/seekadvicetechexperts')
        else:
            user_form = ServiceOfferTechExpertForm(data=request.POST)
            context = {
                'profile_form' : user_form,
                'service_areas_list' : serviceAreasList,
                'service_technology_list' : serviceTechnologyList,
            }    
            return render(request, 'seekadvice_app/personal/self_seekadvice.html', context)    
    else:
        current_user = request.user
        serviceObject = ServiceOfferTechExpert.objects.filter(user=current_user)
        serviceAlreadyExists = serviceObject.exists()

        if serviceAlreadyExists:
            serviceObjectInstance = ServiceOfferTechExpert.objects.get(user=request.user)
            user_form = ServiceOfferTechExpertForm(instance=serviceObjectInstance)

            selected_areas = list(serviceObject.values_list('user_service_areas__serviceareas', flat=True))
            selected_technologies = list(serviceObject.values_list('user_service_technology__servicetechnology', flat=True))
        else:
            user_form = ServiceOfferTechExpertForm()
            selected_areas = []
            selected_technologies = []


        context = {
            'profile_form' : user_form,
            'service_areas_list' : serviceAreasList,
            'service_technology_list' : serviceTechnologyList,
            'selected_areas' : selected_areas,
            'selected_technologies' : selected_technologies
        }    
        return render(request, 'seekadvice_app/personal/self_seekadvice.html', context)



@login_required
def delete_user(request):
    current_user = request.user
    try:
        user_profile_data = CustomUser.objects.get(email=current_user)
        try:
            cloudinary.uploader.destroy(user_profile_data.user_avatar.public_id,invalidate=True)
        except:
            pass

        user_profile_data.delete()
        return redirect('/login')
    except Exception as e:
        print(e)
        return redirect('/home')






@login_required
@user_passes_test(registered_check)
def send_request_message(request):
    current_user = request.user
    senderName = current_user.displayname
    senderId = current_user.id
    #senderProfileURL = f"https://open-source-advice.com/userprofile/username{senderId}/"
    senderProfileURL = f'<html><a href="https://open-source-advice.com/userprofile/username{senderId}/">W3Schools</a></html>'


    serviceOfferId = int(request.POST.get('soid'))
    serviceType = request.POST.get('servicetype')
    sendMessage = request.POST.get('sendMessage')

    #ServiceType could be either "Open Source Packages" or "Areas"
    if (serviceType == "Open Source Packages"):
        return_url = "/seekadvice"
        recipientServiceOffer = ServiceOffer.objects.get(id=serviceOfferId)
    else:
        return_url = "/seekadvicetechexperts"
        recipientServiceOffer = ServiceOfferTechExpert.objects.get(id=serviceOfferId)

    
    recipientMail = recipientServiceOffer.user.email
    recipientName = recipientServiceOffer.user.displayname


    context = {
        'recipientName': recipientName,
        'senderName': senderName,
        'senderId' : senderId,
        'sendMessage' : sendMessage
    }
    message = get_template('seekadvice_app/personal/contact_email.html').render(context)

    try:
        email = EmailMessage(
            'open-source-advice.com - Request',
            message,
            'info@open-source-advice.com',
            [recipientMail],
            reply_to=[current_user],
        )
        email.content_subtype = 'html'
        email.send()
    except Exception as e:
        print("Error", e)
    
    return redirect(return_url)


@login_required
@user_passes_test(registered_check)
def show_user_profile(request, username_id):
    if request.method == "GET":
        search_user = username_id[9:]
        user_profile_info = CustomUser.objects.get(id=search_user)

        context = {
            'userObject': user_profile_info, 
        }
        return render(request, 'seekadvice_app/user_details.html', context)


@login_required
@user_passes_test(registered_check)
def show_service_offer(request, serviceoffer_id):
    if request.method == "GET":
        search_serviceoffer = serviceoffer_id[3:]
        serviceOffers = ServiceOffer.objects.filter(id=search_serviceoffer)

        context = {
            'serviceOffers': serviceOffers,
            'servicetype' : "Open Source Packages" 
        }
        return render(request, 'seekadvice_app/serviceOfferDetails.html', context)