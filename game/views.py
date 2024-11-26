from django.shortcuts import render
from .models import Registration, Question
from django.db.models import Q
from django.shortcuts import redirect
from django.http import JsonResponse


# Create your views here.

def landing(request):
    if request.user.is_authenticated:
        return redirect('login')
    return render(request, "game/landing.html", {})


def check_game_slug(request,slug):
    data = dict()
    try:
        game = Registration.objects.get(slug=slug,is_completed=False)
        is_valid = True
    except:
        is_valid = False
    data['is_valid'] = is_valid
    return JsonResponse(data)


    


def home(request):
    if request.user.is_authenticated:
        game1 = None
        game2 = None
        games = Registration.objects.filter(Q(partner1=request.user) | Q (partner2=request.user))
        two_round_completed = False
        if len(games) == 1:
            getgame1 =  Registration.objects.get(Q(partner1=request.user) | Q (partner2=request.user))
            if getgame1.is_completed:
                game2 = Registration.objects.create(partner1=request.user,game_round=2) 
                questions = Question.objects.filter(id__in=(5,6,11,12,13,14,16,18,20,21))                
                game2.questions.add(*questions)   

            else:
                game1 = getgame1

           
        if len(games) == 2:
            getgame2 =  Registration.objects.filter(Q(partner1=request.user) | Q (partner2=request.user)).last()
            if not  getgame2.is_completed:              
                game2 = getgame2
            else:
                two_round_completed = True
       


        if len(games)  > 2:

            two_round_completed = True

 
   
        if not games:
            game1 = Registration.objects.create(partner1=request.user,game_round=1) 
            questions = Question.objects.filter(id__in=(1,2,3,4,8,9,10,15,17,19))
            game1.questions.add(*questions)   

              



        '''
        elif Registration.objects.filter(Q(partner1=request.user) | Q (partner2=request.user),is_completed=True).exists():
            game2 = Registration.objects.create(partner1=request.user)
        else:
            game1 = Registration.objects.filter(Q(partner1=request.user) | Q (partner2=request.user),is_completed=True).first()
        '''

        return render(request, "game/home.html", {"games": games,'game1':game1,'game2':game2,"title":"Home",'two_round_completed':two_round_completed})
    else:
        return redirect('login')



def game(request,slug):
    game = Registration.objects.get(slug=slug)

    if game.is_completed:
        if request.user == game.partner1:
            partner_name = str(game.partner2)
        else:
            partner_name = str(game.partner1)

        return render(request, "game/quiz.html", {'game':game,'is_completed':True,'noofquestions':game.no_of_questions,'partner_name':partner_name})
    else:

        if request.user.is_authenticated:
            #delete not completed game
            Registration.objects.filter(Q(partner1=request.user) | Q (partner2=request.user),is_completed=False).exclude(slug=slug).delete()

            get_completed_game_count = Registration.objects.filter(Q(partner1=request.user) | Q (partner2=request.user),is_completed=True).count()

            if get_completed_game_count  > 1:
                return render(request, "game/game_completed.html")
        
            #get_games = Registration.objects.filter(Q(partner1=request.user) | Q (partner2=request.user),is_completed=False).exclude(id=game.id).delete()
        
            if "invited_game" in request.session.keys():
                del request.session["invited_game"]

            gender = None
            if request.user == game.partner1:
                gender = game.partner1.gender
                if gender == "m":
                    gender = "male"
                else:
                    gender = "female"
            else:
                game.partner2 = request.user
                game.save()
                if game.partner1.gender == "m":
                    gender = "female"
                else:
                    gender = "male"


            return render(request, "game/quiz.html", {"slug": slug,"gender":gender,'noofquestions':game.no_of_questions,'is_completed':False,'game':game})
        else:
            request.session['invited_game'] = slug

            return redirect('login')




def new_landing(request):
    return render(request, "game/new_landing.html",)


def cfr(request):
    frfb = Registration.objects.filter(is_completed=True,game_round=1)
    srfb = Registration.objects.filter(is_completed=True,game_round=2)
    return render(request, "game/cfr.html",{'frfb':frfb,'srfb':srfb})


