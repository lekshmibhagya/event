
from django.shortcuts import render
from django.contrib.auth.models import User
from . models import *
from . serializers import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import ISO_8601,status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .permissions import *
import re

# Create your views here.
'''signup username and password added to the User table
other fields profile table '''

@api_view(['POST'])
def signup(request):
    if request.method=='POST':
        regex=r'[a-zA-Z]+'
        emailregex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phonenumberregex=r'[0-9]+'

        
        try:
            try:
                if re.fullmatch(regex,request.data['username']):
                    username=request.data['username']
                else:
                    return Response({'app_data':'enter valid username','dev_data':'enter valid username'},status=status.HTTP_400_BAD_REQUEST)

               
            except Exception as E:
                return Response({'app_data':'username required','dev_data':str(E)},status=status.HTTP_400_BAD_REQUEST)
        
            password=request.data['password']
            if password is not None:
                pass
            else:
                return Response({'app_data':'password required','dev_data':'password must be not none'},status=status.HTTP_400_BAD_REQUEST)
            try:
                name=request.data['name']
            except:
                return Response({'app_data':'name reqiured','dev_data':'name required'},status=status.HTTP_400_BAD_REQUEST)
            try:
                if re.fullmatch(emailregex,request.data['email']):
                    email=request.data['email']
                else:
                    return Response({'app_data':'enter valid email','dev_data':'enter valid email'},status=status.HTTP_400_BAD_REQUEST)
                    
            except:
                return Response({'app_data':'email required','dev_data':'email required'},status=status.HTTP_400_BAD_REQUEST)
            try:
                if re.fullmatch(phonenumberregex,request.data['phonenumber']):
                    phonenumber=request.data['phonenumber']
                else:
                    return Response({'app_data':'enter valid phonenumber','dev_data':'enter valid phonenumber'},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'app_data':'phonenumber required','dev_data':'phonenumber required'},status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(username=username):
                return Response({'app_data':'username is already exsisting','dev_data':'username is exsisting'},status=status.HTTP_400_BAD_REQUEST)
            else:
                  
                users=User.objects.create_user(username=username,password=password)
                users.save()
            
        
                profile=Profile(user=users,name=name,email=email,phonenumber=phonenumber)
                profile.save()
        
            
    
                refresh=RefreshToken.for_user(users)
                data={}
                data.update({'refresh_token':str(refresh)})
                data.update({'access_token':str(refresh.access_token)})
        except Exception as E:
            return Response({'app_data':'something went wrong','dev_data':str(E)},status=status.HTTP_400_BAD_REQUEST)


    return Response({'app_data':'successfully registerd','dev-data':'successfully registerd','data':data},status=status.HTTP_201_CREATED)

          

