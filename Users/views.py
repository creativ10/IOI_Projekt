import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

# Create your views here.
from .models import ExtendedUser, Question
from .forms import NewQuestionForm

library = {
    "JAMSKI MEDVED IN ČELJUST JAMSKEGA MEDVEDA": {
        "slika": ["images/common/library/1. JAMSKI MEDVED.png", "images/common/library/1. ČELJUST JAMSKEGA LEVA.png"],
        "podrobnosti": ["Izumrla vrsta medveda pred 27.500 leti", "Najdemo jih po vsej evropi in delu Rusije.",
                        "Jamski medved je bil velik kot največji danes živeči medvedi, samci so v povprečju tehtali med 400 in 500 kg, samice pa 225–250."]
    },
    "DEBELAK": {
        "slika": ["images/common/library/2. DEBLAK.png"],
        "podrobnosti": ["Iz hrastovega debla, dolgo 9,3m", "v uporabi na prehodu iz bronaste v železno dobo (9. stoletje pr. n. št.).",
                        "Ta ugotovitev ni nenavadna, saj so se s takšnimi čolni ljudje pri nas in tudi drugod po Evropi prevažali še v novem veku. "
                        ],
        "najdišče": "Matena pri Iški Loki, Slovenija."
    },
    "DVODELNI OKLEP": {
        "slika": ["images/common/library/3. DVODELNI OKLEP.png"],
        "najdišče": "Novo Mesto",
        "podrobnosti": ["Oklep nakazuje na obstoj vladajoče družbene elite.",
                        "Oklep izhaja iz groba, v katerem so bili najdeni tudi drugi grobni pridatki: čelada, sulični osti, ščit, konjska oprema in keramične posode."]
    },
    "BLEJSKA ZLATA NAŠITKA": {
        "slika": ["images/common/library/4. ZLATA NAŠITKA.png"],
        "podrobnosti": ["Najstarejša zlata predmeta na področju slovenije.", "Koncentrični krogi, ki zelo verjetno simbolizirajo sonce"],
        "najdišče": "Bled",
        "obdobje_nastanka": "1300-1100 pr.kr.",

    },
    "HARPUNE": {
        "slika": ["images/common/library/5. HARPUNE.png"],
        "najdišče": "reka Ljubljanica",
        "obdobje_nastanka": "11.500-7.000 let pr. kr."
    },
    "HOMO HABILIS oziroma spretni človek": {
        "slika": ["images/common/library/6. HOMO HABILIS.png"],
        "podrobnosti": [
            "Je prva človeška oblika v človeški evoluciji.",
            "Živel je pred okoli 2,5 do 2 milijonoma let."
        ]
    },
    "HOMO ERECTUS oz. POKONČNI ČLOVEK": {
        "slika": ["images/common/library/7. HOMO ERECTUS.png"],
        "podrobnosti": [
            "Se je razvil iz homo Habilisa",
            "Najstarejše najdbe: prb. 1,6milijona let iz Afrike",
            "Okoli leta 400.000 pr. n. št., se je homo erectus razvil naprej v arhaičnega Homo sapiensa, ki se je iz Afrike prav tako razširil tudi v Evropo ter Azijo.",
            "Odkrije ogenj, kar mu omogoči peko mesa in vir svetlobe.",
            "Izdela orodje: pestnjak.",
            "Homo erectus se je združeval v ohlapne družbene skupine imenovane horda.Ena horda je štela nekje od 10 do 30 članov."
        ]
    },
    "HOMO NEANDERTALIS OZIROMA NEANDERTALEC": {
        "slika": ["images/common/library/8. NEANDERTALEC.png"],
        "podrobnosti": [
            "Poimenovan po dolini Neander v Nemčiji, kjer so našli prve ostanke",
            "Izhaja Homo Sapiensa, ki se rsazvije iz Homo Erektusa.",
            "Glede na najmlajše ostanke ocenjujejo, da je (iz neznanih vzrokov) izumrl pred 27.000 leti."
        ]
    },
    "HOMO SAPIENS ALI MISLEČI ČLOVEK": {
        "slika": ["images/common/library/9. HOMO SAPIENS.png"],
        "podrobnosti": ["Homo sapiens se je razvil pred okoli 200.000 leti v Afriki.", "Ne obstaja specifičen artefakt, ki bi natančno določil začetek te vrste.",
                        "Glavne značilnosti so: mišljenje, samozavedanje, lažje okostje od njegovih predniko in povečan volumen lobanje."
                        ]
    },
    "IDOL IZ LJUBLJANSKEGA BARJA": {
        "slika": ["images/common/library/10. IDOL IZ LJ BARJA.png"],
        "podrobnosti": ["Narejen iz gline (črno žgana)", "Verjetno je služil kot posoda saj ima na vrhu ustje in je votel."],
        "obdobje_nastanka:": "bakrena doba; prb. 3.000 pr. nšt. - ko so v Egiptu gradili piramide."
    },
    "SITULA IZ VAČ": {
        "slika": ["images/common/library/11. VAŠKA SITULA.png"],
        "najdišče": "Najdena na Vačah blizu Litije",
        "obdobje_nastanka": "1882",
        "zanimivosti": ["izkopal jo je kmet Janez Grilc, ki se je navduševal za arheologijo.",
                        "Situla je (bronasta pločevina) obredna posoda, ki je bila najverjetneje namenjena točenju pijače na slovesnostih.",
                        "Odseva tradicionalne vplive sredozemskega sveta.",
                        "V upodobitvah je opazen vpliv etruščanske umetnosti (motivi iz življenja vladajočega sloja)."
                        ]
    },
    "PIŠČAL IZ DIVJIH BAB": {
        "slika": ["images/common/library/12. PIŠČAL IZ DIVJIH BAB.png"],
        "obdobje_nastanka": "pred 60.000 let",
        "najdišče": "Divje babe (Lokacija obsega 45m dolgo in do 15m široko jamo, ki se nahaja 230m nad reko Idrijco blizu Cerkna)",
        "zanimivosti": ["Najstarejša piščal na svetu, izdelal jo je neandertalec iz stegnenice mladega jamskega medveda."],
        "link": "https://www.youtube.com/watch?v=EqAbtBO2_6Q"
    },
    "MEČ IZ JABELJ": {
        "slika": ["images/common/library/13. MEČ IZ JABELJ.png"],
        "obdobje_nastanka": "2. tisočletja pr. n. št.",
        "najdišče": "v ribniku blizu grada Jablje, Loka pri Mengšu.",
        "zanimivosti": ["Polnoročajni meči so bili v tistem času izredno redki.",
                        "Dragoceno bronasto orožje in posebej meči so bili v tistem času kot zaobljubne ali zahvalne daritve božanstvom pogosto darovani vodam."
                        ]
    },
    "MAMUT IZ NEVELJ": {
        "slika": ["images/common/library/14. MAMUT IZ NAVELJ.png"],
        "obdobje_nastanka": "starost 30.000 let",
        "najdišče": "Nevlje pri Kamniku, kjer naj bi po ljudski legendi nekoč bilo veliko jezero.",
        "zanimivosti": ["Arheologi sklepajo, da je žival za časa življenja zabredla v stoječo vodo, kjer je obtičala v blatu in poginila."]
    }
}


