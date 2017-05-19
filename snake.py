import pygame, os
from pygame.locals import *
from random import *
import urllib.request

pygame.init()
#Centre la fenetre
os.environ['SDL_VIDEO_CENTERED'] = '1'
#Création fenetre
fe = pygame.display.set_mode((1000,700))
fe.fill((0, 0, 0))
pygame.display.set_caption("Snake.")
try:
    ico = pygame.image.load('icon.ico')
    pygame.display.set_icon(ico)
except:
    print()
    #Logo de base

pygame.display.update()

#SUPER VARIABLES

version = "1.3"

load = True
wdaction = "menu"
menuact = 0
wcsc = 0
score = 0
screenborders = True
mode = "normal"

bgcolor = (255,255,255)

#Clock speed

clockspeed = 5
tmit = clockspeed

#Taille

lenght = 1
objlenght = 6
dellenght = 0
size = 25

#Coords

x,y=100,100
adir="left"
fadir=""
snakeCoords=[(x,y)]

#Couleur serpent

skin="classic"
skinData = 0
sncr=(231, 76, 60)

#Powerud cache

poweruds = True
powCache = [skin,clockspeed,objlenght]
powAction = "action"

#
# ECRAN DE DEMARRAGE & FONCTIONS UTILITAIRES
#

#Fonc: verifie la version
def checkVersion():
    try:
        #On récup la version sur le serveur
        verfile = urllib.request.urlopen("http://dariusmartin.hol.es/snake/ver.txt")
        if verfile.read().decode('utf-8') == version:
            #A jour
            resetScreen()
            sendAlert("Vous pouvez changer la difficulté dans les options")
        else:
            #Non à jour
            resetScreen()
            sendAlert("Votre version n'est pas à jour ! Allez sur dariusmartin.hol.es/snake",getColorByName("darkred"),getColorByName("white"))
            return 0
    except:
        resetScreen()
        sendAlert("Connexion internet introuvable :(")

#Fonc: Ecran de démarrage
def welcomeScreen(phase):
    if phase == 0:
        fe.fill(getColorByName("darkred"))
    elif phase == 1:
        fe.fill(getColorByName("darkorange"))
    elif phase == 2:
        fe.fill(getColorByName("darkyellow"))
    logo0 = getFont("Ubuntu-B",22).render("projet", 1, getColorByName("white"))
    fe.blit(logo0, (478, 288))
    logo1 = getFont("Ubuntu-BI",50).render("Snake.", 1, getColorByName("red"))
    fe.blit(logo1, (450, 300))
    logo2 = getFont("Ubuntu-BI",50).render("Snake.", 1, getColorByName("orange"))
    fe.blit(logo2, (447, 297))
    logo3 = getFont("Ubuntu-BI",50).render("Snake.", 1, getColorByName("yellow"))
    fe.blit(logo3, (444, 294))
    logo4 = getFont("Ubuntu-B",22).render("Andrea - Damien - Darius", 1, getColorByName("white"))
    fe.blit(logo4, (390, 360))
    if phase == 3:
        resetScreen()
    pygame.display.update()

#Fonc: récupere une police
def getFont(name,size):
    try:
        return pygame.font.Font("fonts/" + name + ".ttf", size)
    except:
        try:
            return pygame.font.Font(name + ".ttf", size)
        except:
            return pygame.font.SysFont("Helvetica",size)

#Fonc: traduit un booléen en string
def transBool(boo):
    if boo == False:
        return "non"
    else:
        return "oui"

#Fonc: converti couleur nom en RGB
def getColorByName(color):
    if color == "darkred":
        return (192, 57, 43)
    elif color == "red":
        return (231, 76, 60)
    elif color == "darkorange":
        return (211, 84, 0)
    elif color == "orange":
        return (230, 126, 34)
    elif color == "darkyellow":
        return (243, 156, 18)
    elif color == "yellow":
        return (241, 196, 15)
    elif color == "darkaqua":
        return (22, 160, 133)
    elif color == "aqua":
        return (26, 188, 156)
    elif color == "darkgreen":
        return (39, 174, 96)
    elif color == "green":
        return (46, 204, 113)
    elif color == "darkblue":
        return (41, 128, 185)
    elif color == "blue":
        return (52, 152, 219)
    elif color == "darkpurple":
        return (142, 68, 173)
    elif color == "purple":
        return (155, 89, 182)
    elif color == "darkmidnight":
        return (44, 62, 80)
    elif color == "midnight":
        return (52, 73, 94)
    elif color == "darkgrey":
        return (127, 140, 141)
    elif color == "grey":
        return (149, 165, 166)
    elif color == "lightgrey":
        return (189, 195, 199)
    elif color == "whitesmoke":
        return (236, 240, 241)
    elif color == "black":
        return (0, 0, 0)
    elif color == "white":
        return (255, 255, 255)

