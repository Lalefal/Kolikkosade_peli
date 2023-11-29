
"""

    Rahasade

    Ruudun alareunassa on robotti, jota pelaaja voi liikuttaa vasemmalle tai oikealle
    Taivaalta sataa rahaa, jota robotin tulee kerätä.
    Taivaalta sataa myös hirviöitä, joita robotin tulee väistellä.
    Osuma hirviöön vähentää elämiä. 
    Jos elämät loppuvat tai kolikko pääsee pelin alareunaan, peli loppuu.
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
        
        self.uusi_peli()

    def uusi_peli(self):        
        self.luo_kolikot()
        self.luo_hirviot()
        self.luo_robo()
        self.pelaa()
        
    def luo_kolikot(self):
        self.kolikot = []        
        self.kolikot_kuva = pygame.image.load("kolikko.png")        
        self.maks_kolikot = 10
        self.kolikot_lisays = 0
        self.kolikot_odotusaika = random.randint(1000, 3000) 
        self.missasit = False
        
    def luo_hirviot(self):
        self.hirviot = []
        self.hirvio_kuva = pygame.image.load("hirvio.png")
        self.maks_hirviot = 5
        self.hirviot_lisays = 0
        self.hirviot_odotusaika = random.randint(1000, 10000)
        self.osuma = False
        self.osuma_aika = None
        
    def luo_robo(self):
        self.robo = pygame.image.load("robo.png")        
        self.roboL, self.roboK = self.robo.get_width(), self.robo.get_height()
        self.x = 0
        self.y = self.korkeus - self.roboK 
        self.oikealle = False
        self.vasemmalle = False
        self.tauko = False
        self.pisteet = 0
        self.elamat = 5
            
            
    def pelaa(self):
        while True:
            self.kasittele_tapahtumat()
            if not self.tauko:
                self.paivita_peli()
                self.piirra()


    def kasittele_tapahtumat(self):
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
        if key == pygame.K_LEFT:
            self.vasemmalle = not key_up
        elif key == pygame.K_RIGHT:
            self.oikealle = not key_up
        elif key == pygame.K_RETURN and not key_up: 
            self.tauko = not self.tauko
            self.aseta_tauko_otsikko()
            

    def aseta_tauko_otsikko(self):
        if self.tauko:
            pygame.display.set_caption("Kolikot tauolla")
        else:
            pygame.display.set_caption("Peli jatkuu")


    def paivita_peli(self):
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
        kx = random.randint(0, self.leveys - self.kolikot_kuva.get_width())
        ky = 0 - self.kolikot_kuva.get_height()
        self.kolikot.append([kx, ky])


    def tarkista_kolikot(self):
        for kolikko in self.kolikot[:]:
            if (kolikko[1] + self.kolikot_kuva.get_height() >= self.y and
                    ((kolikko[0] >= self.x and kolikko[0] <= self.x + self.roboL) or
                    (kolikko[0] + self.kolikot_kuva.get_width() >= self.x and kolikko[0] + self.kolikot_kuva.get_width() <= self.x + self.roboL) or
                    (kolikko[0] <= self.x and kolikko[0] + self.kolikot_kuva.get_width() >= self.x + self.roboL))):
                self.pisteet += 1
                self.kolikot.remove(kolikko)

            if kolikko[1] + self.kolikot_kuva.get_height() == self.korkeus: 
                self.missasit = True


    def lisaa_hirviot(self):
        hx = random.randint(0, self.leveys - self.hirvio_kuva.get_width())
        hy = 0 - self.hirvio_kuva.get_height()
        self.hirviot.append([hx, hy])
        

    def tarkista_hirviot(self):
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
        if self.oikealle:
            self.x += 4
        if self.vasemmalle:
            self.x -= 4
        #robotin liikkumatila:
        self.x = max(self.x, 0)
        self.x = min(self.x, self.leveys - self.roboL)
        self.y = max(self.y, 0)
        self.y = min(self.y, self.korkeus - self.roboK)
        
        
    def piirra_sydan(self):
        RED = (255, 0, 0)
        points = [
            (27, 60+ self.ohjeen_koko), (9, 70 + self.ohjeen_koko), (27, 88 + self.ohjeen_koko),
            (44, 70 + self.ohjeen_koko)
        ]
        pygame.draw.polygon(self.naytto, RED, points)
        pygame.draw.circle(self.naytto, RED, (17, 65 + self.ohjeen_koko), 10)
        pygame.draw.circle(self.naytto, RED, (37, 65 + self.ohjeen_koko), 10)
    

    def piirra(self):
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
                
        if self.peli_loppui():
            teksti = self.fontti.render("Nyyh, peli loppui!", True, (255, 0, 0))
            self.naytto.blit(teksti, (self.naytto.get_width() / 2, self.naytto.get_height() / 2))
                
        self.naytto.blit(self.robo, (self.x, self.y))
        
        self.naytto.blit(self.kolikot_kuva, (7, 5 + self.ohjeen_koko))
        teksti = self.fontti.render(f" {self.pisteet} ", True, (255, 255, 0)) 
        self.naytto.blit(teksti, (50, 11 + self.ohjeen_koko))
        teksti = self.fontti.render(f" {self.elamat} ", True, (255, 0, 0)) 
        self.naytto.blit(teksti, (50, 58 + self.ohjeen_koko))
        self.naytto.blit(self.ohjeteksti, (7, 5)) 
        
        pygame.display.flip()
        self.kello.tick(60)    
        

    def peli_loppui(self):
        if self.elamat == 0 or self.missasit == True:     
           return True


if __name__ == "__main__":
    Kolikkosade()            