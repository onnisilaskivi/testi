from tkinter import *
from PIL import Image, ImageTk
import random

#Määritellään pelin vakioarvoja / asetuksia
PELI_LEVEYS = 700
PELI_KORKEUS = 700
NOPEUS = 100
RUUDUN_KOKO = 50
PITUUS = 2
MATO_VARI = "pink"
PISTEET_TAUSTAVARI = "yellow"
TAUSTA = "#8E3E2D"

class Mato: #Luodaan Mato luokka

    def __init__(self): #Muodostetaan Mato objekti
        self.pituus = PITUUS #Määritellään pituus
        self.koordinaatit = [] #Määritellään koordinaatit lista
        self.mato_ovaalit = [] #Määritellään madon osat lista

        #Luodaan koordinaattilista ja laitetaan mato aloittamaan pelikentän vasemmasta yläkulmasta,
        #eli koordinaateista 0,0.
        for i in range(0, PITUUS):
            self.koordinaatit.append([0, 0])
        #Luodaan madon osat. Madon osat koostuvat "ovaaleista".
        for x, y in self.koordinaatit:
            mato_ovaali = canvas.create_oval(x, y, x + RUUDUN_KOKO, y + RUUDUN_KOKO, fill=MATO_VARI, tag="mato")
            self.mato_ovaalit.append(mato_ovaali)


class Kalja: # Luodaan Kalja luokka

    def __init__(self): #Muodostetaan Kalja objekti

        #Luodaan satunnaiset luvut x ja y koordinaatistoon:
        x = random.randint(0, (PELI_LEVEYS / RUUDUN_KOKO)-1) * RUUDUN_KOKO
        y = random.randint(0, (PELI_KORKEUS / RUUDUN_KOKO)-1) * RUUDUN_KOKO

        self.koordinaatit = [x, y]

        #Avataan kuva
        self.img = Image.open("beer2.png")
        #Muokataan kuvan koko vastaamaan arvoa RUUDUN_KOKO
        resize_img = self.img.resize((RUUDUN_KOKO, RUUDUN_KOKO), Image.ANTIALIAS)
        #Muutetaan kuva Tkinter kirjastolle sopivaksi
        self.new_img = ImageTk.PhotoImage(resize_img)
        #Lisätään kuva pelikentälle satunnaiseen paikkaan
        canvas.create_image(x, y, image=self.new_img, anchor=NW, tag="kalja")


def seuraava_liike(mato, kalja): #Luodaan seuraava_liike funktio mato ja kalja parametreilla.

    x, y = mato.koordinaatit[0] #määritetään madon pään koordinaatit

    #Määritetään madon liike
    if suunta == "ylos":
        y -= RUUDUN_KOKO
    elif suunta == "alas":
        y += RUUDUN_KOKO
    elif suunta == "vasen":
        x -= RUUDUN_KOKO
    elif suunta == "oikea":
        x += RUUDUN_KOKO

    #päivitetään madon pään koordinaatit
    mato.koordinaatit.insert(0, (x, y))

    #Luodaan uusi ovaali madon pääksi
    mato_ovaali = canvas.create_oval(x, y, x + RUUDUN_KOKO, y + RUUDUN_KOKO, fill=MATO_VARI)
    #päivitetään madon ovaali lista
    mato.mato_ovaalit.insert(0, mato_ovaali)

    #Katsotaan, osuuko madon pää kaljaan.
    if x == kalja.koordinaatit[0] and y == kalja.koordinaatit[1]:
        #Tuodaan pisteet
        global pisteet
        #Lisätään pisteisiin yksi
        pisteet += 1
        #Lisätään uudet pisteet pistelaskuriin
        label.config(text="pisteet:{}".format(pisteet))
        #Poistetaan kalja
        canvas.delete("kalja")
        #Lisätään uusi kalja
        kalja = Kalja()

    else:
        #Poistetaan madon viimeinen osa
        del mato.koordinaatit[-1]
        #Päivitetaan pelikenttä
        canvas.delete(mato.mato_ovaalit[-1])
        #Poistetaan mato_ovaalit listasta madon viimeinen osa
        del mato.mato_ovaalit[-1]

    #Jos mato törmää itseensä tai seinään, peli päättyy.
    if tormays(mato):
        game_over()

    else:
        #kutsutaan seuraava_liike funktiota ja sen parametreja NOPEUS ajan (millisekuntteina) jälkeen.
        window.after(NOPEUS, seuraava_liike, mato, kalja)