#
# FONCTIONS UTILITAIRES DU JEU ET DESIGN
#

#Fonc: [UI] notification sur le menu
def sendAlert(text,bg=getColorByName("whitesmoke"),fg=getColorByName("black")):
    pygame.draw.rect(fe, bg, (0, 620, 1000, 100))
    pygame.draw.rect(fe, getColorByName("red"), (0, 620, 100, 100))
    exc = getFont("Ubuntu-BI",62).render("!", 1, getColorByName("white"))
    fe.blit(exc, (35, 625))
    text = getFont("Ubuntu-R",22).render(text, 1, fg)
    fe.blit(text, (150, 645))
    

#Fonc: [UI] met à jour l'affichage des options
def reloadOption(hover=""):
    buttons = ["opt_skin_classic","opt_time_classic","opt_size_classic","opt_bord_classic",
               "opt_objl_classic","clg_easy_classic","clg_normal_classic","clg_hard_classic",
               "clg_vhard_classic","retour_classic"]
    for but in buttons:
        if but == hover + "_classic":
            makeButton(hover + "_hovered")
        else:
            makeButton(but)


#Fonc: [UI] Boutons options
def drawOptBut(text, xO, yO, act="classic"):
    if act == "classic":
        pygame.draw.rect(fe, getColorByName("white"), (xO, yO, 250, 25))
        pygame.draw.rect(fe, getColorByName("white"), (xO-10, yO+4, 5, 16))
        text = getFont("Ubuntu-R",20).render(text, 1, getColorByName("midnight"))
        fe.blit(text, (xO, yO))
    else:
        pygame.draw.rect(fe, getColorByName("white"), (xO, yO, 250, 25))
        pygame.draw.rect(fe, getColorByName("darkred"), (xO-10, yO+4, 5, 16))
        text = getFont("Ubuntu-R",20).render(text, 1, getColorByName("darkred"))
        fe.blit(text, (xO, yO))

#Fonc: [UI] Boutons challenge
def drawClgBut(text, xO, yO, act="classic"):
    color = (230, 230, 230)
    if text == " Facile" and (mode == "easy" or act == "hovered"):
        color = getColorByName("purple")
    elif text == "Normal" and (mode == "normal" or act == "hovered"):
        color = getColorByName("blue")
    elif text == "  Hard'" and (mode == "hard" or act == "hovered"):
        color = getColorByName("orange")
    elif text == " Extr'm" and (mode == "vhard" or act == "hovered"):
        color = getColorByName("darkred")
    if act == "classic":
        textcolor = getColorByName("white")
        if color == (230, 230, 230):
            textcolor = getColorByName("black")
        pygame.draw.rect(fe, color, (xO, yO, 150, 80))
        text = getFont("Ubuntu-B",25).render(text, 1, textcolor)
        fe.blit(text, (xO+30, yO+24))
    else:
        color = (color[0]+20,color[1]+20,color[2]+20)
        pygame.draw.rect(fe, color, (xO, yO, 150, 80))
        text = getFont("Ubuntu-B",25).render(text, 1, getColorByName("white"))
        fe.blit(text, (xO+30, yO+24))
        

