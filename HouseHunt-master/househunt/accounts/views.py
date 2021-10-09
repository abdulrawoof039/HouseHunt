from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Accountuser,Property,Image,Video,Review
from django.shortcuts import get_object_or_404
import re
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff and request.user.is_superuser:
            return redirect('http://127.0.0.1:8000/admin/')
        elif request.user.is_staff:
            return redirect('staffproperty')
        else:
            return redirect('dashboard')
    else:
        return render(request,'home.html')
#@login_required(login_url='login')
def dashboardView(request):
    if request.user.is_authenticated:
        return render(request,'dashboard.html')
    else:
        return redirect('login')
def contactView(request,my_id):
    if request.user.is_authenticated:
        context={}
        if request.method=='POST':
            name=request.POST['name']
            email=request.POST['email']
            subject1=request.POST['subject']
            messages=request.POST['messages']
            subject = subject1
            message = name+" "+messages
            email_from = email
            if(my_id==1):
                recipient_list = ["srirangamyuktha@gmail.com", ]
            elif(my_id==2):
                recipient_list = ["srirangampranav@gmail.com", ]
            else:
                recipient_list = ["srirangam.madhavi@gmail.com", ]
            send_mail(subject, message, email_from, recipient_list )
            mesg="Received Your Email"
            context={"mesg":mesg}
        return render(request,'contact.html',context)
    else:
        return redirect('login')
def contactsupportView(request):
    if request.user.is_authenticated:
        context={}
        if request.method=='POST':
            name=request.POST['name']
            email=request.POST['email']
            subject1=request.POST['subject']
            messages=request.POST['messages']
            subject = subject1
            message = name+" "+messages
            email_from = email
            recipient_list = ["srirangamyuktha@gmail.com", ]
            send_mail(subject, message, email_from, recipient_list )
            mesg="Received Your Email"
            context={"mesg":mesg}
        return render(request,'contact.html',context)
    else:
        return redirect('login')

