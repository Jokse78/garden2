from django.db import models
from django.contrib.auth.models import User

class Veisle(models.Model):
    pavadinimas = models.CharField(max_length=100)
    aprasymas = models.TextField()
    vieta = models.CharField(max_length=100)
    zeme = models.CharField(max_length=100)
    iranga = models.CharField(max_length=200)
    siltnamis_laukas = models.CharField(max_length=50)
    sėklų_kiekis_per_arą = models.DecimalField(max_digits=5, decimal_places=2)
class Darzas(models.Model):
    savininkas = models.ForeignKey(User, on_delete=models.CASCADE)
    plotas_arais = models.FloatField()
    veisle = models.ForeignKey(Veisle, on_delete=models.CASCADE)
    pasodinimo_data = models.DateField()
    sodinimas_is_seklu = models.BooleanField(default=False)
    sodinuku_pikiavimas = models.DateField(null=True, blank=True)
    sodinuku_perkelimas_lysviuose = models.DateTimeField(null=True, blank=True)
    tresimas = models.DateField(null=True, blank=True)
    laistymas = models.DateField(null=True, blank=True)
    purkstymas = models.DateField(null=True, blank=True)
    derliaus_nuemimas = models.DateField(null=True, blank=True)
    pastabos = models.TextField(null=True, blank=True)

class SodoDarbas(models.Model):
    darzas = models.ForeignKey(Darzas, on_delete=models.CASCADE)
    darbo_data = models.DateField()
    pavadinimas = models.CharField(max_length=100)
    aprasymas = models.TextField()


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefonas = models.CharField(max_length=20, blank=True)
    vietove = models.CharField(max_length=100, blank=True)
    profilio_paveikslelis = models.ImageField(upload_to='profile_images/', blank=True)

    def __str__(self):
        return self.user.username


# Norint leisti vartotojams sekti augalų būklę,
# galima sukurti papildomą modelį, kuris saugotų informaciją apie augalų stebėjimus
# ir būklės pokyčius.

class AugaluBukle(models.Model):
    darzas = models.ForeignKey(Darzas, on_delete=models.CASCADE)
    data = models.DateField()
    sėklų_isaugo = models.PositiveIntegerField(default=0)
    augalai_auga = models.TextField()
    kenkejai_ligos = models.TextField()

    def __str__(self):
        return f'Būklė {self.darzas} - {self.data}'
# Modelis apie augalų informaciją.
class Augalas(models.Model):
    pavadinimas = models.CharField(max_length=100)
    nuotrauka = models.ImageField(upload_to='augalu_nuotraukos/')
    aprasymas = models.TextField()
    auginimo_informacija = models.TextField()

    def __str__(self):
        return self.pavadinimas
# Modelį, kuris saugoja informaciją apie daržo planą ir augalų buvimo vietas.
class DarzoPlanas(models.Model):
    savininkas = models.ForeignKey(User, on_delete=models.CASCADE)
    pavadinimas = models.CharField(max_length=100)

class AugaluVieta(models.Model):
    darzo_planas = models.ForeignKey(DarzoPlanas, on_delete=models.CASCADE)
    augalas = models.ForeignKey(Augalas, on_delete=models.CASCADE)  # Nurodykite, iš kurio modelio yra "Augalas"
    x_koord = models.PositiveIntegerField()
    y_koord = models.PositiveIntegerField()


# Pridėta laukai savo modeliuose, skirti failams saugoti.
class Failas(models.Model):
    pavadinimas = models.CharField(max_length=100)
    failas = models.FileField(upload_to='failai/')
    darzas = models.ForeignKey(Darzas, on_delete=models.CASCADE, blank=True, null=True)
    augalas = models.ForeignKey(Augalas, on_delete=models.CASCADE, blank=True, null=True)

# Modelis, kuris saugoja informaciją apie pranešimu.
class Pranesimas(models.Model):
    siuntejas = models.ForeignKey(User, on_delete=models.CASCADE)
    gavetojas = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gauti_pranesimai')
    tema = models.CharField(max_length=100)
    tekstas = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    perskaitytas = models.BooleanField(default=False)

# Pirmiausia, turite sukurti duomenų struktūrą ir būdus,
# kaip surinkti reikiamus duomenis apie vartotojų daržus ir sėklų išaugimo dinamiką.
# Jūsų modeliuose turite įtraukti laukus, kuriuose saugosite šią informaciją.
class Darzas(models.Model):
    savininkas = models.ForeignKey(User, on_delete=models.CASCADE)
    plotas = models.DecimalField(max_digits=5, decimal_places=2)
    # Kitos laukų deklaracijos

class Sodinimas(models.Model):
    darzas = models.ForeignKey(Darzas, on_delete=models.CASCADE)
    data = models.DateField()
    seldiniu_skaicius = models.PositiveIntegerField()
    # Kitos laukų deklaracijos