#Fonc: [UI] boutons
def makeButton(bID):
    global size
    fontm = getFont("Ubuntu-B",16)
    if bID == "jouer_classic":
        pygame.draw.rect(fe, getColorByName("black"), (400, 475, 200, 70))
        pygame.draw.rect(fe, getColorByName("white"), (404, 479, 192, 62))
        text = getFont("Ubuntu-B",29).render("Jouer", 1, getColorByName("black"))
        fe.blit(text, (463, 490))
    elif bID == "jouer_hovered":
        pygame.draw.rect(fe, getColorByName("darkred"), (400, 475, 200, 70))
        pygame.draw.rect(fe, getColorByName("red"), (404, 479, 192, 62))
        text = getFont("Ubuntu-B",29).render("Jouer", 1, getColorByName("white"))
        fe.blit(text, (463, 490))
    if bID == "options_classic":
        pygame.draw.rect(fe, getColorByName("darkgrey"), (450, 560, 100, 30))
        pygame.draw.rect(fe, getColorByName("white"), (453, 563, 94, 24))
        text = fontm.render("Options", 1, getColorByName("darkgrey"))
        fe.blit(text, (468, 564))
    elif bID == "options_hovered":
        pygame.draw.rect(fe, getColorByName("orange"), (450, 560, 100, 30))
        pygame.draw.rect(fe, getColorByName("white"), (453, 563, 94, 24))
        text = fontm.render("Options", 1, getColorByName("orange"))
        fe.blit(text, (468, 564))
    elif bID == "retour_classic":
        pygame.draw.rect(fe, getColorByName("darkred"), (820, 30, 125, 40))
        text = getFont("Ubuntu-R",20).render("Retour", 1, getColorByName("orange"))
        fe.blit(text, (850, 38))
    elif bID == "retour_hovered":
        pygame.draw.rect(fe, getColorByName("orange"), (820, 30, 125, 40))
        text = getFont("Ubuntu-R",20).render("Retour", 1, getColorByName("darkred"))
        fe.blit(text, (850, 38))
    elif bID == "opt_size_classic":
        drawOptBut("Taille : " + str(size),120,190,"classic")
    elif bID == "opt_size_hovered":
        drawOptBut("Taille : " + str(size),120,190,"hovered")
    elif bID == "opt_time_classic":
        drawOptBut("Vitesse : " + str(clockspeed),120,230,"classic")
    elif bID == "opt_time_hovered":
        drawOptBut("Vitesse : " + str(clockspeed),120,230,"hovered")
    elif bID == "opt_skin_classic":
        drawOptBut("Skin : " + skin,120,350,"classic")
    elif bID == "opt_skin_hovered":
        drawOptBut("Skin : " + skin,120,350,"hovered")
    elif bID == "opt_bord_classic":
        drawOptBut("Bordures : " + transBool(screenborders),120,430,"classic")
    elif bID == "opt_bord_hovered":
        drawOptBut("Bordures : " + transBool(screenborders),120,430,"hovered")
    elif bID == "opt_objl_classic":
        drawOptBut("Grossissement : " + str(objlenght),120,470,"classic")
    elif bID == "opt_objl_hovered":
        drawOptBut("Grossissement : " + str(objlenght),120,470,"hovered")
    elif bID == "clg_easy_classic":
        drawClgBut(" Facile",100,550,"classic")
    elif bID == "clg_easy_hovered":
        drawClgBut(" Facile",100,550,"hovered")
    elif bID == "clg_normal_classic":
        drawClgBut("Normal",300,550,"classic")
    elif bID == "clg_normal_hovered":
        drawClgBut("Normal",300,550,"hovered")
    elif bID == "clg_hard_classic":
        drawClgBut("  Hard'",500,550,"classic")
    elif bID == "clg_hard_hovered":
        drawClgBut("  Hard'",500,550,"hovered")
    elif bID == "clg_vhard_classic":
        drawClgBut(" Extr'm",700,550,"classic")
    elif bID == "clg_vhard_hovered":
        drawClgBut(" Extr'm",700,550,"hovered")
    pygame.display.update()

#Fonc: remet à 0 l'affichage
def resetScreen(color=getColorByName("white")):
    bgcolor = color
    fe.fill(color)
    pygame.display.update()
    
#Fonc: place l'objectif aléatoirement
def objectivePlace():
    global x0,y0
    resetScreen()
    x0 = size*randrange(0,int((1000-size)/size))
    y0 = size*randrange(0,int((700-size)/size))
    while verifQueue(x0,y0) == True:
        x0 = size*randrange(0,int((1000-size)/size))
        y0 = size*randrange(0,int((700-size)/size))

#Fonc: faire apparaitre un "carré"
def drawRect(color,x,y,osize=-1):
    global size
    if osize == -1:
        osize = size
    #Les coordonnées correspondent à l'extrémité
    #Haut-Gauche
    pygame.draw.rect(fe, color, (x, y, osize, osize))

def verifChallenges():
    global mode
    wrong = False
    if mode == "easy":
        if size != 50 or clockspeed != 10 or objlenght != 3 or screenborders != False:
            wrong = True
    if mode == "normal":
        if size != 25 or clockspeed != 5 or objlenght != 6 or screenborders != True:
            wrong = True
    if mode == "hard":
        if size != 25 or clockspeed != 3 or objlenght != 12 or screenborders != True:
            wrong = True
    if mode == "vhard":
        if size != 20 or clockspeed != 1 or objlenght != 20 or screenborders != True:
            wrong = True
    if wrong == True:
        mode = ""
        reloadOption()
            

