
"""
    Rahasade

    Ruudun alareunassa on robotti, jota pelaaja voi liikuttaa vasemmalle tai oikealle
    Taivaalta sataa rahaa, jota robotin tulee kerätä.
    Jos kolikko pääsee pelin alareunaan, elämät vähenee yhdellä.
    Taivaalta sataa myös hirviöitä, joita robotin tulee väistellä.
    Osuma hirviöön vähentää yhden elämän. 
    Jos elämät loppuvat peli loppuu.
    50 kolikkoa == 1 elämä lisää
    Peli pitää kirjaa parhaasta pistetuloksesta
    Versio2 someday:
    Hirviöitä voi myös ampua kerätyillä kolikoilla, jolloin kolikkosaldo vähenee
    ? Kun hirviöön osuus, siitä sinkoaa kolikoita, joita kerätä

""" 
import pygame
import random

class Kolikkosade:
    def __init__(self):
        pygame.init()
        self.leveys, self.korkeus = 640, 640
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        pygame.display.set_caption("Kolikkosade")
        self.kello = pygame.time.Clock()
        self.fontti = pygame.font.SysFont("Arial", 24)
        ohjefontti = pygame.font.SysFont("Arial", 16)
        self.ohjeteksti = ohjefontti.render("Enter = tauko  F2 = uusi peli  Esc = sulje peli ", True, (255, 0, 0)) 
        self.ohjeen_koko = self.ohjeteksti.get_height() + 10
        self.ennatys = 0
        self.uusi_ennatys = self.ennatys
        
        self.uusi_peli()

    def uusi_peli(self):      
        """Alustaa uuden pelin"""  
        self.luo_kolikot()
        self.luo_hirviot()
        self.luo_robo()
        self.pelaa()

        
    def luo_kolikot(self):
        """Luodaan pelissa nakyvat kolikot"""
        self.kolikot = []        
        self.kolikot_kuva = pygame.image.load("kolikko.png")        
        self.maks_kolikot = 10 # Maksimimäärä näkyviä kolikoita
        self.kolikot_lisays = 0
        self.kolikot_odotusaika = random.randint(1000, 3000) # Satunnainen alkuodotusaika millisekunteina
        self.missasit = False #osuuko robotti kolikkoon
        self.missasit_aika = None #Jos robotti ei osu kolikkoon -> teksti UI UI yhden sekunnin ajan
        
    def luo_hirviot(self):
        """Luodaan pelissa nakyvat hirviot"""        
        self.hirviot = []
        self.hirvio_kuva = pygame.image.load("hirvio.png")
        self.maks_hirviot = 5
        self.hirviot_lisays = 0
        self.hirviot_odotusaika = random.randint(1000, 10000)
        self.osuma = False #osuuko hirvio robottiin
        self.osuma_aika = None
        
    def luo_robo(self):
        """Luodaan robotti"""
        self.robo = pygame.image.load("robo.png")        
        self.roboL, self.roboK = self.robo.get_width(), self.robo.get_height()
        self.x, self.y = 0, self.korkeus - self.roboK 
        self.oikealle = False
        self.vasemmalle = False
        self.tauko = False
        self.pisteet = 0  
        self.elamat = 5
                
        if self.pisteet % 3 == 0 and self.pisteet > 0:
            self.elamat += 1
            
            
    def pelaa(self):
        """Pelataan"""
        while True:
            self.kasittele_tapahtumat()
            if not self.tauko:
                self.paivita_peli()
                self.piirra()


    def kasittele_tapahtumat(self):
        """Maarittaa nappaimet.
        Toteuttaa uusi peli / lopeta peli nappainkomennot"""
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()

            if tapahtuma.type == pygame.KEYDOWN:
                self.kasittele_nappaimet(tapahtuma.key)
                
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()

            if tapahtuma.type == pygame.KEYUP:
                self.kasittele_nappaimet(tapahtuma.key, key_up=True)


    def kasittele_nappaimet(self, key, key_up=False):
        """Toteuttaa tauko/robotin liikkumisen nappainkomennot"""
        if key == pygame.K_LEFT:
            self.vasemmalle = not key_up
        elif key == pygame.K_RIGHT:
            self.oikealle = not key_up
        elif key == pygame.K_RETURN and not key_up: 
            self.tauko = not self.tauko
            self.aseta_tauko_otsikko()
            

    def aseta_tauko_otsikko(self):
        """Ikkunan otsikko muuttuu, jos peli on tauolla / kun peli jatkuu"""
        if self.tauko:
            pygame.display.set_caption("Kolikot tauolla")
        else:
            pygame.display.set_caption("Peli jatkuu")


    def paivita_peli(self):
        """Lisätään kolikot/hirviot listalle uusi kolikko/hirvio, 
        jos näkyvien kolikoiden/hirvjioiden 
        määrä on alle maksimin ja odotusaika on kulunut"""
        aika = pygame.time.get_ticks()
        if len(self.kolikot) < self.maks_kolikot and aika - self.kolikot_lisays > self.kolikot_odotusaika:
            self.lisaa_kolikot()
            self.kolikot_lisays = aika

        if len(self.hirviot) < self.maks_hirviot and aika - self.hirviot_lisays > self.hirviot_odotusaika:
            self.lisaa_hirviot()
            self.hirviot_lisays = aika      
            
        self.tarkista_kolikot()
        self.tarkista_hirviot()
        self.liikuta_roboa()


    def lisaa_kolikot(self):
        """Kolikon alkukoordinaattien arpominen"""
        kx = random.randint(0, self.leveys - self.kolikot_kuva.get_width())
        ky = 0 - self.kolikot_kuva.get_height()
        self.kolikot.append([kx, ky])


    def tarkista_kolikot(self):
        """Tarkistetaan, osuuko robotti kolikkoon (+1 piste) 
        tai saavuttaako kolikko ikkunan alareunan (-1 elama)
        Poistetaan kolikko listalta, jotta listalle luodaan uusi kolikko"""
        for kolikko in self.kolikot[:]:
            if (kolikko[1] + self.kolikot_kuva.get_height() >= self.y and
                    ((kolikko[0] >= self.x and kolikko[0] <= self.x + self.roboL) or
                    (kolikko[0] + self.kolikot_kuva.get_width() >= self.x and kolikko[0] + self.kolikot_kuva.get_width() <= self.x + self.roboL) or
                    (kolikko[0] <= self.x and kolikko[0] + self.kolikot_kuva.get_width() >= self.x + self.roboL))):
                self.pisteet += 1
                self.kolikot.remove(kolikko)
                
                if self.pisteet % 50 == 0:
                    self.elamat += 1

            if kolikko[1] + self.kolikot_kuva.get_height() == self.korkeus: 
                self.elamat -= 1
                self.missasit = True
                self.kolikot.remove(kolikko)
                

    def lisaa_hirviot(self):
        """Hirvioiden alkukoordinaattien arpominen"""
        hx = random.randint(0, self.leveys - self.hirvio_kuva.get_width())
        hy = 0 - self.hirvio_kuva.get_height()
        self.hirviot.append([hx, hy])
        

    def tarkista_hirviot(self):
        """Tarkistetaan, osuuko robotti hirvioon (-1 elama) 
        Poistetaan hirvio listalta, jotta listalle luodaan uusi hirvio"""        
        for hirvio in self.hirviot[:]:
            if hirvio[1] < self.korkeus - self.hirvio_kuva.get_height():  
                if (hirvio[1] + self.hirvio_kuva.get_height() >= self.y and
                    ((hirvio[0] >= self.x and hirvio[0] <= self.x + self.roboL) or
                    (hirvio[0] + self.hirvio_kuva.get_width() >= self.x and hirvio[0] + self.hirvio_kuva.get_width() <= self.x + self.roboL) or
                    (hirvio[0] <= self.x and hirvio[0] + self.hirvio_kuva.get_width() >= self.x + self.roboL))):
                    self.elamat -= 1
                    self.osuma = True 
                    self.hirviot.remove(hirvio)        
            elif hirvio[1] == self.korkeus:
                self.hirviot.remove(hirvio)              
    
    
    def liikuta_roboa(self):
        """Robotin nopeus ja liikkumatila"""
        if self.oikealle:
            self.x += 4
        if self.vasemmalle:
            self.x -= 4
        self.x = max(self.x, 0)
        self.x = min(self.x, self.leveys - self.roboL)
        self.y = max(self.y, 0)
        self.y = min(self.y, self.korkeus - self.roboK)
        
        
    def piirra_sydan(self):
        """Sydankuva eli elamat"""
        RED = (255, 0, 0)
        points = [
            (27, 60+ self.ohjeen_koko), (9, 70 + self.ohjeen_koko), (27, 88 + self.ohjeen_koko),
            (44, 70 + self.ohjeen_koko)
        ]
        pygame.draw.polygon(self.naytto, RED, points)
        pygame.draw.circle(self.naytto, RED, (17, 65 + self.ohjeen_koko), 10)
        pygame.draw.circle(self.naytto, RED, (37, 65 + self.ohjeen_koko), 10)
    

    def piirra(self):
        """Piirretaan asiat ikkunaan
        Jos robotti osuu hirvioon, ikkunassa vilkkuu teksti AU AU randomeissa sijainneissa yhden sekunnin ajan.
        Jos robotti ei saa kolikkoa kiinni, ikkunassa vilkkuu teksti UI UI randomeissa sijainneissa yhden sekunnin ajan"""
        self.naytto.fill((102, 0, 51))
        self.piirra_sydan() 
        
        if not self.peli_loppui():
            for kolikko in self.kolikot:
                self.naytto.blit(self.kolikot_kuva, (kolikko[0], kolikko[1] + 1))
                kolikko[1] += 1
                
            for hirvio in self.hirviot:
                self.naytto.blit(self.hirvio_kuva, (hirvio[0], hirvio[1] + 1))
                hirvio[1] += 2    
                
        
        if self.osuma:
            font = pygame.font.SysFont("Arial", 50)                
            AU = font.render("AU AU", True, (255, 255, 0))         
            
            if self.osuma and self.osuma_aika is None:
                self.osuma_aika = pygame.time.get_ticks()        

            nayta_osuma = 1000   
            if self.osuma_aika is not None and pygame.time.get_ticks() - self.osuma_aika < nayta_osuma:
                random_x = random.randint(0, self.leveys - AU.get_width())
                random_y = random.randint(0, self.korkeus - AU.get_height())
                self.naytto.blit(AU, (random_x, random_y))                
            else:
                self.osuma = False  # Aseta osuma Falseksi, kun aika on kulunut loppuun
                self.osuma_aika = None  # Nollaa aika osuman päätyttyä    
                
                
        if self.missasit:
            fontt = pygame.font.SysFont("Arial", 50)                
            UI = fontt.render("UI UI", True, (255, 128, 0))         
            
            if self.missasit and self.missasit_aika is None:
                self.missasit_aika = pygame.time.get_ticks()        

            nayta_osuma = 1000   
            if self.missasit_aika is not None and pygame.time.get_ticks() - self.missasit_aika < nayta_osuma:
                random_x = random.randint(0, self.leveys - UI.get_width())
                random_y = random.randint(0, self.korkeus - UI.get_height())
                self.naytto.blit(UI, (random_x, random_y))                
            else:
                self.missasit = False  # Aseta osuma Falseksi, kun aika on kulunut loppuun
                self.missasit_aika = None  # Nollaa aika osuman päätyttyä                  
                
        if self.peli_loppui():
            #if self.pisteet <= self.ennatys:
            teksti1 = self.fontti.render("Nyyh, peli loppui!", True, (255, 0, 0))
            self.naytto.blit(teksti1, (self.naytto.get_width() / 2, self.naytto.get_height() / 2))                       
            if self.pisteet > self.ennatys:    
                teksti2 = self.fontti.render("JEEE uusi enkka!!", True, (255, 255, 0))
                self.naytto.blit(teksti2, (self.naytto.get_width() / 2, self.naytto.get_height() / 2 + teksti1.get_height()))
                self.uusi_ennatys = self.pisteet

                
        self.naytto.blit(self.robo, (self.x, self.y))
        
        self.naytto.blit(self.kolikot_kuva, (7, 5 + self.ohjeen_koko))
        
        pisteet = self.fontti.render(f" {self.pisteet} ", True, (255, 255, 0)) 
        self.naytto.blit(pisteet, (50, 11 + self.ohjeen_koko))
        
        elamat = self.fontti.render(f" {self.elamat} ", True, (255, 0, 0)) 
        self.naytto.blit(elamat, (50, 58 + self.ohjeen_koko))
        self.naytto.blit(self.ohjeteksti, (7, 5)) 
        
        enkkafontti = pygame.font.SysFont("Arial", 20) 
        enkka = enkkafontti.render(f"Enkka {self.uusi_ennatys} ", True, (255, 0, 0)) 
        self.naytto.blit(enkka, (7, 69 + 2*self.ohjeen_koko)) 
        
        pygame.display.flip()
        self.kello.tick(60)    
        


    def peli_loppui(self):
        """Seuraa pelaajan elamien maaraa ja lopettaa pelin"""
        if self.elamat == 0:     
            return True


if __name__ == "__main__":
    Kolikkosade()            