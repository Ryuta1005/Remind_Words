from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Word
from .forms import AdditionForm
from .forms import ResultForm
import datetime


remind_lateness_list=[
                    datetime.timedelta(days=1),
                    datetime.timedelta(days=3),
                    datetime.timedelta(days=7),
                    datetime.timedelta(days=14),
                    datetime.timedelta(days=30),
                    datetime.timedelta(days=90),
                    ]
class Index(TemplateView):
    def __init__(self):
        self.params={
            "addition":"addition",
            "word_list":"word_list",
            "index":"index",
            "remind_list":"remind_list",
        }
    
    def get(self,request):
        return render(request,"wordbook/index.html",self.params)

    def post(self,request):
        return render(request,"wordbook/index.html",self.params)

class Addition(TemplateView):
    def __init__(self):
        self.params={
            "addition":"addition",
            "word_list":"word_list",
            "index":"index",
            "remind_list":"remind_list",
            "message":"",
            "form":AdditionForm()
        }
    
    def get(self,request):
        return render(request,"wordbook/addition.html",self.params)
    
    def post(self,request):
        next_word_id=1
        while Word.objects.filter(id=next_word_id).exists()==True:
            next_word=Word.objects.get(id=next_word_id)
            next_word.last_word_flag=False
            next_word.save()
            next_word_id=next_word_id+1

        if(request.method=="POST"):
            word_id=request.POST["word_id"]
            english=request.POST["english"]
            japanese=request.POST["japanese"]
            supplement=request.POST["supplement"]
            category=request.POST["category"]
            created_date=datetime.date.today()
            self.params["message"]=\
            "id:"+str(word_id)+\
            "<br>英語:"+english+\
            "<br>日本語:"+japanese+\
            "<br>補足:"+supplement+\
            "<br>カテゴリ:"+category+\
            "<br>登録日:"+str(created_date)
            # "<br>id:"+str(word_id)
            self.params["form"]=AdditionForm(request.POST)   
            word=Word(word_id=word_id,english=english,japanese=japanese,\
                category=category,created_date=created_date,supplement=supplement)
            word.save()
        return render(request,"wordbook/addition.html",self.params)

class WordList(TemplateView):
    def __init__(self):
        data=Word.objects.all()
        self.params={
            "addition":"addition",
            "word_list":"word_list",
            "index":"index",
            "remind_list":"remind_list",
            "data":data,
            "form":ResultForm(),
            "result":"None",
            "test":len(data)+1
        }
    
    def get(self,request):
        return render(request,"wordbook/word_list.html",self.params)
    
    def post(self,request):
        ch=request.POST["choice"]
        self.params["result"]=ch+"を選択しました"
        self.params["form"]=ResultForm(request.POST)
        return render(request,"wordbook/details.html",self.params)

class RemindList(TemplateView):
    def __init__(self):
        data=Word.objects.all()
        remind_words=[]
        data=Word.objects.all()
        comparsion_word=0
        for i in range(len(data)):
            if Word.objects.filter(id=i).exists()==True:
                comparsion_word=Word.objects.get(id=i)
                if comparsion_word.correct==True:
                    remind_date=comparsion_word.learned_date+remind_lateness_list[comparsion_word.intelligibility]
                elif comparsion_word.correct==False:
                    remind_date=comparsion_word.learned_date
                if remind_date<=datetime.date.today():
                    remind_words.append(comparsion_word)
        
        
        # test=[111,111,2,3,4,5,6,]
        # test=remind_words
        self.params={
            "addition":"addition",
            "word_list":"word_list",
            "index":"index",
            "remind_list":"remind_list",
            "data":data,
            "form":ResultForm(),
            "result":"None",
            "comparsion_word":comparsion_word,
            "remind_date":remind_date,
            "remind_words":remind_words,
        }
    
    def get(self,request):
        remind_words=[]
        data=Word.objects.all()
        comparsion_word=Word.objects.get(id=1)
        remind_date=comparsion_word.learned_date+remind_lateness_list[comparsion_word.intelligibility]
        return render(request,"wordbook/remind_list.html",self.params)
    
    def post(self,request):
        # ch=request.POST["choice"]
        # self.params["result"]=ch+"を選択しました"
        # self.params["form"]=ResultForm(request.POST)
        return render(request,"wordbook/details.html",self.params)

class Details(TemplateView):
    def __init__(self):
        data=Word.objects.all()
        self.params={
            "addition":"addition",
            "word_list":"word_list",
            "index":"index",
            "remind_list":"remind_list",
            "data":data,
            "details":"details",
            "result":"Noneee",
            "details":"details",
        }
    
    def get(self,request,num):
        detail=Word.objects.get(id=num)
        data=Word.objects.all()
        next_word_id=detail.id+1
        if detail.last_word_flag==False:
            while Word.objects.filter(id=next_word_id).exists()==False:
                next_word_id=next_word_id+1
        self.params={
            "addition":"addition",
            "word_list":"word_list",
            "index":"index",
            "remind_list":"remind_list",
            "data":data,
            "details":"details",
            "detail":detail,
            "form":ResultForm(),
            "next_word_id":next_word_id,
            "result":" ",
        }
        return render(request,"wordbook/details.html",self.params)
    
    def post(self,request,num):
        detail=Word.objects.get(id=num)
        data=Word.objects.all()
        next_word_id=detail.id+1
        if detail.last_word_flag==False:
            while Word.objects.filter(id=next_word_id).exists()==False:
                next_word_id=next_word_id+1
        self.params={
            "addition":"addition",
            "word_list":"word_list",
            "index":"index",
            "remind_list":"remind_list",
            "data":data,
            "details":"details",
            "detail":detail,
            "form":ResultForm(),
            "next_word_id":next_word_id,
            "result":"Noneee",
        }
        if(request.method=="POST"):
            detail=Word.objects.get(id=num)
            result=ResultForm(request.POST)
            ch=request.POST["choice"]
            self.params["result"]=ch+"を選択しました"
            self.params["form"]=ResultForm(request.POST)
            detail.correct=ch
            detail.learned_date=datetime.date.today()
            detail.learned_count=detail.learned_count+1
            if detail.correct=="True" and detail.intelligibility!=len(remind_lateness_list)-2:
                detail.intelligibility=detail.intelligibility+1
            elif detail.correct=="False" and detail.intelligibility!=0:
                detail.intelligibility=detail.intelligibility-1

            detail.save()
            # da=detail(correct=ch,learned_date=datetime.date.today())
            # da.save()
            # Word.objects.get(id=num).update(field=correct=ch,learned_date=datetime.date.today())
        # Word.save()
        # # return render(request,"wordbook/index.html",params)
        return render(request,"wordbook/details.html",self.params)

def edit(request,num):
    id_num=Word.objects.get(id=num)
    if(request.method=="POST"):
        result=ResultForm(request.POST,instance=id_num)
        result.save()
        return render(request,"wordbook/index.html",params)
    params={
            "addition":"addition",
            "word_list":"word_list",
            "index":"index",
            "form":ResultForm(),
        }
    return render(request,"wordbook/details.html",params)