from django import forms
from .models import CustomUser, ServiceTechnology, ServiceAreas, ServiceOffer, ServiceOfferTechExpert
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from cloudinary.forms import CloudinaryFileField  


class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'style':'text-transform: lowercase;','class' : 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md'}))
    user_avatar = CloudinaryFileField(
        label = "Profile Picture",        
        options = {
            'crop': 'thumb',
            'width': 200,
            'height': 200,
            'allowed_formats': ['jpg', 'png'],
            'folder': 'seekadviceImages',
            'tags': "directly_uploaded",
       },
    )
    user_avatar.widget.attrs.update({'class': 'ml-5 bg-white py-2 px-3 border border-gray-300 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'})
    class Meta():
        model = CustomUser
        fields = ['displayname', 'email', 'password','jobtitle', 'short_description', 'linkedin_name', 'github_name', 'user_avatar']

        widgets = {
            'displayname': forms.TextInput(attrs={'class' : 'flex-1 block w-full focus:ring-indigo-500 focus:border-indigo-500 min-w-0 rounded-none rounded-r-md sm:text-sm border-gray-300'}),
            'jobtitle': forms.TextInput(attrs={'placeholder' : 'e.g. Data Scientist @ Amazon','class' : 'flex-1 block w-full focus:ring-indigo-500 focus:border-indigo-500 min-w-0 rounded-none rounded-r-md sm:text-sm border-gray-300'}),
            'short_description' : forms.Textarea(attrs={'rows':3, 'placeholder' : 'Write a few sentences about yourself.', 'class' : 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border border-gray-300 rounded-md'}),
            'linkedin_name' : forms.TextInput(attrs={'class': 'flex-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full min-w-0 rounded-none rounded-r-md sm:text-sm border-gray-300'}),
            'github_name' : forms.TextInput(attrs={'class': 'flex-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full min-w-0 rounded-none rounded-r-md sm:text-sm border-gray-300'})
        }

        
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = True
        self.fields['email'].required = True
        self.fields['displayname'].required = True
        self.fields['jobtitle'].required = False
        self.fields['short_description'].required = False
        self.fields['linkedin_name'].required = False
        self.fields['github_name'].required = False
        self.fields['user_avatar'].required = False


class CustomUserChangeForm(forms.ModelForm):
    user_avatar = CloudinaryFileField(
        label = "Profile Picture",        
        options = {
            'crop': 'thumb',
            'width': 200,
            'height': 200,
            'allowed_formats': ['jpg', 'png'],
            'folder': 'seekadviceImages',
            'tags': "directly_uploaded",
       },
    )
    user_avatar.widget.attrs.update({'class': 'ml-5 bg-white py-2 px-3 border border-gray-300 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'})
    class Meta():
        model = CustomUser
        fields = ['displayname','jobtitle', 'short_description', 'linkedin_name', 'github_name', 'user_avatar']

        widgets = {
            'displayname': forms.TextInput(attrs={'class' : 'flex-1 block w-full focus:ring-indigo-500 focus:border-indigo-500 min-w-0 rounded-none rounded-r-md sm:text-sm border-gray-300'}),
            'jobtitle': forms.TextInput(attrs={'placeholder' : 'e.g. Data Scientist @ Amazon','class' : 'flex-1 block w-full focus:ring-indigo-500 focus:border-indigo-500 min-w-0 rounded-none rounded-r-md sm:text-sm border-gray-300'}),
            'short_description' : forms.Textarea(attrs={'rows':3, 'placeholder' : 'Write a few sentences about yourself.', 'class' : 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border border-gray-300 rounded-md'}),
            'linkedin_name' : forms.TextInput(attrs={'class': 'flex-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full min-w-0 rounded-none rounded-r-md sm:text-sm border-gray-300'}),
            'github_name' : forms.TextInput(attrs={'class': 'flex-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full min-w-0 rounded-none rounded-r-md sm:text-sm border-gray-300'})
        }
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['displayname'].required = True
        self.fields['jobtitle'].required = False
        self.fields['short_description'].required = False
        self.fields['linkedin_name'].required = False
        self.fields['github_name'].required = False
        self.fields['user_avatar'].required = False

class ServiceOfferForm(forms.ModelForm):
    # user_service_areas = forms.MultipleChoiceField()
    class Meta():
        model = ServiceOffer
        fields = ['consulting', 'generaladvice', 'talk', 'price', 'description', 'user_service_areas', 'user_service_technology']

        widgets = {
            'consulting' : forms.CheckboxInput(attrs={'class' : 'focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded'}),
            'generaladvice' : forms.CheckboxInput(attrs={'class' : 'focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded'}),
            'talk' : forms.CheckboxInput(attrs={'class' : 'focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded'}),
            'price' : forms.TextInput(attrs={'placeholder' : 'Price you charge in $ per hour','class' : 'flex-1 block w-full focus:ring-indigo-500 focus:border-indigo-500 min-w-0 rounded-none rounded-r-md sm:text-sm border-gray-300'}),
            'description' : forms.Textarea(attrs={'rows':3, 'placeholder' : 'Write a few sentences about your offerings.', 'class' : 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border border-gray-300 rounded-md'}),
        }

class ServiceOfferTechExpertForm(forms.ModelForm):
    # user_service_areas = forms.MultipleChoiceField()
    class Meta():
        model = ServiceOfferTechExpert
        fields = ['consulting', 'generaladvice', 'talk', 'price', 'description', 'user_service_areas', 'user_service_technology']

        widgets = {
            'consulting' : forms.CheckboxInput(attrs={'class' : 'focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded'}),
            'generaladvice' : forms.CheckboxInput(attrs={'class' : 'focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded'}),
            'talk' : forms.CheckboxInput(attrs={'class' : 'focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded'}),
            'price' : forms.TextInput(attrs={'placeholder' : 'Price you charge in $ per hour','class' : 'flex-1 block w-full focus:ring-indigo-500 focus:border-indigo-500 min-w-0 rounded-none rounded-r-md sm:text-sm border-gray-300'}),
            'description' : forms.Textarea(attrs={'rows':3, 'placeholder' : 'Write a few sentences about your offerings.', 'class' : 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border border-gray-300 rounded-md'}),
        }



class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
        'placeholder': '',
        'type': 'email',
        'name': 'email'
        }))

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
        'placeholder': '',
        'type': 'email',
        'name': 'email'
        }))


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserSetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(label='New Password:', widget=forms.PasswordInput(attrs={'class' : 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}))
    new_password2 = forms.CharField(label='Confirm Password:', widget=forms.PasswordInput(attrs={'class' : 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}))

