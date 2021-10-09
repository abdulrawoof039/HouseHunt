from django.db import models
from django.contrib.auth.models import AbstractUser
class Accountuser(AbstractUser):
    phonenum=models.CharField(max_length=10)
    is_favourite=models.BooleanField(default=False)
class Property(models.Model):
    user=models.ForeignKey(Accountuser, on_delete=models.CASCADE)
    rentorsale=models.CharField(max_length=255,default="")
    propertytype=models.CharField(max_length=255,default="")
    floornumber=models.IntegerField()
    propertyage=models.IntegerField()
    propertysize=models.IntegerField()
    totalrooms=models.IntegerField()
    bedrooms=models.IntegerField()
    bathrooms=models.IntegerField()
    money=models.IntegerField()          
    tenantspreferred=models.CharField(max_length=255,default="")
    furnishing=models.CharField(max_length=255,default="")
    amenities=models.CharField(max_length=255,default="")
    address=models.CharField(max_length=255,default="")
    address2=models.CharField(max_length=255,default="")
    city=models.CharField(max_length=255,default="")
    state=models.CharField(max_length=255,default="")
    pincode=models.CharField(max_length=255,default="")
    mapurl=models.URLField(max_length= 200,default="")
    description=models.CharField(max_length=500,default="")
    favourite=models.ManyToManyField(Accountuser,related_name='favourite',blank=True)
    verifiedimages=models.CharField(max_length=10,default="No")
    verifiedvideos=models.CharField(max_length=10,default="No")
    verifiedpropertydetails=models.CharField(max_length=10,default="No")
    verifiedcost=models.CharField(max_length=10,default="No")
    verifiedproperty=models.CharField(max_length=30,default="Not Verified")
    emailstatus=models.CharField(max_length=20,default="NotSent")
    def get_totalreviews(self):
        print(len(self.reviews.values()))
        return len(self.reviews.values())
    def get_stars(self):
        l=[0,0,0,0,0]
        print(self.reviews.values())
        for i in self.reviews.values():
            l[int(i['stars'])-1]=l[int(i['stars'])-1]+1
        return l
    def get_ratingstr(self):
        total=sum(int(review['stars']) for review in self.reviews.values())
        if(self.reviews.count()!=0):
            count= total / self.reviews.count()
            format_float = "{:.2f}".format(count)
            return (format_float)
        else:
            return 0
    def get_rating(self):
        total=sum(int(review['stars']) for review in self.reviews.values())
        if(self.reviews.count()!=0):
            count= total / self.reviews.count()
            return (count)
        else:
            return 0
class Image(models.Model):
    prop=models.ForeignKey(Property,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images/')
class Video(models.Model):
    proper=models.ForeignKey(Property,on_delete=models.CASCADE)
    video=models.FileField(upload_to='videos/')
class Review(models.Model):
    prop=models.ForeignKey(Property,related_name='reviews',on_delete=models.CASCADE)
    user=models.ForeignKey(Accountuser,related_name='reviews',on_delete=models.CASCADE)
    title=models.CharField(max_length=200,default="")
    content=models.TextField()
    stars=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    