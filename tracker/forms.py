from django import forms
from .models import StudySession




class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['date','subject','duration','resource','difficulty','mood','notes']
        """Formda hangi alanların görüneceğini belirliyor
        kullanıcı fields içindeki alanları dolduracak"""

        """Her model alanı için bir form bileşeni(widget) tanımlanıyor
        
        attrs{...}ile html özellikleri ekleniyor örneğin class,placeholder,type böylce bootstrap ile uyumlu hale gelir"""
        widgets={
            'date':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'subject':forms.TextInput(attrs={'class':'form-control','placeholder':'Konu'}),
            'duration':forms.NumberInput(attrs={'class':'form-control','placeholder':'Dakika'}),
            'resource':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Kaynak'}),
            'difficulty':forms.Select(attrs={'class':'form-control'}, choices=[(i, str(i)) for i in range(1, 6)]),
            'mood':forms.Select(attrs={'class':'form-control'},choices=[(i, f"{i} /10") for i in range(1,11)]),
            'notes':forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Notlar'}),
        }


