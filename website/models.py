from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from firebase_admin import credentials, initialize_app, storage
from django.conf import settings
import random
# Category, Expertise, Userdata, UserExpertise, Messages, User, Resume

class Category(models.Model):
    category_name = models.CharField(null=True, max_length=100)
    design = models.CharField(null=False, max_length=100, default='success')

    def __str__(self):
        return self.category_name


class Expertise(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.text



class Userdata(models.Model):
    uid = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(null=True, max_length=100, default=None)
    last_name = models.CharField(null=True, max_length=100, default=None)
    github_link = models.CharField(null=True, max_length=300, default=None)
    website = models.CharField(null=True, max_length=300, default=None)
    profile_pic = models.CharField(null=True, max_length=350, default=None)
    background = models.CharField(null=True, max_length=300, default=None)
    experience_years = models.IntegerField(default=timezone.now().year)
    show = models.BooleanField(default=True)
    update = models.DateTimeField(default=timezone.now)
    salary_per_hour = models.IntegerField(default=0)
    details = models.CharField(null=True, max_length=1500, default=None)

    def is_valid(self):
        return self.first_name and self.last_name and self.userexpertise_set

    def get_new_mes(self):
        return len(self.messages_set.filter(mes_read=False).all())

    def get_all_mes(self):
        return self.messages_set.order_by('-id')
    
    def get_exp(self):
        all_exp = []
        for kkk in Expertise.objects.values('category_id').distinct().all():
            query = Category.objects.filter(pk = kkk['category_id'])
            if query: all_exp.append({'category':query[0].category_name, 'design':query[0].design, 'id':query[0].id})
        return all_exp
    
    def get_exp_details(self):
        result = self.get_exp()
        for each in result:
            each['expertise'] = UserExpertise.objects.filter(my_expertise__category__id = each['id'])
        return result

    def toJSON(self):
        years = timezone.now().year - self.experience_years
        return {"id": self.uid.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "github_link": self.github_link,
                "background": self.background,
                "website": self.website,
                "profile_pic": self.profile_pic,
                "experience": f'{years} - {years + 1}',
                "show": self.show,
                "update": self.update,
                "salary_per_hour": f'{self.salary_per_hour} ₪',
                "experience_titels": self.get_exp()}
    
    def __str__(self):
        return self.uid.username


class UserExpertise(models.Model):
    userdata = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    my_expertise = models.ForeignKey(Expertise, on_delete=models.CASCADE)
    description = models.CharField(null=True, max_length=500)


    def __str__(self):
        return self.my_expertise.text


class Messages(models.Model):
    user_to = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)
    mes_content = models.CharField(null=False, max_length=500)
    mes_from = models.CharField(null=False, max_length=100)
    mes_contact = models.CharField(null=False, max_length=100)
    mes_read = models.BooleanField(default=False)

    def read_set(self):
        if self.mes_read:
            return False
        else:
            self.mes_read = True
            self.save()
            return True

    def get_date_format(self):
        return self.pub_date.strftime('%d/%m/%Y %H:%M')

    def __str__(self):
        return self.mes_from

class Resume(models.Model):
    user = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    title = models.CharField(null=False, max_length=100)
    text = models.CharField(null=False, max_length=500)
    start_year = models.IntegerField(null=True)
    end_year = models.IntegerField(null=True)