#@login_required(login_url='login')
def verificationView(request,my_id):
    if request.user.is_authenticated:
        try:
            prop=Property.objects.get(id=my_id)
        except:
            raise Http404
        s1=""
        s2=""
        if request.method=='POST':
            verifiedpropertydetails=request.POST['t1']
            verifiedimages=request.POST['t2']
            verifiedvideos=request.POST['t3']
            verifiedcost=request.POST['t4']
            if(prop.emailstatus=="Sent" and verifiedpropertydetails=="Yes" and verifiedimages=="Yes" and verifiedvideos=="Yes" and verifiedcost=="Yes"):
                    pass
            else:
                if(verifiedpropertydetails=="Yes" and verifiedimages=="Yes" and verifiedvideos=="Yes" and verifiedcost=="Yes"):
                    subject = 'Property Verification'
                    message = f'Congratulations {prop.user.username}, your property has been verified by our team!!!\n\n\nProperty Details:\n\nType : {prop.propertytype}\nBHK Type : {prop.bedrooms} BHK\nAddress:{prop.address}\nLocality:{prop.address2}\nCity:{prop.city}'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [prop.user.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                    prop.emailstatus="Sent"
                    s2="Email sent to Property Owner..."
                    prop.verifiedproperty="Verified"
                else:
                    if(prop.verifiedproperty=="Verified"):
                        prop.emailstatus="NotSent"
                    if(verifiedpropertydetails=="Yes" or verifiedimages=="Yes" or verfiedvideos=="Yes" or verfiedcost=="Yes"):
                        prop.verifiedproperty="Verification in Progress"
                    else:
                        prop.verifiedproperty="Not Verified"   
            prop.verifiedpropertydetails= verifiedpropertydetails
            prop.verifiedimages=verifiedimages
            prop.verifiedvideos=verifiedvideos
            prop.verifiedcost=verifiedcost
            prop.save()
            s1="Changes Saved..."
            print(s2)
            print("hello")
        context={
            "prop":prop,"mesg":s1,"mesg1":s2,
        }
        return render(request,'verification.html',context)
    else:
        return redirect('login')

#@login_required(login_url='login')
def staffProperty(request):
    if request.user.is_authenticated:
        s1=""
        data = Property.objects.all()
        if request.method=='POST':
            username=request.POST['username']
            propertyid=request.POST['propertyid']
            city=request.POST['city']
            city=city.title()
            if(propertyid):
                data=data.filter(id=propertyid)
            elif(username and city):
                try:
                    user=Accountuser.objects.get(username=username)
                    data=data.filter(user=user,city=city)
                except:
                    s1="NO RESULTS FOUND...!!!" 
            elif(username):
                print("hello")
                try:
                    user=Accountuser.objects.get(username=username)
                    data=data.filter(user=user)
                    print(data)
                except:
                    s1="NO RESULTS FOUND...!!!"
            elif(city):
                data=data.filter(city=city)
            if(data and s1==""):
                s1=""
            else:
                print("abc")
                s1="NO RESULTS FOUND...!!!"
                data=Property.objects.all()
            print(s1)
            propert = {
                "proper": data,"username":username,"propertyid":propertyid,"city":city,"mesg":s1
            }
            return render(request,'staffproperty.html',propert)
        propert={
            "proper":data,
        }
        return render(request,'staffproperty.html',propert)
    else:
        return redirect('login')
#@login_required(login_url='login')
def staffpropertyDisplay(request,my_id):
    if request.user.is_authenticated:
        context={}
        try:
            propertyobj=Property.objects.get(id=my_id)
            imgobj=Image.objects.filter(prop=propertyobj)
            videoobj=Video.objects.filter(proper=propertyobj)
        except:
            raise Http404
        context={
            "pro": propertyobj, "img":imgobj, "vid":videoobj,
        }
        return render(request,'staffpropertydisplay.html',context)
    else:
        return redirect('login')
#@login_required(login_url='login')
def profileView(request):
    if request.user.is_authenticated:
        context={}
        if request.method=='POST':
                username=request.POST['username']
                email=request.POST['email']
                phonenum=request.POST['phone']
                user=Accountuser.objects.get(username=username)
                try:
                    u=Accountuser.objects.get(email=email)
                    if(user.username!=u.username):
                        context['mesg']="Email already exists try with another email"
                        return render(request,'profile.html',context)
                except:
                    pass
                context['mesg']="Changes saved"
                user.email = email
                user.phonenum=phonenum
                user.save()
                return render(request,'profile.html',context)
        return render(request,'profile.html',context)
    else:
        return redirect('login')

def profileStaffView(request):
    if request.user.is_authenticated:
        context={}
        if request.method=='POST':
                username=request.POST['username']
                email=request.POST['email']
                phonenum=request.POST['phone']
                user=Accountuser.objects.get(username=username)
                try:
                    u=Accountuser.objects.get(email=email)
                    if(user.username!=u.username):
                        context['mesg']="Email already exists try with another email"
                        return render(request,'profile.html',context)
                except:
                    pass
                context['mesg']="Changes saved"
                user.email = email
                user.phonenum=phonenum
                user.save()
                return render(request,'profilestaff.html',context)
        return render(request,'profilestaff.html',context)
    else:
        return redirect('login')

#@login_required(login_url='login')
def propertyView(request):
    if request.user.is_authenticated:
        data = Property.objects.all()
        img=Image.objects.all()
        video=Video.objects.all()
        propert = {
            "proper": data,"images": img,"videos":video,
        }
        return render(request,'property.html',propert)
    else:
        return redirect('login')
#@login_required(login_url='login')
def favouritesView(request):
    if request.user.is_authenticated:
        data = Property.objects.filter(favourite=request.user)
        img = Image.objects.all()
        video = Video.objects.all()
        propert = {
            "proper": data,"images": img,"videos":video,
        }
        return render(request,'favourites.html',propert)
    else:
        return redirect('login')
def registerPage(request):
    if request.method=='POST':
            username=request.POST['username']
            email=request.POST['email']
            password1=request.POST['password1']
            password2=request.POST['password2']
            phonenum=request.POST['phone']
            if password1==password2:
                if Accountuser.objects.filter(username=username).exists():
                    messages.info(request,'Username already exists')
                elif Accountuser.objects.filter(email=email).exists():
                    messages.info(request,'Email already exists')
                else:
                    user=Accountuser(username=username,email=email,password=password1,phonenum=phonenum)
                    user.password=make_password(user.password)
                    user.save()
                    print('user saved')
                    return redirect('login')
            else:
                messages.info(request,'Passwords not matching')
                return redirect('register')
            return redirect('login')
    else:
            return render(request,"registration/register.html")    
def loginPage(request):
        context={}
        if request.method =="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            try:
                user= Accountuser.objects.get(username=username)
                if user:
                    flag=check_password(password,user.password)
                    if flag :
                        login(request,user)
                        if user.is_staff and user.is_superuser:
                            return redirect('http://127.0.0.1:8000/admin/')
                        elif user.is_staff:
                            return redirect('staffproperty')
                        else:
                            return redirect('dashboard')
                    else:
                        context['error']="Username or Password is incorrect"
            except:
                context['error']="Username or Password is incorrect"
            return render(request,'registration/login.html',context)
        return render(request,'registration/login.html',context)  
#@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')
#@login_required(login_url='login')
def adpostView(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            rentorsale=request.POST['rentorsale']
            propertytype=request.POST.get('propertytype')
            floornumber=request.POST['floornumber']
            propertyage=request.POST['propertyage']
            propertysize=request.POST['propertysize']
            totalrooms=request.POST['totalrooms']
            bedrooms=request.POST['bedrooms']
            bathrooms=request.POST['bathrooms']
            money=request.POST['money']
            tenantspreferred=request.POST.get('tenantspreferred')
            furnishing=request.POST.get('furnishing')
            amenities=request.POST.getlist('amenities')
            images=request.FILES.getlist('images')
            videos=request.FILES.getlist('video')    
            address=request.POST['address1']
            address2=request.POST['address2']
            city=request.POST['city']
            city=city.title()
            address2=address2.title()
            state=request.POST['state']
            pincode=request.POST['zip']
            mapurl=request.POST['googleurl']
            description=request.POST['description']
            user=Accountuser.objects.get(username=request.user.username)
            proper=Property(user=user,rentorsale=rentorsale,propertytype=propertytype,floornumber=floornumber,propertyage=propertyage,propertysize=propertysize,totalrooms=totalrooms,bedrooms=bedrooms,bathrooms=bathrooms,money=money,tenantspreferred=tenantspreferred,furnishing=furnishing,amenities=amenities,address=address,address2=address2,city=city,state=state,pincode=pincode,mapurl=mapurl,description=description)
            proper.save()
            for i in images:
                img=Image(prop=proper,image=i)
                img.save()
            for i in videos:
                vid=Video(proper=proper,video=i)
                vid.save()
            return redirect('dashboard')
        return render(request,'adpost.html')
    else:
        return redirect('login')
#@login_required(login_url='login')
def propertyDisplay(request,my_id):
    if request.user.is_authenticated:
        context={}
        try:
            propertyobj=Property.objects.get(id=my_id)
            imgobj=Image.objects.filter(prop=propertyobj)
            videoobj=Video.objects.filter(proper=propertyobj)
            if propertyobj.favourite.filter(id=request.user.id).exists():
                request.user.is_favourite=True
                request.user.save()
            else:
                request.user.is_favourite=False
                request.user.save()
            print(propertyobj,imgobj,videoobj)
        except Product.DoesNotExist:
            raise Http404
        context={
            "pro": propertyobj, "img":imgobj, "vid":videoobj,
        }
        return render(request,'propertydisplay.html',context)
    else:
        return redirect('login')
#@login_required(login_url='login')
def myPropertiesView(request):
    if request.user.is_authenticated: 
        user=Accountuser.objects.get(username=request.user.username)
        properties=Property.objects.filter(user=user)
        context={
            "property":properties,
        }
        return render(request,'myproperties.html',context)
    else:
        return redirect('login')
#@login_required(login_url='login')
def editProperty(request,my_id):
    if request.user.is_authenticated:
        context={}
        s=""
        try:
            if request.method=='POST':
                    rentorsale=request.POST['rentorsale']
                    propertytype=request.POST.get('propertytype')
                    floornumber=request.POST['floornumber']
                    propertyage=request.POST['propertyage']
                    propertysize=request.POST['propertysize']
                    totalrooms=request.POST['totalrooms']
                    bedrooms=request.POST['bedrooms']
                    bathrooms=request.POST['bathrooms']
                    money=request.POST['money']
                    tenantspreferred=request.POST.get('tenantspreferred')
                    furnishing=request.POST.get('furnishing')
                    amenities=request.POST.getlist('amenities')
                    images=request.FILES.getlist('images')
                    videos=request.FILES.getlist('video')   
                    address=request.POST['address1']
                    address2=request.POST['address2']
                    address2=address2.title()
                    city=request.POST['city']
                    city=city.title()
                    state=request.POST['state']
                    pincode=request.POST['zip']
                    mapurl=request.POST['googleurl']
                    description=request.POST['description']
                    imgid=request.POST['imgid']
                    vidid=request.POST['vidid']
                    imgid=list(map(int,imgid.split()))
                    vidid=list(map(int,vidid.split()))
                    pro=Property.objects.get(id=my_id)
                    pro.rentorsale=rentorsale
                    pro.propertytype=propertytype
                    pro.floornumber=floornumber
                    pro.propertyage=propertyage
                    pro.propertysize=propertysize
                    pro.totalrooms=totalrooms
                    pro.bedrooms=bedrooms
                    pro.bathrooms=bathrooms
                    pro.money=money
                    pro.tenantspreferred=tenantspreferred
                    pro.furnishing=furnishing
                    pro.amenities=amenities
                    pro.address=address
                    pro.address2=address2
                    pro.city=city
                    pro.state=state
                    pro.pincode=pincode
                    pro.mapurl=mapurl
                    pro.description=description
                    pro.save()
                    s="Changes saved"
                    for i in imgid:
                        img=Image.objects.get(id=i)
                        img.delete()
                    for i in vidid:
                        vid=Video.objects.get(id=i)
                        vid.delete()
                    for i in images:
                        img=Image(prop=pro,image=i)
                        img.save()
                    for i in videos:
                        vid=Video(proper=pro,video=i)
                        vid.save()
            try:
                propertyobj=Property.objects.get(id=my_id)
                imgobj=Image.objects.filter(prop=propertyobj)
                videoobj=Video.objects.filter(proper=propertyobj)
                print(propertyobj,imgobj,videoobj) 
            except Product.DoesNotExist:
                raise Http404
            context={
                "pro": propertyobj, "img":imgobj, "vid":videoobj, "mesg": s,
            }
        except:
            try:
                propertyobj=Property.objects.get(id=my_id)
                imgobj=Image.objects.filter(prop=propertyobj)
                videoobj=Video.objects.filter(proper=propertyobj)
                print(propertyobj,imgobj,videoobj) 
            except Product.DoesNotExist:
                raise Http404
            context={
                "pro": propertyobj, "img":imgobj, "vid":videoobj, "mesg": s,
            }
            pass
        return render(request,'editproperties.html',context)
    else:
        return redirect('login')
#@login_required(login_url='login')
def ownerDetails(request,my_id):
    if request.user.is_authenticated:
        context={}
        try:
            propertyobj=Property.objects.get(id=my_id)
        except Product.DoesNotExist:
            raise Http404
        context={
            "pro": propertyobj,
        }
        return render(request,'ownerdetails.html',context)
    else:
        return redirect('login')
#@login_required(login_url='login')
def filtersView(request):
    if request.user.is_authenticated:
        context={}
        if (request.POST.get('submit')=='SEARCH'):
            qs=Property.objects.all()
            img=Image.objects.all()
            video=Video.objects.all()
            l=request.POST['locality']
            l=l.title()  
            locality=re.findall(r"[\w']+",l)
            rentorsale=request.POST['rentorsale']
            propertytype=request.POST.getlist('propertytype')
            bedrooms=request.POST.getlist('bedrooms')
            tenanttype=request.POST.getlist('tenanttype')
            floor=request.POST.getlist('floor')
            maxprice=request.POST['max']
            minprice=request.POST['min']
            if(len(locality)==1):
                l1=qs.filter(address2__contains=locality[0])
                l2=qs.filter(city=locality[0])
                qs=l1|l2
            elif(len(locality)==2):
                l1=qs.filter(address2__contains=locality[0],city=locality[1])
                l2=qs.filter(address2__contains=locality[1],city=locality[0])
                qs=l1|l2
            else:   
                query = Q(address2__contains=locality[0])
                query.add(Q(city=locality[0]), Q.OR)
                for i in range(1,len(locality)):
                    query.add(Q(city=locality[i]), Q.OR)
                    query.add(Q(address2__contains=locality[i]), Q.OR) 
                qs=qs.filter(query)
            print(qs)
            qs=qs.filter(rentorsale=rentorsale)
            if(len(propertytype)!=0 and qs):
                qs=qs.filter(propertytype__in=propertytype)
            if(len(bedrooms)!=0 and qs):
                if("5" in bedrooms):
                    qs=qs.filter(Q(bedrooms__in=bedrooms) | Q(bedrooms__gte=5))
                else:
                    qs=qs.filter(bedrooms__in=bedrooms)
            if(len(tenanttype)!=0 and qs):
                qs=qs.filter(tenantspreferred__in=tenanttype)
            if(len(floor)!=0 and qs):
                if("4" in floor):
                    qs=qs.filter(Q(floornumber__in=floor) | Q(floornumber__gte=4))
                else:
                    qs=qs.filter(floornumber__in=floor)
            if(qs):
                qs=qs.filter(money__range=(minprice,maxprice))
            if(qs):
                propert = {
                    "proper": qs,"images": img,"videos":video,
                }
                return render(request,'property.html',propert)
            else:
                s="Sorry!!! No results found..."
                s1="Try removing some of the filters..."
                propert = {
                    "proper": qs,"images": img,"videos":video,"mesg":s,"mesg1":s1
                }
                return render(request,'property.html',propert)
        pro=Property.objects.all()
        locality=[]
        for i in pro:
            locality.append(i.city)
            locality.append(i.address2+","+i.city)
        l=set(locality)
        print(l)
        l1=list(l)
        print(l1)
        context={
            "locality":l1,
        }
        return render(request,'buyrent.html',context)
    else:
        return redirect('login')
#@login_required(login_url='login')
def propertyFavourite(request,my_id):
    if request.user.is_authenticated:
        try:
            propertyobj=Property.objects.get(id=my_id)
            print(propertyobj)
            if propertyobj.favourite.filter(id=request.user.id).exists():
                propertyobj.favourite.remove(request.user)
            else:
                propertyobj.favourite.add(request.user)
        except:
            pass
        return redirect('property_display',my_id)
    else:
        return redirect('login')
#@login_required(login_url='login')
def reviewsDisplay(request,my_id):
    if request.user.is_authenticated:
        try:
            propertyobj=Property.objects.get(id=my_id)  
        except:
            print("except")
        if request.method=='POST':
                context={}
                rating=request.POST['rating']
                title=request.POST['title']
                review=request.POST.get('review')
                try:
                    if(Review.objects.get(prop=propertyobj,user=request.user)):
                        reviewobj=Review.objects.get(prop=propertyobj,user=request.user)
                        reviewobj.title=title
                        reviewobj.content=review
                        reviewobj.stars=rating
                        reviewobj.save()
                        mesg="Changes Saved"
                except:
                    reviewobj=Review(prop=propertyobj,user=request.user,title=title,content=review,stars=rating)
                    reviewobj.save()
                    mesg="Submitted Successfully"
                content=reviewobj.content
                title=reviewobj.title
                stars=int(reviewobj.stars)
                starslist=[0,0,0,0,0]
                for i in range(0,stars):
                        starslist[i]=1
                context={'prop':propertyobj,'content':content,'title':title,'mesg':mesg,"starslist":starslist,'stars':stars}
                return render(request,'review.html',context)
        else:
            context={}
            content=""
            title=""
            stars=0
            starslist=[0,0,0,0,0]
            try:
                if(Review.objects.get(prop=propertyobj,user=request.user)):
                    reviewobj=Review.objects.get(prop=propertyobj,user=request.user)
                    content=reviewobj.content
                    title=reviewobj.title
                    stars=int(reviewobj.stars)
                    for i in range(0,stars):
                        starslist[i]=1
                    context={'prop':propertyobj,'content':content,'title':title,"starslist":starslist,'stars':stars}
                return render(request,'review.html',context)
            except:
                context={'prop':propertyobj,'content':content,'title':title,"starslist":starslist,'stars':stars}
                return render(request,'review.html',context)
    else:
        return redirect('login')
#@login_required(login_url='login')
def reviewsOwnerDisplay(request,my_id):
    if request.user.is_authenticated:
        try:
            propertyobj=Property.objects.get(id=my_id)  
        except:
            raise Http404
        context={}
        try:
                if(Review.objects.get(prop=propertyobj,user=request.user)):
                    reviewobj=Review.objects.get(prop=propertyobj,user=request.user)
                    content=reviewobj.content
                    title=reviewobj.title
                    stars=int(reviewobj.stars)
                    for i in range(0,stars):
                        starslist[i]=1
                    context={'prop':propertyobj}
                return render(request,'reviewsowner.html',context)
        except:
                context={'prop':propertyobj}
                return render(request,'reviewsowner.html',context)
    else:
        return redirect('login')
#@login_required(login_url='login')
def aboutView(request):
    if request.user.is_authenticated:
        return render(request,'about.html')
    else:
        return redirect('login')
    
