from django.db import models
from django.utils.text import slugify 
from ckeditor_uploader.fields import RichTextUploadingField
import datetime
from django.db.models import Q
from account.models import User
# Create your models here.

gender_choices =(
    ("m", "Male"),
    ("f", "Female")
)

negative_choices =(
    ("TM", "To Me"),
    ("TO", "To Opposite")
)

class Relationship_Started_Year(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
class Question_Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
    
class Question(models.Model):    
    name=models.CharField(max_length=30)
    description=RichTextUploadingField()
    question_category = models.ForeignKey(Question_Category,null=True, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True,null=True)   
    negative_mark_to = models.CharField(choices=negative_choices,max_length=2,default="TM")

    def __str__(self):
        return self.name

    @property
    def options(self):
        return self.option_set.values()


    class Meta:
        ordering = ('id',)



class Option(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    description=models.TextField()
    value=models.FloatField(default=0)

    def __str__(self):
        return self.description

class Registration(models.Model):
    partner1 = models.ForeignKey(User, on_delete=models.CASCADE)
    partner2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="partner2",null=True,blank=True)
    slug  = models.SlugField(max_length=200,unique=True,blank=True)
    #relationship_started_year = models.ForeignKey(Relationship_Started_Year, on_delete=models.SET_NULL,null=True)
    game_round  = models.BigIntegerField(default=1)
    questions = models.ManyToManyField(Question,null=True,blank=True)
    is_completed = models.BooleanField(default=False)
    online_count = models.BigIntegerField(default=0) 

    def save(self, *args, **kwargs):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime('%S%f')
        if not self.slug:
            name = slugify((self.partner1.first_name.strip().replace("-", ""))[:5]+formatted_time)
            self.slug = name.replace("-", "")

        '''
        questions = list(Question.objects.all().order_by('?').values_list('id',flat=True)[:10])
        print(questions)
        for question in questions:
            self.questions = question
        '''
        super(Registration, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug
    
    class Meta:
        ordering = ('id',)

    @property
    def male_negative_mark(self):
        return Response.objects.filter(Q(question__negative_mark_to="TM",partner1=True) | Q(question__negative_mark_to="TO",partner2=True) ,game=self).count() 


    @property
    def female_negative_mark(self):
        return  Response.objects.filter(Q(question__negative_mark_to="TM",partner2=True) | Q(question__negative_mark_to="TO",partner1=True) ,game=self).count()

    @property
    def no_of_questions(self):
        return self.questions.all().count()


    @property
    def attended_question_count(self):       
        return Response.objects.filter(game=self,partner1__isnull=False,partner2__isnull=False).count()
    
    @property
    def male_name(self):       
        if self.partner1.gender == "m":
            return str(self.partner1)
        else:
            return str(self.partner2)

    
    @property
    def female_name(self):       
        if self.partner1.gender == "f":
            return str(self.partner1)
        else:
            return str(self.partner2)

class Response(models.Model):
    partner1 = models.BooleanField(blank=True,null=True) #male answer
    partner2 = models.BooleanField(blank=True,null=True) #female answer
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    game = models.ForeignKey(Registration,on_delete=models.CASCADE)

    def qdescription(self):
        return str(self.question.description)