@api_view(['POST'])
def login(request):
    
    if request.method=='POST':
        try:
            username=request.data['username']
            password=request.data['password']
            if User.objects.filter(username = username).exists():
                user=User.objects.get(username=username)
                print(user)
                pass
            else:
                return Response({'app_data':'This username  has not been registered. Please signup to continue','dev_data':'This email deosnot exists'}, status = status.HTTP_400_BAD_REQUEST)
            user=authenticate(username=username,password=password)
            if not user==None:
                refresh = RefreshToken.for_user(user)
                data = {}
                data.update({'refresh_token':str(refresh)})
                data.update({'access_token':str(refresh.access_token)})
                return Response({'app_data':'success','dev_data':'successfully created','data':data},status=status.HTTP_201_CREATED)
            else:
                return Response({'app_data':'failed','dev_data':'failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response({'app_data':'Something went wrong', 'dev_data':str(E)}, status=status.HTTP_400_BAD_REQUEST)
@permission_classes([IsAuthenticated])        
@api_view(['PUT'])
def editProfile(request):
    regex=r'[a-zA-Z]+'
    emailregex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phonenumberregex=r'[0-9]+'
    
    if request.method=='PUT':
        try:
            user_obj=User.objects.get(id=request.user.id)
            print(user_obj)
            profile_obj=Profile.objects.get(user=user_obj)
            print(profile_obj)
            if profilePermissions(user_obj,profile_obj):
                try:
                    if re.fullmatch(regex,request.data['name']):
                        name=request.data['name']
                    else:
                        return Response({'app_data':'enter valid username','dev_data':'enter valid username'},status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({'app_data':'name required','dev_data':'name required'},status=status.HTTP_400_BAD_REQUEST)
                try:
                    if re.fullmatch(emailregex,request.data['email']):
                        email=request.data['email']
                    else:
                        return Response({'app_data':'enter a valid email like admin@gmail.com','dev_data':'not a valid email'},status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({'app_data':'email required','dev_data':'email required'},status=status.HTTP_400_BAD_REQUEST)
                try:
                    if re.fullmatch(phonenumberregex,request.data['phonenumber']):
                        phonenumber=request.data['phonenumber']
                    else:
                        return Response({'app_data':'not valid','dev_data':'not valid'},status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({'app_data':'phonenumber required','dev_data':'phonenumber required'},status=status.HTTP_400_BAD_REQUEST)
                
                
                profile_obj=Profile.objects.filter(user=user_obj)
                
                profile_obj.update(name=name,email=email,phonenumber=phonenumber)

                return Response({'app_data':'successfully registerd','dev-data':'successfully registerd'},status=status.HTTP_201_CREATED)   
            else:
                return Response({'app_data':'no permission','dev_data':'no permissions'},status=status.HTTP_400_BAD_REQUEST)   

        except Exception as E:
            return Response({'app_data':'something went wrong','dev_data':str(E)},status=status.HTTP_400_BAD_REQUEST)
  
def imageUpload(file):
    image_allowed=['png','jpg','jpeg']
   
    try:        
        print("dfgsdf")
        print('length is:',len(file))
        if not file==None:
            print('length is:',len(file))
            if len(file)>1:
                print("hai")
                
                return False
            else:
                print("5645")
                for image in file:
                    images=str(image)
                    image_format=images.split('.')[-1]
                    print("hui")
                    print('images is',images)
                    print('image format',image_format)
                    if image_format in image_allowed:
                        # data=Event(image=image)
                        # data.save()
                        image_upload=image
                        print('image_permitted',image_upload)
                        
                        return image_upload
                    else:
                        return False
    except Exception as E:
         return str(E)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def createEvent(request):
    if request.method=='POST':
        
        # try:
            eventname=request.data['eventname']
            data=Event.objects.filter(owner__user__id=request.user.id)
            print(data)
            if eventname is not None:
                for i in data:
                    evnt_name=i.event_name
                    if (evnt_name==eventname):

                        return Response({'app_data':'this user have already this event','dev_data':'user have already this event'},status=status.HTTP_400_BAD_REQUEST)
            

         
               
            try:
                about=request.data['about']
            except:
                return Response({'app_data':'about required','dev_data':'about required'},status=status.HTTP_400_BAD_REQUEST)
            try:
                location=request.data['location']
            except:
                return Response({'app_data':'location required','dev_data':'location required'},status=status.HTTP_400_BAD_REQUEST)
            try:
                start_date=request.data['start_date']
            except:
                return Response({'app_data':'start date required','dev_data':'start date required'},status=status.HTTP_400_BAD_REQUEST)
            try:
                end_date=request.data['end_date']
            except:
                return Response({'app_data':'end date required','dev_data':'end date required'},status=status.HTTP_400_BAD_REQUEST)
            try:
                
                file=request.data.pop('file')
                print('file is a list :',file)
                if not file==None:
                    try:
                        data=imageUpload(file)
                        if imageUpload(file):
                            var=imageUpload(file)
                            print("var is the image permitted to upload : ",var)
                        else:
                            return Response({'app_data':'not permitted multiple images and file format otherthan png,jpeg,jpeg','dev_data':'not permitted multiple images and file format otherthan png,jpeg,jpeg'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
                       
                    except Exception as E:
                        print(str(E))
                else:
                    return Response({'app_data':'image required','dev_data':'image required'},status=status.HTTP_400_BAD_REQUEST)

               
                
                
            except Exception as E:
                return Response({'app_data':'image required','dev_data':str(E)},status=status.HTTP_400_BAD_REQUEST)
            # if Event.objects.filter(owner__user__id=request.user.id).exists:
            user=Profile.objects.get(user_id=request.user.id)
            print(user,'337')
            data=Event.objects.create(event_name=eventname,about=about,location=location,start_date=start_date,end_date=end_date,image=var,owner =user)
            
            
            return Response({'app_data':"succesfully created","dev_data":"created"},status=status.HTTP_201_CREATED)

     
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def editEvent(request,uid):
   if request.method=='PUT':
        try:
            profile_obj=Profile.objects.get(user=request.user)
           
            print('profile object for permissions',profile_obj)
            event_obj=Event.objects.get(id=uid)
            print("event object is",event_obj)
            print(event_obj.owner)
            if userPermissions(profile_obj,event_obj):
                eventname=request.data['eventname']
                data=Event.objects.filter(owner__user__id=request.user.id)
                print('data is',data)
                if eventname is not None:
                    for i in data:
                        name=i.event_name
                        print(name)
                        if(name==eventname):
                            return Response({'app_data':'event already exsisting','dev_data':'event already exsisting'},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'app_data':'about required','dev_data':'about required'},status=status.HTTP_400_BAD_REQUEST)

                
                try:
                    about=request.data['about']
                except:
                    return Response({'app_data':'about required','dev_data':'about required'},status=status.HTTP_400_BAD_REQUEST)
                try:
                    location=request.data['location']
                except:
                    return Response({'app_data':'location required','dev_data':'location required'},status=status.HTTP_400_BAD_REQUEST)
                try:
                    start_date=request.data['start_date']
                except:
                    return Response({'app_data':'start date required','dev_data':'start date required'},status=status.HTTP_400_BAD_REQUEST)
                try:
                    end_date=request.data['end_date']
                except:
                    return Response({'app_data':'end date required','dev_data':'end date required'},status=status.HTTP_400_BAD_REQUEST)
                try:
                
                    file=request.data.pop('file')
                    
                    if imageUpload(file):
                        var=imageUpload(file)
                    else:
                        return Response({'app_data':'not permitted multiple images and file format otherthan png,jpeg,jpeg','dev_data':'not permitted multiple images and file format otherthan png,jpeg,jpeg'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

                  
                except:
                    return Response({'app_data':'image required','dev_data':'image required'},status=status.HTTP_400_BAD_REQUEST)
            
                
                data_obj=Event.objects.filter(id=uid)
                print(data_obj)
                

                data_obj.update(event_name=eventname,about=about,location=location,start_date=start_date,end_date=end_date,image=var)
                data_obj.update()
                return Response({'app_data':"succesfully updated","dev_data":"updated"},status=status.HTTP_201_CREATED)
            else:
                return Response({'app_data':"permission not allowed","dev_data":" not updated"},status=status.HTTP_400_BAD_REQUEST)

                # da=event_profile.owner(owner__user__id=request.user.id)
                
                
            
        except Exception as E:
            return Response({'app_data':"something went wrong","dev_data":str(E)},status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def deleteEvent(request,did):
    if request.method=='POST':
        try:
            profile_obj=Profile.objects.get(user=request.user)
            print(profile_obj)
            event_obj=Event.objects.get(id=did)
            
            if deletePermissions(profile_obj,event_obj):
                print(profile_obj)
                if Event.objects.filter(id=did).exists():
                    data=Event.objects.get(id=did)
                    data.delete()
                    return Response({'app_data':'data removed','dev_data':'data removed'},status=status.HTTP_200_OK)
            else:
                return Response({'app_data':'dont have permission to delete the event','dev_data':'permission required'},status=status.HTTP_400_BAD_REQUEST)   
        except Exception as E:
            return Response({'app_data':"something went wrong","dev_data":str(E)},status=status.HTTP_400_BAD_REQUEST)
@permission_classes([IsAuthenticated])           
@api_view(['GET'])
def viewMyEvents(request):
    if request.method=='GET':
        try:
            
            events=Event.objects.filter(owner__user__id=request.user.id)
            event_serializers=EventSerializer(events,many=True)
            return Response(event_serializers.data)
        except Exception as E:
            return Response({'app_data':'something went wrong','dev_data':str(E)},status=status.HTTP_400_BAD_REQUEST)
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def viewAllEvents(request):
    if request.method=='GET':
        try:
            events=Event.objects.all()
            event_serializers=EventSerializer(events,many=True)
            return Response(event_serializers.data)
        except Exception as E:
            return Response({'app_data':'something went wrong','dev_data':str(E)},status=status.HTTP_400_BAD_REQUEST)
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def viewProfile(request):
    if request.method=='GET':
        profile_query=Profile.objects.get(user__id=request.user.id)
        print(profile_query)
        try:
            profile_query=Profile.objects.filter(user__id=request.user.id)
            print(profile_query)
            profile_serializer=ProfileSerialzer(profile_query,many=True)
            return Response(profile_serializer.data)

        except Exception as E:
            return Response({'app_data':'something went wrong','dev_data':str(E)},status=status.HTTP_400_BAD_REQUEST)


