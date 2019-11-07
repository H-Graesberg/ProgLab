

import random
from collections import Counter
import matplotlib.pyplot as plt

# Globale variabler
VALG = ['stein', 'saks', 'papir']


class Spiller:
    '''Superklassen til spillertypene, inneholder det som er felles'''

    navngenerator = 1

    def __init__(self, navn=None):
        """Konstruktør for generell spillertype med navngenerator"""
        if navn is None:
            self.navn = "spillernr. " + str(self.navngenerator)
            Spiller.navngenerator += 1
        else:
            self.navn = navn
        self.poengsum = 0
        self.historie = []
        self.spillertype = 'Ikke angitt'
        self.midlertidig = ''

    def velg_aksjon(self, motstander):
        '''Krever at alle spiller må ha denne metoden'''
        return

    def fix_historie1(self):
        self.midlertidig = self.historie.pop(-1)

    def fix_historie2(self):
        self.historie.append(self.midlertidig)

    def navn_og_spillertype(self):
        """Navn på klassen, gis til grensesnitt"""
        return str(self.get_navn()) + ' (' + str(self.get_spillertype()) + ')'

    def get_spillertype(self):
        """returnerer spillertype til spiller"""
        return self.spillertype

    def get_navn(self):
        """returnerer unikt navn til spillern"""
        return self.navn

    def add_historie_return(self, aksjon):
        '''Legger til aksjon i sin egen historie'''
        self.historie.append(aksjon)

    def get_historie(self):
        '''Returnerer historien'''
        return self.historie

    def add_poengsum(self, poeng):
        '''Holder styr på poeng til spilleren'''
        self.poengsum += poeng

    def motvalg(self, mots_valg):
        '''Hjelpemetode, ikke helt god'''
        if mots_valg == 'stein':
            return 'papir'
        elif mots_valg == 'papir':
            return 'saks'
        else:
            return 'stein'


class Tilfeldig(Spiller):
    """Helt tilfeldig valg av aksjon"""

    def __init__(self, name):
        '''Konstruktør, bruker samme fra super. Setter spillertype.'''
        super().__init__(name)
        self.spillertype = 'Tilfeldig'

    def velg_aksjon(self, motstander):
        '''Helt tilfeldig aksjon, bruker global variabel for valg'''
        valg = VALG[random.randint(0, 2)]
        self.add_historie_return(valg)
        return valg


class Saksemann(Spiller):
    """Prøveklasse for å sjekke funksjonalitet hos andre klasser"""

    def __init__(self, name):
        '''Setter spillertype til Saksemann'''
        super().__init__(name)
        self.spillertype = 'Saksemann'

    def velg_aksjon(self, motstander):
        '''0:stein, 1:saks, 2:papir'''
        valg = VALG[0]
        self.add_historie_return(valg)
        return valg


class Sekvensiell(Spiller):
    '''Velger i sekvens; stein, saks, papir'''

    def __init__(self, name):
        '''Setter spillertype. Har i tillegg sekvensnummer for iterere gjennom lista VALG'''
        super().__init__(name)
        self.sekvensnummer = 0
        self.spillertype = 'Sekvensiell'

    def velg_aksjon(self, motstander):
        '''Iterasjon gjennom lista Valg og nullstilling når sekvensnummer overstiger 2'''
        valg = VALG[self.sekvensnummer]
        if self.sekvensnummer < 2:
            self.sekvensnummer += 1
        else:
            self.sekvensnummer = 0
        self.add_historie_return(valg)
        return valg


class MestVanlig(Spiller):
    '''Gjør mottrekk for hva motspiller har valgt mest'''

    def __init__(self, name):
        '''Setter spillertype til Mest vanlig'''
        super().__init__(name)
        self.spillertype = 'Mest vanlig'

    def velg_aksjon(self, motstander):
        '''Sjekker hva motspiller har valgt mest og spiller mot dette'''
        if len(motstander.historie) == 0:
            valg = self.motvalg(VALG[random.randint(0, 2)])
            self.add_historie_return(valg)
            return valg
        motstanders_valg = Counter(motstander.historie).most_common()
        if len(motstanders_valg) == 1:
            valg = self.motvalg(motstanders_valg[0][0])
            self.add_historie_return(valg)
            return valg
        if (motstanders_valg[0][1] == motstanders_valg[1][1]) \
                and len(motstanders_valg) > 2:
            if motstanders_valg[1][1] == motstanders_valg[2][1]:
                valg = self.motvalg(VALG[random.randint(0, 2)])
                self.add_historie_return(valg)
                return valg
            valg = self.motvalg(motstanders_valg[random.randint(0, 1)][0])
            self.add_historie_return(valg)
            return valg
        self.add_historie_return(self.motvalg(motstanders_valg[0][0]))
        return self.motvalg(motstanders_valg[0][0])

        # Skrive egen metode for å hente ut neste element i liste.. Korter ned
        # koden mye!


