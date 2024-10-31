from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import administrators_collection, mirror_collection, sites_collection, content_collection
# Create your views here.

class Administrator_Login(APIView):
    
    def post(self, request):

        username = request.data['username']
        password = request.data['password']

        if administrators_collection.find_one({"username":username,"password":password}):
                administrator = administrators_collection.find_one({"username":username,"password":password})
                ws_secret_key = administrator.get('administrator_login_return_key')
                return Response({'status_text':'ok','status_code':200,'ws_secret_key':ws_secret_key})
            
        return Response({'status_text':'UnAuthorised','status_code':401})
    
class Administrator_Register(APIView):
    
    def post(self, request):

        required_data = ['username','password','email','profile_image_url','contact','address_line_1','address_line_2','address_line_3']
        print(request.data , )
        if  not all(field in request.data.keys() for field in required_data):
             return Response({"status_text":"requred keys 'username','password','email','profile_image_url','contact','address_line_1','address_line_2','address_line_3'"})
        username = request.data['username']
        password = request.data['password']
        email_id = request.data['email']
        profile_image_url = request.data['profile_image_url']
        contact = request.data['contact']
        address_line_1 = request.data['address_line_1']
        address_line_2 = request.data['address_line_2']
        address_line_3 = request.data['address_line_3']


        if administrators_collection.find_one({'email_id':email_id}):
             return Response({'status':'Email Already Exist Please Login'})
        
        if administrators_collection.find_one({'username':username}):
             return Response({'status':'Username Already taken'})

        administrator_data = {
            "username":username,
            "password":password,
            "email_id":email_id,
            "profile_image_url":profile_image_url,
            "contact":contact,
            "address_line_1":address_line_1,
            "address_line_2":address_line_2,
            "address_line_3":address_line_3,
            "administrator_login_return_key":username+password,
            "websocket_channel_name":None
        }

        administrators_collection.insert_one(administrator_data)
        return Response({'status_text':'Registered Successfully','status_code':200})
            
        # return Response({'status':'UnAuthorised'})

class Mirror_Login(APIView):

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        if mirror_collection.find_one({"username":username,"password":password}):
     
                mirror = mirror_collection.find_one({"username":username,"password":password})
                # mirror_id = mirror.get('_id')
                # return Response({'status_text':'ok','status_code':200,'ws_secret_key':ws_secret_key})
        
                contents = content_collection.find({'mirror_id':mirror.get('_id')})
                content_list = []

                for content in contents:
                    if '_id' in content:
                        content['_id'] = str(content['_id'])
                    if 'mirror_id' in content:
                        content['mirror_id'] = str(content['mirror_id'])
                    if 'site_id' in content:
                        content['site_id'] = str(content['site_id'])
                    if 'administrator_id' in content:
                        content['administrator_id'] = str(content['administrator_id'])
                    content_list.append(content)

                    # (
                    #     "mirror_group",
                    #     {
                    #         'type': 'update.mirror',
                    #         'data': {'service':'GetMyContents','data':content_list},
                    #     }
                    # )
                return Response({'status_text':'ok','status_code':200,'data':content_list})

            
        return Response({'status_text':'UnAuthorised','status_code':401})
    
class Mirror_Register(APIView):

    def post(self, request):

        required_data = ['username','password','site_name','administrator_username','mirror_name','mirror_description']

        if  not all(field in request.data for field in required_data):
             return Response({"status_text":"requred keys 'username','password','site_name','administrator_username','mirror_name','mirror_description'"})
        username = request.data['username']
        password = request.data['password']
        site_name = request.data['site_name']
        administrator_username = request.data['administrator_username']
        mirror_name = request.data['mirror_name']
        mirror_description = request.data['mirror_description']

        if mirror_collection.find_one({'username':username}):
             return Response({'status':'Username Already taken'})
        
        # administrator_object = f''
        if administrators_collection.find_one({"username":administrator_username}):
            administrator =  administrators_collection.find_one({"username":administrator_username})


            if sites_collection.find_one({'site_name':site_name, 'administrator_id':administrator.get("_id")}):
                site = sites_collection.find_one({'site_name':site_name, 'administrator_id':administrator.get("_id")})

                # if administrator is not None and site is not None:

                mirror_data = {
                    "username":username,
                    "password":password,
                    "site_id":site.get("_id"),
                    "administrator_id":administrator.get('_id'),
                    "mirror_name":mirror_name,
                    "mirror_description":mirror_description,
                    "mirror_login_return_key":username+password,
                    "websocket_channel_name":None
                }
                mirror_collection.insert_one(mirror_data)
                # ws_secret_key = 'key'
                return Response({'status_text':'Registered Successfully','status_code':200})
            else:
                return Response({'status_text':'Not Allowed','status_code':401}) 
        else:
            return Response({'status_text':'UnAuthorised','status_code':401})


class Site_Register(APIView):

    def post(self, request):

        required_data = ['administrator_username','site_name','site_image_url','site_description']

        if  not all(field in request.data for field in required_data):
             return Response({"status_text":"requred keys 'administrator_username','site_name','site_image_url','site_description'"})
        site_name = request.data['site_name']
        site_image_url = request.data['site_image_url']
        administrator_username = request.data['administrator_username']
        site_description = request.data['site_description']

        if sites_collection.find_one({'site_name':site_name}):
             return Response({'status':'site name Already Exist'})
        
        # administrator_object = f''
        administrator =  administrators_collection.find_one({"username":administrator_username})
        if administrator is not None:

            site_data = {
                "site_name":site_name,
                "administrator_id":administrator.get('_id'),
                "site_name":site_name,
                "site_description":site_description,
                "site_image_url":site_image_url
            }
            sites_collection.insert_one(site_data)
            # ws_secret_key = 'key'
            return Response({'status_text':'Registered Successfully','status_code':200})
        else:
            return Response({'status_text':'UnAuthorised','status_code':401})