def vaihda_suunta(uusi_suunta):

    global suunta #lisätään suunta funktioon

    #Määritetään uusi suunta. 180 asteen käännöksiä ei hyväksytä.
    if uusi_suunta == 'vasen':
        if suunta != 'oikea':
            suunta = uusi_suunta
    elif uusi_suunta == 'oikea':
        if suunta != 'vasen':
            suunta = uusi_suunta
    elif uusi_suunta == 'ylos':
        if suunta != 'alas':
            suunta = uusi_suunta
    elif uusi_suunta == 'alas':
        if suunta != 'ylos':
            suunta = uusi_suunta

def tormays(mato): #Lisätään törmäys funktioon parametriksi mato

    x, y = mato.koordinaatit[0] #Tuodaan madonpää funktioon

    #Katsotaan onko madon pää pelikentän sisällä
    if x < 0 or x >= PELI_LEVEYS:
        return True
    elif y < 0 or y >= PELI_KORKEUS:
        return True

    #Katsotaan osuuko madon pää sen omaan vartaloon
    for madon_osa in mato.koordinaatit[1:]:
        if x == madon_osa[0] and y == madon_osa[1]:
            return True

    return False

def game_over():
    #Tyhjennetään pelikenttä, kun törmäys tapahtuu ja peli päättyy.
    canvas.delete(ALL)
    global pisteet
    pisteet = 0
    #Lisätään uudet pisteet pistelaskuriin
    label.config(text="pisteet:{}".format(pisteet))

#Aloita peli napin painallus kutsuu Mato ja Kalja objekteja sekä seuraava_liike funktiota. 
def painallus():
    mato = Mato()
    kalja = Kalja()
    seuraava_liike(mato, kalja) #Kutsutaan seuraava_liike funktiota

#Tehdään aloitusikkuna
window2 =Tk()
#Määritetään aloitusikkunan koko
window2.geometry("500x250")
#Aloitusikkunan otsikko
window2.title("Matopeli")
#Lisätään madon kuva
photo = PhotoImage(file='mato.png')
#Lisätään aloitusikkunan matologo
window2.iconphoto(True, photo)
#Lisätään aloita peli nappi
button = Button(window2,
                text="Aloita peli!",
                command=window2.destroy,
                image=photo,
                compound='bottom')
button.pack()

#Lisätään ohjeet
label = Label(window2, text="Tervetuloa matopeliin! Matoa ohjataan tietokoneen nuolinäppäimillä.\nPaina aloita peli painiketta, kun haluat siirtyä peli-ikkunaan!", font=18)
label.pack()
window2.mainloop()

#Tehdään peli-ikkuna
window = Tk()
#Kohdistetaan näppäimistö ja hiiri peli-ikkunaan
window.focus_force()
#Otsikko Matopeli
window.title("Matopeli")
#Ei anneta ohjelman käyttäjän muokata ikkunan kokoa.
window.resizable(False, False)

pisteet = 0
suunta = 'alas'

#Asetetaan pisteet peli-ikkunaan
label = Label(window, text="pisteet:{}".format(pisteet), bg=PISTEET_TAUSTAVARI, font=('consolas', 40))
label.pack()

#Lisätään pelialusta peli-ikkunaan
canvas = Canvas(window, bg=TAUSTA, height=PELI_KORKEUS, width=PELI_LEVEYS)
canvas.pack()

#Määritetään ohjelman näppäimet, jolla matoa liikutetaan
window.bind('<Left>', lambda event: vaihda_suunta('vasen'))
window.bind('<Right>', lambda event: vaihda_suunta('oikea'))
window.bind('<Up>', lambda event: vaihda_suunta('ylos'))
window.bind('<Down>', lambda event: vaihda_suunta('alas'))

button2 = Button(window,
                text="Aloita peli!",
                command=painallus
                )
button2.pack()

window.mainloop()