class Historiker(Spiller):
    '''Tar inn subsekvens, og ser etter mottrekk til motspillers neste trekk.'''

    def __init__(self, name, husk):
        '''Setter spillertype til historiker og størrelse på subsekvens'''
        super().__init__(name)
        self.husk = husk
        self.spillertype = 'Historiker'

    def velg_aksjon(self, motstander):
        '''Sjekker opp subsekvenser. Først om det finnes, og hvis det er
        fler velge ut mest sannsynlig'''
        sub_check = motstander.historie[-int(self.husk):]
        if self.husk > len(motstander.historie):
            valg = VALG[random.randint(0, 2)]
            self.add_historie_return(valg)
            return valg
        frekvens = [0, 0, 0]

        for i in range(len(motstander.historie) - self.husk - 1, 0, -1):
            if motstander.historie[i:i + int(self.husk)] == sub_check:
                valg = motstander.historie[i + self.husk]
                frekvens[Aksjon(valg).value] += 1
        if max(frekvens) < 1:
            valg = VALG[random.randint(0, 2)]
            self.add_historie_return(valg)
            return valg
        # funnet på stack.. Men fungerer! Forklare hvorfor?
        m = max(frekvens)
        mid = [i for i, j in enumerate(frekvens) if j == m]
        valg = self.motvalg(str(Aksjon(random.choice(mid))))
        # valg = self.motvalg(str(Aksjon(frekvens.index(max(frekvens))))) Fant
        # på stack...
        self.add_historie_return(valg)
        return valg


class Aksjon():
    """Definerer om hvilken aksjon som slår en annen, gjøres ved operator overloading"""

    def __init__(self, val):
        '''Gir trekk en verdi, lettere for sjekk om hva som slår hva'''
        if isinstance(val, str):
            val = {'stein': 0, 'saks': 1, 'papir': 2}[val]
        assert isinstance(val, int) & (val >= 0) & (val < 3)
        self.value = val

    def __eq__(self, other):
        '''Overkjører likhetsoperator'''
        return self.value == other.value

    def __gt__(self, other):
        '''Overkjører større enn operator'''
        return (3 + other.value - self.value) % 3 == 1

    def __str__(self):
        '''Gir tilbake stringverdi istedenfor tall'''
        return {0: 'stein', 1: 'saks', 2: 'papir'}[self.value]

    def get_aksjon(self):
        return self.value


class EnkeltSpill():
    '''Kjører ett enkeltspill, super til mangespill'''

    def __init__(self, spiller1, spiller2):
        '''En variabel hver spiller og en for vinner'''
        self.spiller1 = spiller1
        self.spiller2 = spiller2
        self.runde_vinner = None

    # nødløsning, må være bedre her....Threading?
    def gjennomfoer_spill(self):
        """Spør hver spiller om aksjon og del ut poeng. Rapporter valg og resultat til spillerne"""
        valg1 = self.spiller1.velg_aksjon(self.spiller2)
        self.spiller1.fix_historie1()
        valg2 = self.spiller2.velg_aksjon(self.spiller1)
        self.spiller1.fix_historie2()
        if Aksjon(valg1) == Aksjon(valg2):
            vinner = 'Uavgjort'
            self.spiller1.add_poengsum(0.5)
            self.spiller2.add_poengsum(0.5)
        elif Aksjon(valg1) > Aksjon(valg2):
            vinner = self.spiller1.get_navn()
            self.spiller1.add_poengsum(1)
        else:
            vinner = self.spiller2.get_navn()
            self.spiller2.add_poengsum(1)
        self.runde_vinner = vinner
        return self

    def __str__(self):
        '''Skriver pent til skjerm'''
        return self.spiller1.navn_og_spillertype() + ' valgte ' + str(self.spiller1.get_historie()[-1]) + \
            ".\n" + self.spiller2.navn_og_spillertype() + ' valgte ' + str(self.spiller2.get_historie()[-1]) + \
            ".\n" + 'Vinner: ' + self.runde_vinner