#
# GESTION DU/DES SERPENTS
#

#Fonc: vérifier si les coords sont sur le serpent ou pas (
def verifQueue(x,y):
    global snakeCoords
    #POWER-UP d'invincibilité
    if powAction == "nodeathqueue":
        return False
    #Pour chaque carré de la queue on check si c'est égal
    #aux coords de la tête.
    for xy in snakeCoords:
        if xy[0] == x and xy[1] == y:
            return True
    return False

#Fonc: récupère la couleur en fonction de
#l'ID du carré demandé.
def getSkin(rectID):
    global skin,skinData
    #Liste des skins (colore differemment le serpent)
    if skin == "classic":
        if rectID == 0:
            return getColorByName("darkred")
        else:
            return getColorByName("red")
    elif skin == "rainbow":
        if rectID == 0:
            return getColorByName("black")
        return (randrange(0,256),randrange(0,256),randrange(0,256))
    elif skin == "germany":
        if rectID == 0:
            return getColorByName("black")
        elif rectID <= 0.33*lenght:
            return getColorByName("darkmidnight")
        elif rectID <= 0.66*lenght:
            return getColorByName("red")
        else:
            return getColorByName("yellow")
    elif skin == "france":
        if rectID == 0:
            return getColorByName("darkblue")
        elif rectID <= int(0.33*lenght):
            return getColorByName("blue")
        elif rectID <= int(0.66*lenght):
            return getColorByName("lightgrey")
        else:
            return getColorByName("red")
    elif skin == "blink":
        if skinData == 0:
            return getColorByName("black")
        else:
            return bgcolor 
    elif skin == "rainbow2":
        if rectID == 0:
            return getColorByName("black")
        elif rectID <= int(0.167*lenght):
            return getColorByName("red")
        elif rectID <= int(0.333*lenght):
            return getColorByName("orange")
        elif rectID <= int(0.500*lenght):
            return getColorByName("yellow")
        elif rectID <= int(0.667*lenght):
            return getColorByName("green")
        elif rectID <= int(0.834*lenght):
            return getColorByName("blue")
        else:
            return getColorByName("purple")
    else:
        skin = "classic"
        getSkin(rectID)

#Fonc: Mise à jour du serpent à chaque déplacement
def updateSnake():
    global snakeCoords,x,y,skin,skinData,dellenght
    snakeCoords.reverse()
    #Enlève l'affichage du dernier
    lastxy = snakeCoords[0]
    drawRect((bgcolor),lastxy[0],lastxy[1])
    #On supprime le dernier carré (coords)
    if dellenght == 0:
        del snakeCoords[0]
    else:
        dellenght-=1
    #Ajoute les coordonnés actuels
    snakeCoords.append((x,y))
    #sens normal
    snakeCoords.reverse()
    #Affichage
    rectID=-1
    for xy in snakeCoords:
        rectID+=1
        drawRect(getSkin(rectID),xy[0],xy[1])
    #Data : skin clignotant
    if skin == "blink":
        if skinData == 0:
            skinData = 1
        else:
            skinData = 0

#
# GESTION PARTIE & CONTROLES
#

#Fonc: game over
def sendGameOver():
    global x,y,size,clockspeed,score,snakeCoords,load,lenght,wdaction,menuact,tmit,objlenght
    #AFFICHAGE écran
    menuact = 0
    wdaction = "menu"
    resetScreen((100,0,100))
    updateSnake()
    drawRect(getSkin(0),x,y)
    font = getFont("Ubuntu-BI",72)
    text = font.render("Game Over.", 1, (205, 205, 205))
    fe.blit(text, (294, 296))
    text = font.render("Game Over.", 1, (230, 230, 230))
    fe.blit(text, (297, 298))
    text = font.render("Game Over.", 1, getColorByName("white"))
    fe.blit(text, (300, 300))
    pygame.display.update()
    pygame.time.Clock().tick(0.5)
    #RESET partie
    snakeCoords=[(x,y)]
    score = 0
    objectivePlace()
    lenght = 1
    tmit = clockspeed
    updateCache(True)

#Fonc: POWERUDs cache
def updateCache(reset=False):
    global powCache,powAction,skin,clockspeed,objlenght
    if reset == False:
        powCache = [skin,clockspeed,objlenght]
    else:
        powAction = ""
        if powCache[0] != skin:
            skin = powCache[0]
        if powCache[1] != clockspeed:
            clockspeed = powCache[1]
        if powCache[2] != objlenght:
            objlenght = powCache[2]

