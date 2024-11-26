#game/consumers.py
import json
from .models import Registration, Response, Question
from .serializers import QuestionSerializer
from channels.layers import get_channel_layer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class QuizConsumer(WebsocketConsumer):
    def connect(self):
        slug = self.scope['url_route']['kwargs']['slug']
   
        game  = Registration.objects.get(slug=slug)  
        self.room_group_name = game.slug
        if game.online_count > 0:
          
            async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
                )
            self.accept()

            if Response.objects.filter(game=game,partner1__isnull=False,partner2__isnull=False).exists():
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'next_question',
                        'slug':slug
                    }
                )
            else:            
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'start_question',
                        'joined': True,
                        'slug':slug
                    }
                )
            
        else:

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            if game.online_count == 0:       
                game.online_count = game.online_count + 1
                game.save()

            self.accept()
    

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        option = text_data_json['option']
        receive_type = text_data_json['type']       
        if receive_type == "answer_submit":
            questionid = text_data_json['question']
            option = text_data_json['option']
            slug = text_data_json['slug']
            sender = text_data_json['gender']  #text_data_json['sender']
            game = Registration.objects.get(slug=slug)
            question = Question.objects.get(id=questionid)
            if sender == "male":
                answer, created = Response.objects.get_or_create(
                    game=game,
                    question=question,
                )

                if  option == "0":
                    answer.partner1 = False
                else:
                  
                    answer.partner1 = True
                answer.save()

                if Response.objects.filter(game=game,question=question,partner2__isnull=False).exists():

                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type':'next_question',
                            'slug':slug
                        }
                    )

            elif sender == "female":
            
                answer, created = Response.objects.get_or_create(
                    game=game,
                    question=question,
                )
                
                if  option == "0":
                    answer.partner2 = False
                else:
                  
                    answer.partner2 = True
                answer.save()

                if Response.objects.filter(game=game,question=question,partner1__isnull=False).exists():

                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type':'next_question',
                            'slug':slug
                        }
                    )




        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_messagee',
                'option':option
            }
        )

    def chat_messagee(self, event):
        option = event['option']

        self.send(text_data=json.dumps({
            'type':'option',
            'option':option
        }))


    def start_question(self, event):
        last_response = Response.objects.filter(game__slug=event['slug']).last()
        game = Registration.objects.get(slug=event['slug'])


        if last_response == None:
            question = game.questions.all().first()           
            data = QuestionSerializer(question)
        else:
            question = game.questions.all().first()           
            data = QuestionSerializer(question)


        self.send(text_data=json.dumps({
            'type':'joined',
            'question':data.data          
        }))



    def next_question(self, event):
        game  = Registration.objects.get(slug=event['slug'])     

        if game.attended_question_count  == game.no_of_questions:
            game.is_completed = True
            game.save()           
            self.send(text_data=json.dumps({
            'type':'show_report',
            'male_negative': game.male_negative_mark,
            'female_negative': game.female_negative_mark,
            'male_name':str(game.partner1),
            'female_name':str(game.partner2)

            }))
        else:

            no_of_questions_attended = game.attended_question_count   
            questions = list(game.questions.all())       
            question = questions[no_of_questions_attended]              
            data = QuestionSerializer(question)
            self.send(text_data=json.dumps({
                'type':'next_question',
                'question':data.data,
                'male_negative': game.male_negative_mark,
                'female_negative': game.female_negative_mark

            }))



    def disconnect(self, close_code):
        # Called when the socket closes

        slug = self.scope['url_route']['kwargs']['slug']
   
        game  = Registration.objects.get(slug=slug)
        self.room_group_name = game.slug

        #count  = len(self.channel_layer.groups.get(game.slug, {}).items())
        #if count == 1:

        if game.online_count == 1:
            game.online_count -=1
            game.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'stop_question',
                'joined': False
            }
        )
            


    def stop_question(self, event):
        
        self.send(text_data=json.dumps({
            'type':'discontinued'            
        }))
    
    