def prijava(request):
    if request.method == 'GET':
        return render(request, 'auth/prijava.html')
    elif request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/')


def registracija(request):
    if request.method == 'GET':
        return render(request, 'auth/registracija.html')
    elif request.method == 'POST':
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
        extedned_user = ExtendedUser.objects.create(rel=user, user_role=1)
        return redirect('/prijava/')


@login_required(login_url='/prijava')
def prva_stran(request):
    return render(request, 'igra/stran_1.html',
                  {'stran': 'Stran 1', 'stran_index': 1, 'next': '/druga_stran',
                   'odgovori': [
                       {'barva': '#b6f2df', 'selected': '#5FBD9F'},
                       {'barva': '#b8f2c5', 'selected': '#59AF6C'},
                       {'barva': '#d7f4ab', 'selected': '#8DB057'},
                       {'barva': '#ffea94', 'selected': '#E1C75C'}
                   ], 'barve': ['#b6f2df', '#b8f2c5', '#d7f4ab', '#ffea94'], "lib": library
                   })


@login_required(login_url='/prijava')
def druga_stran(request):
    return render(request, 'igra/stran_2.html', {'stran': 'Stran 2', 'stran_index': 2, 'next': '/tretja_stran', 'prev': '/prva_stran/',
                                                 'odgovori': [
                                                     {'barva': '#b6f2df', 'selected': '#5FBD9F'},
                                                     {'barva': '#b8f2c5', 'selected': '#59AF6C'},
                                                     {'barva': '#d7f4ab', 'selected': '#8DB057'},
                                                     {'barva': '#ffea94', 'selected': '#E1C75C'}
                                                 ], 'barve': ['#b6f2df', '#b8f2c5', '#d7f4ab', '#ffea94'], "lib": library
                                                 })