#Fonc: Traduction nom de code des POWERUDs
def translatePowerud(name=""):
    global powAction
    #Recup le powerud actuel si non précisé
    if name == "":
        name = powAction
    #Listes nom de code/traduite
    powerudsList = ["nogrow","brake","nodeathqueue","blink","moregrow","speed"]
    translatedPowerudsList = ["Grossissement nul","Ralentissement","Queue invincible","Clignotement","Grossissement doublé","Accélération"]
    if name in powerudsList:
        #Si nom de code est dans la liste on prend l'équivalent
        #dans la liste traduite
        return translatedPowerudsList[powerudsList.index(name)]
    else:
        #Si nom de code inexistant, on affiche celui-ci
        return name

#Fonc: gestion power-up (victoire)
def sendPowerud():
    global powAction,powCache,skin,clockspeed,objlenght
    powerup = False
    #50% de chance d'avoir un powerud
    rd = randrange(0,2)
    if poweruds == True:
        if rd != 1:
            updateCache(True)
            return
    else:
        updateCache(True)
        return
    rd = randrange(0,101)
    #Détermination si c'est malus ou bonus
    if mode == "easy":
        if rd >= 20: #80% bonus
            powerup = True
    elif mode == "normal":
        if rd >= 50: #50% bonus (équilibré)
            powerup = True
    elif mode == "hard":
        if rd >= 65: #35% bonus
            powerup = True
    else:
        if rd >= 80: #20% bonus
            powerup = True
    #Reset POWERUD
    updateCache(True)
    #Mise en cache des données
    updateCache()
    #Détermination de l'effet
    if powerup == True:
        #BONUS :)
        bonus = ["nogrow","brake","nodeathqueue"]
        rd=randrange(0,len(bonus))
        powAction = bonus[rd]
        if powAction == "brake":
            clockspeed += 2
        #DESIGN
        #Fond
        resetScreen((223, 255, 221)) #vert clair
        #Nom POWERUD en bas à droite
        text = getFont("Ubuntu-BI",22).render(translatePowerud() + " !", 1, getColorByName("darkgreen"))
        fe.blit(text, (20, 670))
    else:
        #MALUS :(
        malus = ["blink","moregrow","speed"]
        rd=randrange(0,len(malus))
        powAction = malus[rd]
        #Si mode extr'm et malus speed, on l'enleve
        if mode == "vhard" and powAction == "speed":
            powAction = "blink"
        if powAction == "blink":
            skin = "blink"
        elif powAction == "moregrow":
            objlenght *= 2
        elif powAction == "speed":
            clockspeed -= 1
        #DESIGN
        #Fond
        resetScreen((255, 223, 221)) #rouge clair
        #Nom POWERUD en bas à droite
        text = getFont("Ubuntu-BI",22).render(translatePowerud() + " !", 1, getColorByName("darkred"))
        fe.blit(text, (20, 670))
        

#Fonc: modifie les coordonnés en fonction de l'action
def move(dir):
    global x,y,snak1,fadir
    #On enlève l'actuel
    drawRect(getColorByName("white"),x,y)
    #coords
    if dir == "left": #gauche
        #Modifie les coordonnés, et déplace le carré
        x-=size
    if dir == "right": #droite
        x+=size
    if dir == "top": #top
        y-=size
    if dir == "bottom": #bot
        y+=size
    fadir=""
    verifcoords()

#Fonc: Analyse les coordonnés pour diverses utilités.
def verifcoords():
    global x,y,size,clockspeed,score,snakeCoords,load,lenght,wdaction,menuact,tmit,objlenght,dellenght,powAction
    #BORDS DE LA FENETRE
    bordloose = False
    xtemp,ytemp = x,y
    if x < 0:
        x = 1000-size
    if y < 0:
        y = 700-size
    if x >= 1000:
        x = 0
    if y >= 700:
        y = 0
    if (xtemp != x or ytemp != y) and screenborders == True:
        bordloose = True
    #DEFAITE (Mordu la queue)
    if verifQueue(x,y) == True or bordloose == True:
        sendGameOver()
    #VICTOIRE MANCHE (Objectif)
    if x == x0 and y == y0:
        #Score et objectif
        score+=1
        objectivePlace()
        #VICTOIRE : POWERUD
        sendPowerud()
        if powAction != "nogrow":
            dellenght = objlenght
            lenght+=objlenght
        else:
            powAction = ""
        #Affichage Score
        pygame.display.set_caption("Snake. Score : " + str(score))
    #Maj serpent
    updateSnake()
    

