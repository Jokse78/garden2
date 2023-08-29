from django.shortcuts import render, redirect
from .forms import SekluApskaiciavimoForma, AugaluBuklesForma, AugalasForma, DarzoPlanasForma, AugaluVietaForma
from .models import Veisle, Darzas, AugaluBukle, Augalas, DarzoPlanas, AugaluVieta
from django.conf import settings
from twilio.rest import Client
from django.core.mail import send_mail

def index(request):
    return render(request, 'garden_app/index.html')
def veisles_sarasas(request):
    veisles = Veisle.objects.all()
    return render(request, 'vaisiu_sodinimas/veisles_sarasas.html', {'veisles': veisles})


def mano_darzai(request):
    if request.user.is_authenticated:
        darzai = Darzas.objects.filter(savininkas=request.user)
        return render(request, 'vaisiu_sodinimas/mano_darzai.html', {'darzai': darzai})
    else:
        return render(request, 'vaisiu_sodinimas/mano_darzai.html')

def redaguoti_profilį(request):
    if request.method == 'POST':
        forma = ProfilisRedagavimoForma(request.POST, instance=request.user.profilis)
        if forma.is_valid():
            forma.save()
            return redirect('mano_profilis')
    else:
        forma = ProfilisRedagavimoForma(instance=request.user.profilis)
    return render(request, 'vaisiu_sodinimas/redaguoti_profilį.html', {'forma': forma})

# Vaizdas, kuris leidžia vartotojams įvesti daržo plotą ir pasirinkti veislę.
# Taip pat apskaičiuoja reikiamą sėklų kiekį pagal pasirinktą veislę.

def apskaiciuoti_seklu_kieki(request):
    if request.method == 'POST':
        forma = SekluApskaiciavimoForma(request.POST)
        if forma.is_valid():
            veisle = forma.cleaned_data['veisle']
            darzo_plotas = forma.cleaned_data['darzo_plotas']
            seklu_kiekis = veisle.sėklų_kiekis_per_arą * darzo_plotas
            return render(request, 'vaisiu_sodinimas/seklu_apskaiciavimas_rezultatai.html', {'seklu_kiekis': seklu_kiekis})
    else:
        forma = SekluApskaiciavimoForma()
    return render(request, 'vaisiu_sodinimas/seklu_apskaiciavimas.html', {'forma': forma})

# Vaizdas, kuris leidžia vartotojams įvesti augalų būklės duomenis.
def sekti_bukle(request, darzas_id):
    darzas = Darzas.objects.get(id=darzas_id)

    if request.method == 'POST':
        forma = AugaluBuklesForma(request.POST)
        if forma.is_valid():
            bukle = forma.save(commit=False)
            bukle.darzas = darzas
            bukle.save()
            return redirect('mano_darzai')  # Galite nukreipti į kitą puslapį
    else:
        forma = AugaluBuklesForma()
    return render(request, 'vaisiu_sodinimas/sekti_bukle.html', {'forma': forma, 'darzas': darzas})

# Funkciją, kuri leidžia vartotojui pasirinkti, kaip jis nori gauti priminimus (el. paštu, SMS ar abu variantus).
def siusti_priminimus(request, darzas_id):
    darzas = Darzas.objects.get(id=darzas_id)

    if request.method == 'POST':
        pasirinkimas = request.POST.get('pasirinkimas')

        if pasirinkimas == 'email':
            send_mail(
                'Priminti apie daržo darbus',
                'Tai priminimas apie daržo darbus.',
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )

        elif pasirinkimas == 'sms':
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                to=request.user.profilis.telefonas,  # Gauti telefono numerį iš vartotojo profilio
                from_=settings.TWILIO_PHONE_NUMBER,
                body='Tai priminimas apie daržo darbus.'
            )

        return render(request, 'vaisiu_sodinimas/priminimo_issiuntimas.html', {'pasirinkimas': pasirinkimas})

    return render(request, 'vaisiu_sodinimas/siusti_priminimus.html', {'darzas': darzas})

# Funkciją, kuri leidžia vartotojui filtruoti įrankių sąrašą pagal įvairius kriterijus.
def filtruoti_irankius(request):
    irankiai = Irankis.objects.all()

    kategorija = request.GET.get('kategorija')
    jėgos_šaltinis = request.GET.get('jėgos_šaltinis')
    kaina = request.GET.get('kaina')

    if kategorija:
        irankiai = irankiai.filter(kategorija=kategorija)

    if jėgos_šaltinis:
        irankiai = irankiai.filter(jėgos_šaltinis=jėgos_šaltinis)

    if kaina:
        irankiai = irankiai.filter(kaina__lte=kaina)

    return render(request, 'vaisiu_sodinimas/filtruoti_irankius.html', {'irankiai': irankiai})

# Funkcionalumas paieškai pagal pavadinimą.
def filtruoti_irankius(request):
    irankiai = Irankis.objects.all()

    # Filtravimas pagal kitus kriterijus (kaip anksčiau)

    paieska = request.GET.get('paieska')
    if paieska:
        irankiai = irankiai.filter(pavadinimas__icontains=paieska)

    return render(request, 'vaisiu_sodinimas/filtruoti_irankius.html', {'irankiai': irankiai})

# Vaizdas, kuris leidžia vartotojui peržiūrėti augalų katalogą ir pridėti naujus augalus.

def augalu_katalogas(request):
    augalai = Augalas.objects.all()
    return render(request, 'vaisiu_sodinimas/augalu_katalogas.html', {'augalai': augalai})

def prideti_nauja_augala(request):
    if request.method == 'POST':
        forma = AugalasForma(request.POST, request.FILES)
        if forma.is_valid():
            forma.save()
            return redirect('augalu_katalogas')
    else:
        forma = AugalasForma()
    return render(request, 'vaisiu_sodinimas/prideti_nauja_augala.html', {'forma': forma})

# Vaizdas, kuris leidžia vartotojui sukurti daržo planą ir pažymėti augalų buvimo vietas.
def sukurti_darzo_plana(request):
    if request.method == 'POST':
        plano_forma = DarzoPlanasForma(request.POST)
        if plano_forma.is_valid():
            darzo_planas = plano_forma.save(commit=False)
            darzo_planas.savininkas = request.user
            darzo_planas.save()
            return redirect('sukurti_darzo_plana')
    else:
        plano_forma = DarzoPlanasForma()

    return render(request, 'vaisiu_sodinimas/sukurti_darzo_plana.html', {'plano_forma': plano_forma})


def prideti_augalu_vieta(request, darzo_planas_id):
    darzo_planas = DarzoPlanas.objects.get(id=darzo_planas_id)

    if request.method == 'POST':
        vieta_forma = AugaluVietaForma(request.POST)
        if vieta_forma.is_valid():
            vieta = vieta_forma.save(commit=False)
            vieta.darzo_planas = darzo_planas
            vieta.save()
            return redirect('prideti_augalu_vieta', darzo_planas_id=darzo_planas_id)
    else:
        vieta_forma = AugaluVietaForma()

    return render(request, 'vaisiu_sodinimas/prideti_augalu_vieta.html',
                  {'vieta_forma': vieta_forma, 'darzo_planas': darzo_planas})