@login_required(login_url='/prijava')
def tretja_stran(request):
    return render(request, 'igra/stran_3.html', {'stran': 'Stran 3', 'stran_index': 3, 'prev': '/druga_stran/',
                                                 'odgovori': [
                                                     {'barva': '#b6f2df', 'selected': '#5FBD9F'},
                                                     {'barva': '#b8f2c5', 'selected': '#59AF6C'},
                                                     {'barva': '#d7f4ab', 'selected': '#8DB057'},
                                                     {'barva': '#ffea94', 'selected': '#E1C75C'}
                                                 ], 'barve': ['#b6f2df', '#b8f2c5', '#d7f4ab', '#ffea94'], "lib": library
                                                 })


def get_questions_and_answers(request, level):
    vprasanja = {
        1: {
            "tema": "PRAZGODOVINSKA OBDOBJA",
            "Podrobnosti":
                [
                    {
                        "vprasanje": "Katero zgodovinsko obdobje je trajalo najdlje časa?",
                        "odgovori": ["Novi vek", "Srednji vek", "Stari vek", "Prazgodovina"],
                        "pravilen_odgovor": "Prazgodovina"
                    },
                    {
                        "vprasanje": "Kako imenujemo najstarejše obdobje človeške zgodovine?",
                        "odgovori": ["Kamena doba", "Kovinska doba", "Antika", "Srednji vek"],
                        "pravilen_odgovor": "Kamena doba"
                    },
                    {
                        "vprasanje": "Katera je drugo ime za starejšo kameno dobo?",
                        "odgovori": ["Paleolitik", "Mezolitik", "Neolitik", "Halštat"],
                        "pravilen_odgovor": "Paleolitik"
                    },
                    {
                        "vprasanje": "Katera je drugo ime za mezolitik?",
                        "odgovori": ["Bronasta doba", "Mlajša kamena doba", "Starejša kamena doba", "Srednja kamena doba"],
                        "pravilen_odgovor": "Srednja kamena doba"
                    },
                    {
                        "vprasanje": "Katera je drugo ime za mlajšo kameno dobo?",
                        "odgovori": ["Paleolitik", "Mezolitik", "Neolitik", "Halštat"],
                        "pravilen_odgovor": "Neolitik"
                    }
                ]
        },
        2: {
            "tema": "RAZVOJ ČLOVEKA",
            "Podrobnosti":
                [
                    {
                        "vprasanje": "Katera človeška vrsta je naredila najstarejše glasbilo na svetu?",
                        "odgovori": ["Homo Habilis", "Homo Erectus", "Neandertalec", "Homo Sapiens"],
                        "pravilen_odgovor": "Neandertalec"
                    },
                    {
                        "vprasanje": "Kaj je skupnega neandertalcu in homo sapiensu?",
                        "odgovori": ["Udomačitev psa", "Življenje v začasnih bivališčih", "Izdelava kolesa", "Predelava kovin"],
                        "pravilen_odgovor": "Življenje v začasnih bivališčih"
                    },
                    {
                        "vprasanje": "Kdaj je človek odkril ogenj?",
                        "odgovori": ["V starejši kameni dobi", "V srednji kameni dobi", "V mlajši kameni dobi", "V bronasti dobi"],
                        "pravilen_odgovor": "V starejši kameni dobi"
                    },
                    {
                        "vprasanje": "Katera človekov predhodnik je najstarejši?",
                        "odgovori": ["Neandertalec", "Homo Erectus", "Homo Habilis", "Avstralopitek"],
                        "pravilen_odgovor": "Srednja kamena doba"
                    },

                ]
        },
        3: {
            "tema": "RAZVOJ ČLOVEKA",
            "Podrobnosti":
                [
                    {
                        "vprasanje": "Kdaj se je začela neolitska revolucija?",
                        "odgovori": ["Pred približno 100.000 leti", "Pred približno 20.000 leti", "Pred približno 10.000 leti", "Pred približno 500 leti"],
                        "pravilen_odgovor": "Pred približno 10.000 leti"
                    },
                    {
                        "vprasanje": "Kdaj so se ljudje začeli ukvarjati s poljedelstvom?",
                        "odgovori": ["Ko so se odkrili kovine", "Ko so izumrli mamuti", "Ko se je podnebje otoplilo", "Ko so izumili kolo"],
                        "pravilen_odgovor": "Ko se je podnebje otoplilo"
                    },
                    {
                        "vprasanje": "Kakšno obliko poljedelstva je človek uporabljal v začetku stalne naselitve?",
                        "odgovori": ["Požigalništvo", "Izsuševanje", "Gnojenje s hlevskim gnojem", "Namakalno poljedelstvo"],
                        "pravilen_odgovor": "Požigalništvo"
                    },
                    {
                        "vprasanje": "Kdaj so začele nastajati prve vasi?",
                        "odgovori": ["V času prvih civilizacij", "Ob koncu ledene dobe", "Ob začetku pridobivanja železa", "V času razvoja namakalnega poljedelstva"],
                        "pravilen_odgovor": "Ob koncu ledene dobe"
                    },

                ]
        },
        4: {
            "tema": "KAMENA DOBA",
            "Podrobnosti":
                [
                    {
                        "vprasanje": "V katerem obdobju je bil moški najpogosteje lovec, ženska pa nabiralka sadežev?",
                        "odgovori": ["V kameni dobi", "V bronasti dobi", "V železni dobi", "V starem veku"],
                        "pravilen_odgovor": "V kameni dobi"
                    },
                    {
                        "vprasanje": "V kameni dobi so ljudje živeli v skupi, ki jo imenujemo...",
                        "odgovori": ["Heima", "Himera", "Klapa", "Horda"],
                        "pravilen_odgovor": "Horda"
                    },
                    {
                        "vprasanje": "Kaj je pomenila delitev dela po spolu v kameni dobi?",
                        "odgovori": ["Da so bile ženske nabiralke, moški lovci.", "Da so ženske skrbele za ogenj, moški so bili nabiralci", "Da so moški skrbeli za ogenj, ženske so lovile",
                                     "Da so moški skrbeli za družino, ženske pa za ogenj"],
                        "pravilen_odgovor": "Da so bile ženske nabiralke, moški lovci."
                    },
                    {
                        "vprasanje": "Orodje in orožje kamene dobe niso bili narejeni iz ...",
                        "odgovori": ["Brona", "Lesa", "Kosti", "Kremena"],
                        "pravilen_odgovor": "Brona"
                    },

                ]
        },
        5: {
            "tema": "DOBA KOVIN",
            "Podrobnosti":
                [
                    {
                        "vprasanje": "Z uporabo kovin se je v zgodovini človeštva začelo obdobje, ki ga imenujemo ...",
                        "odgovori": ["Kamena doba", "Doba kovin", "Srednji vek", "Modrena doba"],
                        "pravilen_odgovor": "Doba kovin"
                    },
                    {
                        "vprasanje": "Katero kovino so ljudje odkrili najprej?",
                        "odgovori": ["Železo", "Zlato", "Srebro", "Baker"],
                        "pravilen_odgovor": "Baker"
                    },
                    {
                        "vprasanje": "Območje rodovitnega polmeseca povezuje reke ...",
                        "odgovori": ["Nil, Ind, Tigris", "Tigris, Evfrat, Nil", "Tigris, Rumena reka, Ganges", "Evfrat, Nil, Modra reka"],
                        "pravilen_odgovor": "Tigris, Evfrat, Nil"
                    },
                    {
                        "vprasanje": "Neolitik je čas v katerem so  ...",
                        "odgovori": ["Se pojavile prve obrti", "So ljudje udomačili psa", "So ljudje odkrili ogenj", "So za prehrano lovili mamute"],
                        "pravilen_odgovor": "Se pojavile prve obrti"
                    },
                    {
                        "vprasanje": "Kako imenujemo naselja na vzpetinah iz časa starejše železne dobe?",
                        "odgovori": ["Gradiči", "Gradišča", "Gomile", "Grmade"],
                        "pravilen_odgovor": "Gradišča"
                    },
                    {
                        "vprasanje": "Kje so gradili naselja v času železne dobe?",
                        "odgovori": ["Ob rekah", "Ob vodnih izvirih", "Na križišču pomembnih poti", "Na vzpetinah"],
                        "pravilen_odgovor": "Na vzpetinah"
                    },
                    {
                        "vprasanje": "Zasebna lastnina se pojavi v obdobju ?",
                        "odgovori": ["Kovinske dobe", "Neolitika", "Srednjega veka", "Starega veka"],
                        "pravilen_odgovor": "Kovinske dobe"
                    },
                    {
                        "vprasanje": "Z menjalno trgovino?",
                        "odgovori": ["Menjamo blago za blago", "Blago kupujemo z denarjem", "Si blago izposodimo", "Se dogovorimo za naknadno plačilo"],
                        "pravilen_odgovor": "Menjamo blago za blago"
                    }

                ]
        },
        6: {
            "tema": "SLOVENSKA PRAZGODOVINA",
            "Podrobnosti":
                [
                    {
                        "vprasanje": "Katero je najstarejše kamenodobno najdišče v Sloveniji?",
                        "odgovori": ["Jama Divje babe", "Potočka zijalka", "Betlov spodmol", "Ajdovska jama"],
                        "pravilen_odgovor": "Betlov spodmol"
                    },
                    {
                        "vprasanje": "Katero je najpomembnejše najdišče iz bakrene dobe v Sloveniji?",
                        "odgovori": ["Nevlje pri Kamniku", "Jama Divje babe", "Ljubljansko barje", "Betalov spodmol"],
                        "pravilen_odgovor": "Ljubljansko barje"
                    },
                    {
                        "vprasanje": "Kaj je deblak? ",
                        "odgovori": ["Deblo, ki so ga uporabljali za postavitev hiš na barju", "Čoln izklesan iz drevesnega debla", "Del lesenega mostu iz časa koliščarjev",
                                     "Hrastovo drevo, ki so ga uporabljali za pripravo ognja ob solsticiju"],
                        "pravilen_odgovor": "Čoln izklesan iz drevesnega debla"
                    },
                    {
                        "vprasanje": "Kje v Sloveniji so našli največ deblakov?.",
                        "odgovori": ["V Potočki zijalki", "V Kranju", "V Nevljah", "Na Ljubljanskem barju"],
                        "pravilen_odgovor": "Na Ljubljanskem barju"
                    },
                    {
                        "vprasanje": "Pot, ki je povezovala Sredozemlje in Baltsko morje in je vodila tudi preko današnjega slovenskega ozemlja, se imenuje ...",
                        "odgovori": ["Zlata pot", "Železna cesta", "Solna pot", "Jantarjeva pot"],
                        "pravilen_odgovor": "Jantarjeva pot"
                    },
                    {
                        "vprasanje": "Kako imenujemo železnodobne posode, ki so jih večinoma uporabljali med obredi?",
                        "odgovori": ["Situla", "Kanglica", "Vrč", "Menažka"],
                        "pravilen_odgovor": "Situla"
                    },
                    {
                        "vprasanje": "Situle prikazujejo življenje ...",
                        "odgovori": ["V bakreni dobi", "V železni dobi", "V času neolitske revolucije", "V prvih mestih"],
                        "pravilen_odgovor": "V železni dobi"
                    },
                    {
                        "vprasanje": "Kje je bila najdena najbolj znana situla v Sloveniji?",
                        "odgovori": ["Na Ljubljanskem barju", "V Litiji", "Na Vačah", "V Dolgi vasi"],
                        "pravilen_odgovor": "Na Vačah"
                    }

                ]
        }
    }
    return JsonResponse(vprasanja[level])


def get_libraby(requenst):
    return JsonResponse(library)


@login_required(login_url='/prijava')
def create_new_question(request):
    if request.method == "POST":
        question = Question(question=request.POST["question"],
                            answer_1=request.POST["answer_1"],
                            answer_2=request.POST["answer_2"],
                            answer_3=request.POST["answer_3"],
                            answer_4=request.POST["answer_4"],
                            correct_answer=request.POST["correct_answer"],
                            theme=request.POST["theme"],
                            )
        question.save()
        return HttpResponse(status=200)


def students_questions(request, theme):
    all_questions = Question.objects.filter(theme=theme)
    to_return = {"tema": theme}
    questions = []
    for question in all_questions:
        questions.append({
            "vprasanje": question.question,
            "odgovori": [question.answer_1, question.answer_2, question.answer_3, question.answer_4],
            "pravilen_odgovor": question.correct_answer
        })
    to_return["Podrobnosti"] = questions
    return JsonResponse(to_return)


def odjava(request):
    logout(request)
    return redirect('/prijava/')
