from django import forms

class AdditionForm(forms.Form): 
    word_id=forms.IntegerField()
    english=forms.CharField(max_length=300)
    japanese=forms.CharField(max_length=300)
    supplement=forms.CharField(max_length=100,widget=forms.Textarea,required=False)
    category=forms.CharField(max_length=100)

class ResultForm(forms.Form): 
    result_data=[
        (True,"○"),
        (False,"✕")
    ]
    choice=forms.ChoiceField(label="radio",choices=result_data,widget=forms.RadioSelect())