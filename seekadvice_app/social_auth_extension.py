import requests
from django.shortcuts import redirect
from .models import CustomUser
import cloudinary
import cloudinary.uploader
import cloudinary.api


def upload_picture(strategy, details, user, is_new, *args, **kwargs):
    if is_new:
        data = user.social_auth.values_list('extra_data').first()
        dict_data = dict(data[0])            
        access_token_model = dict_data['access_token']
        provider = user.social_auth.values_list('provider', flat=True)[0]
        try:
            userprofile = CustomUser.objects.get(email=user)
            if provider == "github":                
                #Make the Request on github
                url = "https://api.github.com/user"
                payload={}
                headers = {
                'Authorization': f'Bearer {access_token_model}'
                }
                r = requests.request("GET", url, headers=headers, data=payload)
                if (r.status_code == 200):
                    json_response = r.json()
                    userprofile.displayname = json_response['name'] if json_response['name'] != None else ''
                    userprofile.jobtitle = json_response['company'] if json_response['company'] != None else ''
                    userprofile.github_name = json_response['login'] if json_response['login'] != None else ''
                    url_response = json_response['avatar_url'] if json_response['avatar_url'] != None else ''
                    if url_response != '':
                        userprofile.user_avatar = cloudinary.uploader.upload_resource(url_response, folder='seekadviceImages')
                    userprofile.save()
            elif provider == "google-oauth2":
                userprofile.displayname = details.get('fullname')
                userprofile.save()

        except Exception as e:
            print(e)
            return
