from django import forms

class OrderForm(forms.Form):
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class":"", "placeholder":"Masalan: +998 90 123 45 67"})
    )
    location = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class":"", "placeholder":"Manzil / Lokatsiya"})
    )
    payment_method = forms.ChoiceField(
        choices=[("cash","Naqt"),("card","Karta")],
        widget=forms.Select()
    )