class MangeSpill(EnkeltSpill):  # Også plotte grafisk her
    '''Kjører flere spill etter hverandre og kommer med grafisk fremstilling'''

    def __init__(self, spiller1, spiller2, antall_spill):
        super().__init__(spiller1, spiller2)
        self.antall_spill = antall_spill

    def arranger_enkeltspill(self):
        return super().gjennomfoer_spill()

    def total_vinner(self):
        if self.spiller1.poengsum > self.spiller2.poengsum:
            return self.spiller1.get_navn()
        elif self.spiller1.poengsum < self.spiller2.poengsum:
            return self.spiller2.get_navn()
        else:
            return 'Uavgjort'

    def arranger_turnering(self):
        '''Kjører antall spill etter hverandre'''
        x_aks = []
        poeng_player1 = []
        poeng_player2 = []
        for i in range(1, self.antall_spill + 1):
            self.gjennomfoer_spill()  # print her om live resultater
            x_aks.append(i)
            poeng_player1.append(self.spiller1.poengsum * 100 / i)
            poeng_player2.append(self.spiller2.poengsum * 100 / i)

        plt.title('Stein, saks, papir-fremstilling')
        plt.xlabel('Antall spill')
        plt.ylabel('Seiersprosent: ' + self.spiller1.get_navn() +
                   ' blå og ' + self.spiller2.get_navn() + ' oransje.')
        plt.axis([0, self.antall_spill, 0, 100])
        plt.grid(True)
        plt.plot(x_aks, poeng_player1)
        plt.plot(x_aks, poeng_player2)

        print(
            self.spiller1.navn_og_spillertype() +
            ': ' + str(self.spiller1.poengsum) +
            '\n' + self.spiller2.navn_og_spillertype() +
            ': ' + str(self.spiller2.poengsum) +
            '\nVinner: ' + str(self.total_vinner()))
        plt.show()


def main():
    '''Kjøring av GUI'''

    print('Hvem skal spille?')
    spillertype_1 = str(input('Spiller 1: '))
    navn1 = str(input('Navn: '))
    if spillertype_1 == 'Historiker':
        husk1 = int(input('Husk: '))
        spiller_1 = Historiker(navn1, husk1)
    elif spillertype_1 == 'Mest vanlig':
        spiller_1 = MestVanlig(navn1)
    elif spillertype_1 == 'Sekvensiell':
        spiller_1 = Sekvensiell(navn1)
    else:
        spiller_1 = Tilfeldig(navn1)

    spillertype_2 = str(input('Spiller 2: '))
    navn2 = str(input('Navn: '))
    if spillertype_2 == 'Historiker':
        husk2 = int(input('Husk: '))
        spiller_2 = Historiker(navn2, husk2)
    elif spillertype_2 == 'Mest vanlig':
        spiller_2 = MestVanlig(navn2)
    elif spillertype_2 == 'Sekvensiell':
        spiller_2 = Sekvensiell(navn2)
    else:
        spiller_2 = Tilfeldig(navn2)

    runder = int(input('Hvor mange runder skal spilles? '))

    spill3 = MangeSpill(spiller_1, spiller_2, runder)
    spill3.arranger_turnering()


def alt_main():
    '''Raskere testkjøring'''
    p1 = Tilfeldig(None)
    p2 = Sekvensiell(None)
    p3 = MestVanlig('Luringen')
    p4 = Saksemann('Edward')
    p5 = Historiker('Herman', 2)
    p6 = Historiker('Jan', 3)
    p7 = Historiker('Fredrik', 10)

    # print(p3.velg_aksjon(p4))
    # print(p3.motvalg('stein'))
    # print(p3.motvalg('saks'))
    # print(p3.motvalg('papir'))

    # spill1 = EnkeltSpill(p5, p2)
    # spill2 = EnkeltSpill(p3, p1)
    # print(spill1.gjennomfoer_spill())
    # print(spill2.gjennomfoer_spill())
    spill3 = MangeSpill(p1, p5, 3000)
    spill3.arranger_turnering()


alt_main()
# main()
