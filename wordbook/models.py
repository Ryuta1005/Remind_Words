from django.db import models
import datetime

class Word(models.Model):
    word_id=models.IntegerField()
    english=models.CharField(max_length=300)
    japanese=models.CharField(max_length=300)
    supplement=models.CharField(max_length=300)
    category=models.CharField(max_length=100)
    created_date=models.DateField(default=datetime.date.today())
    correct=models.BooleanField(default=True)#直近の正解不正解
    learned_date=models.DateField(default=datetime.date.today())#最後に解いた日
    learned_count=models.IntegerField(default=0)#解いた回数
    intelligibility=models.IntegerField(default=0)#理解度（正解すれば+１、不正解でマイナス１、理解度によって次解く日を決める）
    last_word_flag=models.BooleanField(default=True)