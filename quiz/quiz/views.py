
from ast import Global
from distutils.command.config import config
import email
from optparse import Option
import re
import string
from stringprep import in_table_c11
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from django.contrib import messages
from virtualenv import session_via_cli
from mypro import settings
import pyrebase
from django.contrib import auth


config = {
  "apiKey": "AIzaSyBh54bhUiOduOlyq6k6DTTeXL_lAg0L94w",
  "authDomain": "cpanel-10ae6.firebaseapp.com",
  "databaseURL":"https://cpanel-10ae6-default-rtdb.firebaseio.com",
  "projectId": "cpanel-10ae6",
  "storageBucket": "cpanel-10ae6.appspot.com",
  "messagingSenderId": "206710126999",
  "appId": "1:206710126999:web:ee4da3d9d3f7de6bd4ecd2"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


# Create your views here.
def sign(request):
    return render(request, 'sign.html')

    

def home(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    """
    data = {
        "q":"How many different cloud deployment models?",
        "option 1":2,
        "option 2":3,
        "option 3":7,
        "option 4":4,
        "option 5":10,
        "ans":3,
        "ans2":2
    }

    database.child("csp").child("GCP").child("Q__2").set(data)

    
    data = {
        "q":"How many different cloud deployment models?",
        "option 1":2,
        "option 2":3,
        "option 3":7,
        "option 4":4,
        "ans":3
    }

    database.child("csp").child("Azure").child("Q_2").set(data)
    """
    
    try:

        user = authe.sign_in_with_email_and_password(email,password)

    except:
        message = "Invalid user"
        return render(request, 'sign.html',{"m":message})


    session_id = user["idToken"]
    request.session["uid"]=str(session_id)
        

    
    return render(request, 'home.html',{"e":email})



def logout(request):
    auth.logout(request)
    return render(request, 'sign.html')

def signup(request):
    return render(request, 'signup.html')

def postsignup(request):


    email = request.POST.get('email')
    password = request.POST.get('password')


    try:


        user = authe.create_user_with_email_and_password(email,password)

    except:
        message = "Invalid details"
        return render(request, 'up.html',{"m":message})

    user1 = user['idToken']


    authe.send_email_verification(user1)
    messag = "verification link sent, Kindly confirm then signup"
    

    return render(request, "sign.html",{"rw":messag})


def cancelsignup(request):

    return render(request, "sign.html")

def go(request):
    
    


    if request.method == "GET" and "csrfmiddlewaretoken" in request.GET:
        #earch = request.GET.get("search")

        b = request.GET.get('csp1')

        if b == "GCP":

        
            con = database.child("csp").child("GCP").shallow().get().val()
            d = []   
            for j in con:
                d.append(j)

            #cd = []
            #for i in d:
            type = request.GET.get('type')
            if type == "radio":

                an = request.GET.get('ag')
                ans1 = request.GET.get('ans1')

                sc = request.GET.get('sc')
                sc = int(sc)

                if an == ans1:
                    sc = sc + 1

            else:

                an1 = request.GET.get('ag1')
                an2 = request.GET.get('ag2')
                an3 = request.GET.get('ag3')
                an4 = request.GET.get('ag4')
                an5 = request.GET.get('ag5')

                lis = [an1,an2,an3,an4,an5]

                ans = []

                for i in lis:
                    if i != "None":
                        ans.append(i)

                

                ans1 = request.GET.get('ans1')
                ans2 = request.GET.get('ans2')



                sc = request.GET.get('sc')
                sc = int(sc)

                if ans1 and ans2 in ans:
                    sc = sc + 1

                


            me = request.GET.get('inc')
            me = int(me)

            if me == len(d):
                
                idtoken = request.session['uid']
                a = authe.get_account_info(idtoken)
                a = a["users"]
                a = a[0]
                email = a["email"]
                per = (sc/me)*100
                if per >= 40:
                    res = "Congratulations!!! You are Pass."
                else:
                    res = "Oops! Your are Fail."
                
                subject = " Your Result on Quizwerr "
                message = (str(res) + ", total Marks is:-"+str(sc)+ ", percentange is:-"+str(per)+"%")
                from_email = settings.EMAIL_HOST_USER
                to_list = [email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)

                return render(request, "go.html",{"res":res,"score":sc,"ms":b})

            else:
                i = d[me]


                me = me + 1                

                pos = "not first"

                if len(i) == 3:

                    
                    ques = database.child("csp").child("GCP").child(i).child("q").get().val()
                    ans = database.child("csp").child("GCP").child(i).child("ans").get().val()
                    option1 = database.child("csp").child("GCP").child(i).child("option 1").get().val()
                    option2 = database.child("csp").child("GCP").child(i).child("option 2").get().val()
                    option3 = database.child("csp").child("GCP").child(i).child("option 3").get().val()
                    option4 = database.child("csp").child("GCP").child(i).child("option 4").get().val()

                    if  me== len(d):
                        pos1 = "final"
                            

                        return render(request, "go.html", {"pos1":pos1,"pos":pos,"sc":sc,"me":me,"m":b,"ques":ques,"ans":ans,"option1":option1,"option2":option2,
                        "option3":option3,"option4":option4})

                    else:
                        pos2 = "not final"
                        return render(request, "go.html", {"pos2":pos2,"pos":pos,"sc":sc,"me":me,"m":b,"ques":ques,"ans":ans,"option1":option1,"option2":option2,
                        "option3":option3,"option4":option4})
                        
                else:
                    ques = database.child("csp").child("GCP").child(i).child("q").get().val()
                    ans = database.child("csp").child("GCP").child(i).child("ans").get().val()
                    ans2 = database.child("csp").child("GCP").child(i).child("ans2").get().val()
                    option1 = database.child("csp").child("GCP").child(i).child("option 1").get().val()
                    option2 = database.child("csp").child("GCP").child(i).child("option 2").get().val()
                    option3 = database.child("csp").child("GCP").child(i).child("option 3").get().val()
                    option4 = database.child("csp").child("GCP").child(i).child("option 4").get().val()
                    option5 = database.child("csp").child("GCP").child(i).child("option 5").get().val()
                        
                        
                    if  me== len(d):
                        pos1 = "final"
                            

                        return render(request, "go.html", {"pos1":pos1,"pos":pos,"sc":sc,"me":me,"m":b,"quest":ques,"ans":ans,"ans2":ans2,"option1":option1,"option2":option2,
                        "option3":option3,"option4":option4,"option5":option5})

                    else:
                        pos2 = "not final"
                        return render(request, "go.html", {"pos2":pos2,"pos":pos,"sc":sc,"me":me,"m":b,"quest":ques,"ans":ans,"ans2":ans2,"option1":option1,"option2":option2,
                         "option3":option3,"option4":option4,"option5":option5})

        elif b == "AWS":
            con = database.child("csp").child("AWS").shallow().get().val()
            d = []   
            for j in con:
                d.append(j)

            #cd = []
            #for i in d:
            type = request.GET.get('type')
            if type == "radio":

                an = request.GET.get('ag')
                ans1 = request.GET.get('ans1')

                sc = request.GET.get('sc')
                sc = int(sc)

                if an == ans1:
                    sc = sc + 1

            else:

                an1 = request.GET.get('ag1')
                an2 = request.GET.get('ag2')
                an3 = request.GET.get('ag3')
                an4 = request.GET.get('ag4')
                an5 = request.GET.get('ag5')

                lis = [an1,an2,an3,an4,an5]

                ans = []

                for i in lis:
                    if i != "None":
                        ans.append(i)

                

                ans1 = request.GET.get('ans1')
                ans2 = request.GET.get('ans2')



                sc = request.GET.get('sc')
                sc = int(sc)

                if ans1 and ans2 in ans:
                    sc = sc + 1

                


            me = request.GET.get('inc')
            me = int(me)

            if me == len(d):
                idtoken = request.session['uid']
                a = authe.get_account_info(idtoken)
                a = a["users"]
                a = a[0]
                email = a["email"]
                per = (sc/me)*100
                if per >= 40:
                    res = "Congratulations!!! You are Pass."
                else:
                    res = "Oops! Your are Fail."
                
                subject = " Your Result on Quizwerr "
                message = (str(res) + ", total Marks is:-"+str(sc)+ ", percentange is:-"+str(per)+"%")
                from_email = settings.EMAIL_HOST_USER
                to_list = [email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)

                return render(request, "go.html",{"res":res,"score":sc,"ms":b})

            else:
                i = d[me]


                me = me + 1                

                pos = "not first"

                if len(i) == 3:

                    
                    ques = database.child("csp").child("AWS").child(i).child("q").get().val()
                    ans = database.child("csp").child("AWS").child(i).child("ans").get().val()
                    option1 = database.child("csp").child("AWS").child(i).child("option 1").get().val()
                    option2 = database.child("csp").child("AWS").child(i).child("option 2").get().val()
                    option3 = database.child("csp").child("AWS").child(i).child("option 3").get().val()
                    option4 = database.child("csp").child("AWS").child(i).child("option 4").get().val()

                    if  me== len(d):
                        pos1 = "final"
                            

                        return render(request, "go.html", {"pos1":pos1,"pos":pos,"sc":sc,"me":me,"m":b,"ques":ques,"ans":ans,"option1":option1,"option2":option2,
                        "option3":option3,"option4":option4})

                    else:
                        pos2 = "not final"
                        return render(request, "go.html", {"pos2":pos2,"pos":pos,"sc":sc,"me":me,"m":b,"ques":ques,"ans":ans,"option1":option1,"option2":option2,
                        "option3":option3,"option4":option4})
                        
                else:
                    ques = database.child("csp").child("AWS").child(i).child("q").get().val()
                    ans = database.child("csp").child("AWS").child(i).child("ans").get().val()
                    ans2 = database.child("csp").child("AWS").child(i).child("ans2").get().val()
                    option1 = database.child("csp").child("AWS").child(i).child("option 1").get().val()
                    option2 = database.child("csp").child("AWS").child(i).child("option 2").get().val()
                    option3 = database.child("csp").child("AWS").child(i).child("option 3").get().val()
                    option4 = database.child("csp").child("AWS").child(i).child("option 4").get().val()
                    option5 = database.child("csp").child("AWS").child(i).child("option 5").get().val()
                        
                        
                    if  me== len(d):
                        pos1 = "final"
                            

                        return render(request, "go.html", {"pos1":pos1,"pos":pos,"sc":sc,"me":me,"m":b,"quest":ques,"ans":ans,"ans2":ans2,"option1":option1,"option2":option2,
                        "option3":option3,"option4":option4,"option5":option5})

                    else:
                        pos2 = "not final"
                        return render(request, "go.html", {"pos2":pos2,"pos":pos,"sc":sc,"me":me,"m":b,"quest":ques,"ans":ans,"ans2":ans2,"option1":option1,"option2":option2,
                         "option3":option3,"option4":option4,"option5":option5})


        else:
            con = database.child("csp").child("Azure").shallow().get().val()
            d = []   
            for j in con:
                d.append(j)

            #cd = []
            #for i in d:
            type = request.GET.get('type')
            if type == "radio":

                an = request.GET.get('ag')
                ans1 = request.GET.get('ans1')

                sc = request.GET.get('sc')
                sc = int(sc)

                if an == ans1:
                    sc = sc + 1

            else:

                an1 = request.GET.get('ag1')
                an2 = request.GET.get('ag2')
                an3 = request.GET.get('ag3')
                an4 = request.GET.get('ag4')
                an5 = request.GET.get('ag5')

                lis = [an1,an2,an3,an4,an5]

                ans = []

                for i in lis:
                    if i != "None":
                        ans.append(i)

                

                ans1 = request.GET.get('ans1')
                ans2 = request.GET.get('ans2')



                sc = request.GET.get('sc')
                sc = int(sc)

                if ans1 and ans2 in ans:
                    sc = sc + 1

                


            me = request.GET.get('inc')
            me = int(me)

            if me == len(d):

                idtoken = request.session['uid']
                a = authe.get_account_info(idtoken)
                a = a["users"]
                a = a[0]
                email = a["email"]
                per = (sc/me)*100
                if per >= 40:
                    res = "Congratulations!!! You are Pass."
                else:
                    res = "Oops! Your are Fail."
                
                subject = " Your Result on Quizwerr "
                message = (str(res) + ", total Marks is:-"+str(sc)+ ", percentange is:-"+str(per)+"%")
                from_email = settings.EMAIL_HOST_USER
                to_list = [email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)

                return render(request, "go.html",{"res":res,"score":sc,"ms":b})

            else:
                i = d[me]


                me = me + 1                

                pos = "not first"

                if len(i) == 3:

                    
                    ques = database.child("csp").child("Azure").child(i).child("q").get().val()
                    ans = database.child("csp").child("Azure").child(i).child("ans").get().val()
                    option1 = database.child("csp").child("Azure").child(i).child("option 1").get().val()
                    option2 = database.child("csp").child("Azure").child(i).child("option 2").get().val()
                    option3 = database.child("csp").child("Azure").child(i).child("option 3").get().val()
                    option4 = database.child("csp").child("Azure").child(i).child("option 4").get().val()

                    if  me== len(d):
                        pos1 = "final"
                            

                        return render(request, "go.html", {"pos1":pos1,"pos":pos,"sc":sc,"me":me,"m":b,"ques":ques,"ans":ans,"option1":option1,"option2":option2,
                        "option3":option3,"option4":option4})

                    else:
                        pos2 = "not final"
                        return render(request, "go.html", {"pos2":pos2,"pos":pos,"sc":sc,"me":me,"m":b,"ques":ques,"ans":ans,"option1":option1,"option2":option2,
                        "option3":option3,"option4":option4})
                        
                else:
                    ques = database.child("csp").child("Azure").child(i).child("q").get().val()
                    ans = database.child("csp").child("Azure").child(i).child("ans").get().val()
                    ans2 = database.child("csp").child("Azure").child(i).child("ans2").get().val()
                    option1 = database.child("csp").child("Azure").child(i).child("option 1").get().val()
                    option2 = database.child("csp").child("Azure").child(i).child("option 2").get().val()
                    option3 = database.child("csp").child("Azure").child(i).child("option 3").get().val()
                    option4 = database.child("csp").child("Azure").child(i).child("option 4").get().val()
                    option5 = database.child("csp").child("Azure").child(i).child("option 5").get().val()
                        
                        
                    if  me== len(d):
                        pos1 = "final"
                            

                        return render(request, "go.html", {"pos1":pos1,"pos":pos,"sc":sc,"me":me,"m":b,"quest":ques,"ans":ans,"ans2":ans2,"option1":option1,"option2":option2,
                        "option3":option3,"option4":option4,"option5":option5})

                    else:
                        pos2 = "not final"
                        return render(request, "go.html", {"pos2":pos2,"pos":pos,"sc":sc,"me":me,"m":b,"quest":ques,"ans":ans,"ans2":ans2,"option1":option1,"option2":option2,
                         "option3":option3,"option4":option4,"option5":option5})



    else:

        

        a = request.POST.get('csp')
    
        if a == "GCP":

        
            con = database.child("csp").child("GCP").shallow().get().val()
            d = []   
            for j in con:
                d.append(j)

            #cd = []
            #for i in d:
            i = d[0]
            me = 1
            sc = 0

            pos2 = "l"
                
            ques = database.child("csp").child("GCP").child(i).child("q").get().val()
            ans = database.child("csp").child("GCP").child(i).child("ans").get().val()
            option1 = database.child("csp").child("GCP").child(i).child("option 1").get().val()
            option2 = database.child("csp").child("GCP").child(i).child("option 2").get().val()
            option3 = database.child("csp").child("GCP").child(i).child("option 3").get().val()
            option4 = database.child("csp").child("GCP").child(i).child("option 4").get().val()
                

            return render(request, "go.html", {"pos2":pos2,"sc":sc,"me":me,"m":a,"ques":ques,"ans":ans,"option1":option1,"option2":option2,
            "option3":option3,"option4":option4})
        
        elif a == "AWS":
            con = database.child("csp").child("AWS").shallow().get().val()
            d = []   
            for j in con:
                d.append(j)

            #cd = []
            #for i in d:
            i = d[0]
            me = 1
            sc = 0
                
            pos2 = "l"

            ques = database.child("csp").child("AWS").child(i).child("q").get().val()
            ans = database.child("csp").child("AWS").child(i).child("ans").get().val()
            option1 = database.child("csp").child("AWS").child(i).child("option 1").get().val()
            option2 = database.child("csp").child("AWS").child(i).child("option 2").get().val()
            option3 = database.child("csp").child("AWS").child(i).child("option 3").get().val()
            option4 = database.child("csp").child("AWS").child(i).child("option 4").get().val()
                

            return render(request, "go.html", {"pos2":pos2,"sc":sc,"me":me,"m":a,"ques":ques,"ans":ans,"option1":option1,"option2":option2,
            "option3":option3,"option4":option4})

        else:
            con = database.child("csp").child("Azure").shallow().get().val()
            d = []   
            for j in con:
                d.append(j)

            #cd = []
            #for i in d:
            i = d[0]
            me = 1
            sc = 0
                
            pos2 = "l"
            ques = database.child("csp").child("Azure").child(i).child("q").get().val()
            ans = database.child("csp").child("Azure").child(i).child("ans").get().val()
            option1 = database.child("csp").child("Azure").child(i).child("option 1").get().val()
            option2 = database.child("csp").child("Azure").child(i).child("option 2").get().val()
            option3 = database.child("csp").child("Azure").child(i).child("option 3").get().val()
            option4 = database.child("csp").child("Azure").child(i).child("option 4").get().val()
                

            return render(request, "go.html", {"pos2":pos2,"sc":sc,"me":me,"m":a,"ques":ques,"ans":ans,"option1":option1,"option2":option2,
            "option3":option3,"option4":option4})


def sign2(request):
    return render(request, "sign.html")