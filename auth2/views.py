from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from user.models import Profile
from django.contrib.auth import authenticate
# Create your views here.

@api_view(["GET","POST"])
def home_page(request):
    return Response({"message":"HELL"},status=status.HTTP_200_OK)





@api_view(["POST"])
def user_login(request):
    parameters = request.data
    print("Passed Parameter := ", parameters)

    try:
        identifier = request.data["identifier"]
        password = request.data["password"]
        if not all([identifier,password]):
            return Response({"error": f"Missing fields: Username/Phone and Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = None
        print("CURRENT")
        if str(identifier).isdigit() and len(str(identifier))==10:
            print("YES ITS PHONE BASED USER ")
            try:
              user_profile = Profile.objects.get(phonenumber=identifier)
              user = user_profile.user
            except Profile.DoesNotExist:
                return Response({"invalid":"User with this phone number does not Exists"})    
        else:
            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:  
                return  Response({"invalid":"User Does not Exits"})
        
        print("AFTER")
        user =  authenticate(username=user,password=password)
        if user is None:
            return Response({"error":"Invalid Credentials"},status=401)
        print("AFTER USER",user)
        
        previous_token = Token.objects.get(user=user).delete if Token.objects.filter(user=user).exists() else None
        if previous_token:
            previous_token.delete()
    
        print("AFTER TOKEN")
        token = Token.objects.create(user=user)
        
        return Response({"message":"User Logged in Successfully","auth_token":token.key})
    except Exception as e:
        return  Response({"error":f"Error Ocuured {e}"},status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"message":"User Logged Out Successfully "})
    except Exception as e:
        return Response({"message":f"Error Occured {e}"})
    
    

@api_view(["POST"])
def register_login(request):
    parameters = request.data
    print("Passed Parameter := ", parameters)

    try:
        required_fields = ["username", "email", "password", "fullname", "phonenumber"]
        missing_fields = [field for field in required_fields if not parameters.get(field)]

        if missing_fields:
            return Response({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

        username = parameters["username"].strip()
        email = parameters["email"].strip()
        password = parameters["password"]
        fullname = parameters["fullname"]
        phonenumber = parameters["phonenumber"]

        if User.objects.filter(username=username).exists():
            return Response({"message": "User with this username already exists"}, status=status.HTTP_409_CONFLICT)

        if User.objects.filter(email=email).exists():
            return Response({"message": "User with this email already exists"}, status=status.HTTP_409_CONFLICT)

        if Profile.objects.filter(phonenumber=phonenumber).exists():
            return Response({"message": "User with this phone number already exists"}, status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        user_profile = Profile.objects.create(user=user, phonenumber=phonenumber, fullname=fullname)
        user_profile.save()

        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)

        return Response({"message": "Register API", "auth_token": token.key})

    except Exception as e:
        return Response({"error": f"Error Occurred: {str(e)}", "auth_token": "not available"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_api(request):
    return Response({"message":f"Wow Welcome {request.user}"})
    