#Prog: Ecran de démarrage
loadScreen = True
screenNb = 91#Screen de démarrage
while loadScreen:
    screenNb -= 1
    if screenNb == 90:
        welcomeScreen(0)
    elif screenNb == 60:
        welcomeScreen(1)
    elif screenNb == 30:
        welcomeScreen(2)
    elif screenNb == 0:
        welcomeScreen(3)
        loadScreen = False
    pygame.time.Clock().tick(50)

while load:
    #BEFORE START SNAKE
    if wdaction == "snakestart":
        pygame.time.Clock().tick(100)
        if menuact == 2:
            updateCache()
            resetScreen()
            menuact = 0
            x = size*randrange(0,int((1000)/size))
            y = size*randrange(0,int((700-size)/size))
            snakeCoords=[(x,y)]
            #Objectif
            snak2 = pygame.draw.rect(fe, getColorByName("darkyellow"), (x0, y0, size, size))
            drawRect(getSkin(0),x,y)
            #Text
            text = getFont("Ubuntu-B",22).render("Utilisez ZQSD ou les flèches pour vous déplacer.", 1, getColorByName("black"))
            fe.blit(text, (250, 400))
            pygame.display.update()
            tmit = 1
            #Display update
        #Events
        for event in pygame.event.get():
            #Type clavier
            if event.type == QUIT:
                load = False
            if event.type == KEYDOWN:
                if fadir == "":
                    fadir = adir
                #Flèches
                if event.key == K_LEFT or event.key == K_a:
                    adir="left"
                    wdaction = "snake"
                    menuact = 2
                elif event.key == K_RIGHT or event.key == K_d:
                    adir="right"
                    wdaction = "snake"
                    menuact = 2
                elif event.key == K_UP or event.key == K_w:
                    adir="top"
                    wdaction = "snake"
                    menuact = 2
                elif event.key == K_DOWN or event.key == K_s:
                    adir="bottom"
                    wdaction = "snake"
                    menuact = 2
    #JEU SNAKE
    if wdaction == "snake":
        if menuact == 2:
            menuact = 0
            resetScreen()
        #Gestion du temps (où 20 ticks = 1 avancement)
        pygame.time.Clock().tick(100) #120 FPS
        if tmit == 0:
            #On avance la tête
            move(adir)
            tmit = clockspeed
            #On remet le curseur de base
            #en cas de cause extérieure
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
        tmit -= 1
        #Objectif
        snak2 = pygame.draw.rect(fe, getColorByName("darkyellow"), (x0, y0, size, size))
        #Display update
        pygame.display.update()
        #Events
        for event in pygame.event.get():
            #Type clavier
            if event.type == QUIT:
                load = False
            if event.type == KEYDOWN:
                if fadir == "":
                    fadir = adir
                #Flèches
                if (event.key == K_LEFT or event.key == K_a) and (fadir != "right" or lenght == 1):
                    adir="left"
                elif (event.key == K_RIGHT or event.key == K_d) and (fadir != "left" or lenght == 1):
                    adir="right"
                elif (event.key == K_UP or event.key == K_w) and (fadir != "bottom" or lenght == 1):
                    adir="top"
                elif (event.key == K_DOWN or event.key == K_s) and (fadir != "top" or lenght == 1):
                    adir="bottom"
                elif event.key == K_ESCAPE:
                    sendGameOver()
    #MENU OPTIONS
    elif wdaction == "options":
        pygame.time.Clock().tick(15)
        if menuact == 0:
            resetScreen()
            #DESIGN PAGE
            #header
            pygame.draw.rect(fe, getColorByName("darkred"), (0, 0, 1000, 100))
            text = getFont("Ubuntu-B",50).render("Options", 1, getColorByName("white"))
            fe.blit(text, (100, 18))
            #taille et vitesse
            text = getFont("Ubuntu-B",22).render("GENERAL", 1, getColorByName("black"))
            fe.blit(text, (100, 150))
            #Skin
            text = getFont("Ubuntu-B",22).render("SKIN", 1, getColorByName("black"))
            fe.blit(text, (100, 270))
            #Règles
            text = getFont("Ubuntu-B",22).render("RÈGLES", 1, getColorByName("black"))
            fe.blit(text, (100, 390))
            #Challenges
            text = getFont("Ubuntu-B",22).render("CHALLENGES", 1, getColorByName("black"))
            fe.blit(text, (100, 510))
            #Boutons
            reloadOption()
            menuact = 1
        #MAJ SKIN (PREVUE)
        i=0
        x,y,lenght = 100,310,16
        for i in range(0,16):
            drawRect(getSkin(i),x,y,25)
            x+=25
            i+=1
        x,y,lenght = 0,0,1
        pygame.display.update()
        #EVENTS
        for event in pygame.event.get():
            #Type Souris
            if event.type == pygame.MOUSEMOTION:
                mousecoords = pygame.mouse.get_pos()
                #Hover boutons
                #RETOUR
                if (mousecoords[0] >= 820 and mousecoords[0] <= 945) and (mousecoords[1] >= 30 and mousecoords[1] <= 70):
                    reloadOption("retour")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #OPT: taille
                elif (mousecoords[0] >= 120 and mousecoords[0] <= 220) and (mousecoords[1] >= 190 and mousecoords[1] <= 210):
                    reloadOption("opt_size")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #OPT: temps
                elif (mousecoords[0] >= 120 and mousecoords[0] <= 320) and (mousecoords[1] >= 230 and mousecoords[1] <= 250):
                    reloadOption("opt_time")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #OPT: skin
                elif (mousecoords[0] >= 120 and mousecoords[0] <= 320) and (mousecoords[1] >= 350 and mousecoords[1] <= 370):
                    reloadOption("opt_skin")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #OPT: bordures
                elif (mousecoords[0] >= 120 and mousecoords[0] <= 320) and (mousecoords[1] >= 430 and mousecoords[1] <= 450):
                    reloadOption("opt_bord")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #OPT: grossissement
                elif (mousecoords[0] >= 120 and mousecoords[0] <= 320) and (mousecoords[1] >= 470 and mousecoords[1] <= 490):
                    reloadOption("opt_objl")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #CLG: Facile
                elif (mousecoords[0] >= 100 and mousecoords[0] <= 250) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    reloadOption("clg_easy")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #CLG: Normal
                elif (mousecoords[0] >= 300 and mousecoords[0] <= 450) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    reloadOption("clg_normal")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #CLG: Dur
                elif (mousecoords[0] >= 500 and mousecoords[0] <= 650) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    reloadOption("clg_hard")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #CLG: Extreme
                elif (mousecoords[0] >= 700 and mousecoords[0] <= 850) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    reloadOption("clg_vhard")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                else:
                    reloadOption()
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
            #Click souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                #RETOUR
                if (mousecoords[0] >= 820 and mousecoords[0] <= 945) and (mousecoords[1] >= 30 and mousecoords[1] <= 70):
                    resetScreen()
                    menuact = 0
                    wdaction = "menu"
                #TAILLE
                elif (mousecoords[0] >= 120 and mousecoords[0] <= 220) and (mousecoords[1] >= 190 and mousecoords[1] <= 210):
                    sizes = [5,10,20,25,40,50,100]
                    siID = sizes.index(size)
                    siID += 1
                    if siID == len(sizes):
                        siID = 0
                    size = sizes[siID]
                    reloadOption("opt_size")
                #BORDURES
                elif (mousecoords[0] >= 120 and mousecoords[0] <= 320) and (mousecoords[1] >= 430 and mousecoords[1] <= 450):
                    if screenborders == False:
                        screenborders = True
                    else:
                        screenborders = False
                    reloadOption("opt_bord")
                #VITESSE
                elif (mousecoords[0] >= 120 and mousecoords[0] <= 320) and (mousecoords[1] >= 230 and mousecoords[1] <= 250):
                    speeds = [1,2,3,4,5,6,7,8,9,10]
                    spID = speeds.index(clockspeed)
                    spID += 1
                    if spID == len(speeds):
                        spID = 0
                    clockspeed = speeds[spID]
                    reloadOption("opt_time")
                #GROSSISSEMENT
                elif (mousecoords[0] >= 120 and mousecoords[0] <= 320) and (mousecoords[1] >= 470 and mousecoords[1] <= 490):
                    grosst = [0,1,2,3,4,5,6,8,10,15,20]
                    grID = grosst.index(objlenght)
                    grID += 1
                    if grID == len(grosst):
                        grID = 0
                    objlenght = grosst[grID]
                    reloadOption("opt_objl")
                #SKIN
                elif (mousecoords[0] >= 120 and mousecoords[0] <= 320) and (mousecoords[1] >= 350 and mousecoords[1] <= 370):
                    if skin == "classic":
                        skin = "france"
                    elif skin == "france":
                        skin = "germany"
                    elif skin == "germany":
                        skin = "rainbow2"
                    elif skin == "rainbow2":
                        skin = "rainbow"
                    else:
                        skin = "classic"
                    reloadOption("opt_skin")
                #CLG: Facile
                elif (mousecoords[0] >= 100 and mousecoords[0] <= 250) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    mode = "easy"
                    size = 50
                    clockspeed = 10
                    screenborders = False
                    objlenght = 3
                    reloadOption("clg_easy")
                #CLG: Moyen
                elif (mousecoords[0] >= 300 and mousecoords[0] <= 450) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    mode = "normal"
                    size = 25
                    clockspeed = 5
                    screenborders = True
                    objlenght = 6
                    reloadOption("clg_normal")
                #CLG: Dur
                elif (mousecoords[0] >= 500 and mousecoords[0] <= 650) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    mode = "hard"
                    size = 25
                    clockspeed = 3
                    screenborders = True
                    objlenght = 12
                    reloadOption("clg_hard")
                #CLG: Extreme
                elif (mousecoords[0] >= 700 and mousecoords[0] <= 850) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    mode = "vhard"
                    size = 20
                    clockspeed = 1
                    screenborders = True
                    objlenght = 20
                    reloadOption("clg_vhard")
                #Maj challenge
                verifChallenges()
            #Type Croix
            if event.type == QUIT: 
                load = False
    #MENU D'ACCUEIL
    elif wdaction == "menu":
        pygame.time.Clock().tick(15)
        #Mosaique
        headNbRect = 0
        for headNbRect in range(0,40):
            if headNbRect < 20:
                color = (randrange(150,210),randrange(150,210),randrange(150,210))
            else:
                color = getColorByName("white")
            xH = size*randrange(0,int((1000)/size))
            yH = size*randrange(0,int((700-size)/size))
            while yH > 430:
                yH = size*randrange(0,int((700-size)/size))
            drawRect(color,xH,yH)
        #Logo
        font = getFont("Ubuntu-BI",50)
        logo0 = getFont("Ubuntu-B",22).render("projet", 1, getColorByName("black"))
        fe.blit(logo0, (454, 288))   
        logo1 = font.render("Snake.", 1, getColorByName("red"))
        fe.blit(logo1, (425, 300))
        logo2 = font.render("Snake.", 1, getColorByName("orange"))
        fe.blit(logo2, (422, 297))
        logo3 = font.render("Snake.", 1, getColorByName("yellow"))
        fe.blit(logo3, (419, 294))
        pygame.display.update()
        if menuact == 0:
            #Mise en place du menu
            resetScreen()
            exc = getFont("Ubuntu-BI",32).render("Chargement...", 1, getColorByName("midnight"))
            fe.blit(exc, (20, 325))
            pygame.display.update()
            #Check version
            checkVersion()
            #Boutons
            #Jouer
            makeButton("jouer_classic")
            makeButton("options_classic")
            menuact = 1
        for event in pygame.event.get():
            #Type Souris
            if event.type == pygame.MOUSEMOTION:
                mousecoords = pygame.mouse.get_pos()
                #Hover boutons
                #JOUER
                if (mousecoords[0] >= 400 and mousecoords[0] <= 600) and (mousecoords[1] >= 475 and mousecoords[1] <= 545):
                    makeButton("jouer_hovered")
                    makeButton("options_classic")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #OPTIONS
                elif (mousecoords[0] >= 450 and mousecoords[0] <= 550) and (mousecoords[1] >= 560 and mousecoords[1] <= 590):
                    makeButton("options_hovered")
                    makeButton("jouer_classic")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                else:
                    makeButton("options_classic")
                    makeButton("jouer_classic")
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
            #Type clic souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                #LANCEMENT DU SNAKE
                if (mousecoords[0] >= 400 and mousecoords[0] <= 600) and (mousecoords[1] >= 475 and mousecoords[1] <= 545):
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    objectivePlace()
                    menuact = 2
                    wdaction = "snakestart"
                elif (mousecoords[0] >= 450 and mousecoords[0] <= 550) and (mousecoords[1] >= 562 and mousecoords[1] <= 592):
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    wdaction = "options"
                    menuact = 0

            #Type Croix
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    objectivePlace()
                    menuact = 2
                    wdaction = "snakestart"
            if event.type == QUIT:
                print("Au revoir :'(")
                load = False
        
                


pygame.quit()
