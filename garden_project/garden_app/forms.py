from django import forms
from .models import Profilis, Veisle, AugaluBukle, Augalas, DarzoPlanas, AugaluVieta, Failas, Pranesimas, Sodinimas

# Forma, kuri ledžia vartotojams redaguoti savo profilį. Ši forma turi laukus, atitinkančius Profilis modelio laukus.
class ProfilisRedagavimoForma(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['telefonas', 'vietove', 'profilio_paveikslelis']

# Forma, kuri ledžia vartotojams pasirinkti veislę ir įvesti daržo plotą.
class SekluApskaiciavimoForma(forms.Form):
    veisle = forms.ModelChoiceField(queryset=Veisle.objects.all(), empty_label=None)
    darzo_plotas = forms.FloatField()
# Formą, kuri leidžia vartotojams įvesti informaciją apie augalų būklę.
class AugaluBuklesForma(forms.ModelForm):
    class Meta:
        model = AugaluBukle
        fields = ['data', 'sėklų_isaugo', 'augalai_auga', 'kenkejai_ligos']

# Forma, kuri leis įkelti naujus augalus į katalogą.
class AugalasForma(forms.ModelForm):
    class Meta:
        model = Augalas
        fields = ['pavadinimas', 'nuotrauka', 'aprasymas', 'auginimo_informacija']

# Formą, kuri leidžia vartotojams sukurti daržo planą ir pažymėti augalų buvimo vietas.
class DarzoPlanasForma(forms.ModelForm):
    class Meta:
        model = DarzoPlanas
        fields = ['pavadinimas']

class AugaluVietaForma(forms.ModelForm):
    class Meta:
        model = AugaluVieta
        fields = ['augalas', 'x_koord', 'y_koord']
# Formą, kurioje leidžiama vartotojui įkelti failus.
class FailoIkelimasForma(forms.ModelForm):
    class Meta:
        model = Failas
        fields = ['pavadinimas', 'failas']
# Formą, kuri leidžia administratoriui siųsti pranešimus:
class PranesimoSiuntimoForma(forms.ModelForm):
    class Meta:
        model = Pranesimas
        fields = ['gavetojas', 'tema', 'tekstas']

