#Augeix Adrien TG8
#le nom du .exe est volontaire

from ursina import *                   


app = Ursina()                         

window.title = 'Paper Mario'               
window.borderless = False               
window.fullscreen = False               
window.exit_button.visible = False      
window.exit_button.enabled = False 
window.fps_counter.enabled = True       



sky=Sky(texture='modeles/sky',scale=40)

class Niveau: #oui, faire cet objet sert à rien mais bon tant pis
    def __init__(self) -> None:
        """
        classe qui contient le niveau (sol, son, collider)
        """
        self.sol=Entity(model='modeles/sol', texture="modeles/sol", position=(0,0,0), scale=0.1)
        self.sonNiveau = Audio('sons/niveau1.mp3', pitch=1, loop=False, autoplay=False,volume = 0.35)
        self.sol.collider = 'mesh'
        #self.sol.collider.show()


class MarioPlayer(Entity): #la classe MarioPlayer renvoit à la classe Entity fournie par Ursina, ce qui rend MarioPlayer comme une entité cube sur laquelle on mettra les collisions etc
    """
    classe qui contient le personnage principal, sa position etc.
    """
    def __init__(self,position=(0,10,0),vitesse=1) -> None:
        super().__init__() #on donne les attributs du init de la classe Entity à notre MarioPlayer
        """
        self.collisionDroiteGauche=Entity(model='cube', color=color.rgba(0,0,0,0) , position=(0,0,2), scale=(0.2,1,0.2),visible=True) #sprite de saut
        self.collisionDevant.collider = "mesh"
        self.collisionDevant.collider.show()
        """
        #self.visible=False #activer cette ligne pour désactiver le rendu des zones de collision
        #self.collider.show()
        self.pied1Compteur=True
        self.pied1son = Audio('pied1', pitch=1, loop=False, autoplay=False,volume = 0.5)
        self.pied2son = Audio('pied2', pitch=1, loop=False, autoplay=False,volume = 0.5)
        self.piedCompteurNumerique=self.pied1son.length*9
        self.animationCurseurSound2d3d= Audio('2d3d', pitch=1, loop=False, autoplay=False)
        self.animationCurseurSound3d2d= Audio('3d2d', pitch=1, loop=False, autoplay=False)
        self.compteurAnimationCurseur=0 #compteur de temps pour désactiver le curseur sur le perso quand il change de vision 
        self.entity = Animation("marcheGauche/marche",fps=16,loop=True,autoplay=False,scale=1) #face 1 du joueur (regarde vers la gauche)
        self.entityDeux = Animation("marcheDroite/marche",fps=16,loop=True,autoplay=False,scale=1,rotation_y=180) #face 2 du joueur (regarde vers la droite)
        self.entitySaute = Entity(model='quad', texture="saute/saute", position=(0,0,0), scale=1,visible=False) #sprite de saut
        self.entitySauteDeux = Entity(model='quad', texture="saute/sauteInverse", position=(0,0,0), scale=1,visible=False,rotation_y=180) #sprite de saut 2
        self.curseurAnimation = Animation("curseur/curseur",fps=25,loop=False,autoplay=True,scale=(1.6,1.3,1),enabled=False) #animation du curseur de souris qui change de mode 3d
        self.curseurAnimationDeux = Animation("curseur/curseur",fps=25,loop=False,autoplay=True,scale=(1.6,1.3,1),enabled=False) #idem mais l'autre côté
        self.saut=False #si saut est sur true, le perso saute
        self.position = Vec3(position) #position du joueur (type vector3 sous forme x,y,z )
        self.rotation_x = 0 #rotation sous forme x,y,z, l'utilisation d'un vector3 était moins pratique pour le peu dont j'allais me servir de cette fonction
        self.rotation_y = 0
        self.rotation_z = 0
        self.regardeDroite=False
        self.tourneVersDroite_y=False #booléens pour verifier si une animation est en cours pour tourner vers la droite
        self.tourneVersGauche_y=False #idem mais vers la gauche
        self.__vitesse=vitesse #vitesse de déplacement du personnage (peut le changer quand on créé le personnage)
        self.__tempsSaut=0
    def updateLocation(self): #le joueur est composé en réalité de plusieurs Entity (Animation est une Entity), on mets donc à jour leur position en fonction de la position de l'objet défini par la classe MarioPlayer
        """
        met à jour la position des éléments du joueur en fonction de la position de la classe
        """
        
        self.curseurAnimation.position=Vec3(self.position.x+0.15,self.position.y-0.075,self.position.z) 
        self.curseurAnimation.rotation=Vec3(self.rotation_x,self.rotation_y,self.rotation_z)
        self.curseurAnimationDeux.position=Vec3(self.position.x+0.05,self.position.y-0.075,self.position.z)
        self.curseurAnimationDeux.rotation=Vec3(self.rotation_x,self.rotation_y+180,self.rotation_z)
        self.entitySaute.position=self.position
        self.entitySauteDeux.position=self.position
        self.entity.position=self.position #mets à jout les attributs de position
        self.entityDeux.position=self.position
        self.entity.rotation=Vec3(self.rotation_x,self.rotation_y,self.rotation_z) #element qu est tourné vers le joueur
        self.entitySaute.rotation=Vec3(self.rotation_x,self.rotation_y,self.rotation_z)
        self.entitySauteDeux.rotation=Vec3(self.rotation_x,self.rotation_y+180,self.rotation_z)
        self.entityDeux.rotation=Vec3(self.rotation_x,self.rotation_y+180,self.rotation_z) #element dos au joueur, qui s'affiche quand le personnage tourne, c'est plus opti que de faire un réel model 3d et plus pratique pour les animations
    def start(self): #lance l'animation des 2 textures à partir d'une seule méthode
        """
        lance l'animation de marche du joueur
        """
        self.entity.start()
        self.entityDeux.start()
    def finish(self): #arrête l'animation des 2 textures à partir d'une seule méthode
        """
        termine l'animation de marche du joueur
        """
        self.entity.finish()
        self.entityDeux.finish()
    def is_playing(self): #retourne true si l'animation est en train de se jouer, on vérifie les 2 par mesure de sécurité
        """
        si l'animation est lue
        """
        return self.entityDeux and self.entity.is_playing
    def nbrVitesse(self): #donne le nombre équivalent à la vitesse car celle-ci est en privé
        """
        retourne la vitesse du joueur
        """
        return self.__vitesse
    def animationSautAffiche(self): #affiche l'animation de saut de mario et cache les autres sprites
        """
        passe sur l'animation de saut
        """
        if self.entity.visible:
            self.entitySaute.visible=True
            self.entitySauteDeux.visible=True
            self.entity.visible=False
            self.entityDeux.visible=False
    def animationSautCache(self): #cache l'animation de saut
        """
        passe sur l'animation de marche
        """
        if not self.entity.visible:
            self.entitySaute.visible=False
            self.entitySauteDeux.visible=False
            self.entity.visible=True
            self.entityDeux.visible=True
    def startCurseur(self): #lance l'animation du curseur
        """
        lance l'animation du curseur quand on change de dimention qui suit mario (attaché à MarioPlayer aussi)
        """
        if camera.mode2d:
            self.animationCurseurSound2d3d.play()
        else:
            self.animationCurseurSound3d2d.play()
        self.curseurAnimation.enabled=True
        self.curseurAnimationDeux.enabled=True
        self.curseurAnimationDeux.start()
        self.curseurAnimation.start()
    def update(self):
        """
        méthode lue à chaque frame par ursina engine (car MarioPlayer a utilisé super().__init__() sur Entity et a récupéré differents attributs/méthodes)
        """
        if held_keys['z']: #si z est pressé
            if not self.rayCollisionProfondeurTete.hit and not self.rayCollisionProfondeurPied.hit and not camera.onTransition:
                if not camera.mode2d:
                    self.position += ( time.dt*self.nbrVitesse()*1.5,0,0)  #on bouge le perso en fonction de sa vitesse et du temps
                    if not self.is_playing(): #si l'animation de marche n'est pas lancée, on la lance
                        self.start()
        if held_keys['s']:
            if not self.rayCollisionProfondeurTete.hit and not self.rayCollisionProfondeurPied.hit and not camera.onTransition:
                if not camera.mode2d:
                    self.position -= ( time.dt*self.nbrVitesse()*1.5,0,0)  #on bouge le perso en fonction de sa vitesse et du temps
                    if not self.is_playing(): #si l'animation de marche n'est pas lancée, on la lance
                        self.start()
        if held_keys['q']:
            if not camera.onTransition:
                if camera.mode2d: #si on est en 2d
                    if self.rotation_y==180: #si quand on avance vers la gauche le perso regarde à droite :
                        self.tourneVersGauche_y=True #on joue l'animation pour se tourner vers la gauche
                    if (not joueur.rayFace2dTete.hit and not joueur.rayFace2dPied.hit):
                        self.position -= (time.dt*self.nbrVitesse(), 0, 0)
                    if not self.is_playing(): #si l'animation de marche n'est pas lancée, on la lance
                        self.start()
                elif not camera.mode2d: #si on est en 3d
                    if not held_keys['d']:
                        if self.rotation_y==270: #si quand on avance vers la gauche le perso regarde à droite :
                            self.tourneVersGauche_y=True #on joue l'animation pour se tourner vers la gauche
                        if not self.rayCollision.hit and not self.feet_ray.hit:
                            self.position += (0, 0, time.dt*self.nbrVitesse())
                        if not self.is_playing(): #si l'animation de marche n'est pas lancée, on la lance
                            self.start()
        elif not held_keys["d"] and not held_keys["z"] and not held_keys["s"]: #si la touche d n'est pas pressée (ce qui veut dire, si on a pas besoin de jouer d'animation)
            self.finish() #on coupe l'animation

        if held_keys['d']: 
            if not camera.onTransition:
                if camera.mode2d: #si on est en 2d
                    if self.rotation_y==0: 
                        self.tourneVersDroite_y=True
                    if (not joueur.rayFace2dTete.hit and not joueur.rayFace2dPied.hit):
                        self.position += (time.dt*self.nbrVitesse(),0, 0)  
                    if not self.is_playing(): #idem
                        self.start()
                elif not camera.mode2d:
                    if not held_keys['q']:
                        if self.rotation_y==90:
                            self.tourneVersDroite_y=True
                        if not self.rayCollision.hit and not self.feet_ray.hit:
                            self.position -= (0,0, time.dt*self.nbrVitesse())  
                        if not self.is_playing(): #idem
                            self.start()
        if self.saut: #si on est en train de sauter
            if self.__tempsSaut<=0.2: #si il n'est pas encore tout en haut de son saut (à propos du temps de saut)
                self.__tempsSaut+=1*time.dt
                self.position += (0,time.dt*self.nbrVitesse()*2, 0)  
            elif self.__tempsSaut<=0.3:
                self.__tempsSaut+=1*time.dt
            else:
                self.saut=False
                self.__tempsSaut=0
        

class Fumee(Entity):
    def __init__(self,position:Vec3) -> None:
        """
        particule de fumée qui suit mario (est une entitée custom)
        """
        super().__init__()
        self.model="cube"
        self.transparence=1
        self.color=color.rgba(186,186,186,self.transparence)#définis la couleur de la particule, on utilise un attribut transparence car on va le diminuer
        self.scale=0.25
        self.position=position
    def update(self):
        """
        méthode lue par ursina à chaque frame, réduit la taille de la fumée, son opacitée et la supprime
        """
        self.transparence*=2
        self.color=color.rgba(186,186,186,self.transparence) #on réduit l'opacité de la particule (en réalité on augmente la valeur alpha, qui définit l'opacité (255 = transparent))
        self.scale-=0.01
        if self.scale<0.001:
            destroy(self)


joueur = MarioPlayer(vitesse=2,position=(0,1,0)) #on fait un objet joueur avec une vitesse de 2 (nombre sans unité)
niveau = Niveau()
camera.orthographic = True #met la caméra en mode "projection orthogonale", google saura mieux expliquer que moi dans un commentaire 
camera.scale=0.15
camera.onTransition = False
camera.mode2d = True
camera.compteur=0

niveau.sonNiveau.play()
texoffset=0

"""
#TESTS DES MÉTHODES :
print("----------------------------") #la console est un peu surchargée par usina, sans ça on voit rien

print(joueur.is_playing())
joueur.start()
print(joueur.is_playing())
joueur.finish()
print(joueur.is_playing())
print(joueur.nbrVitesse)

print("----------------------------")

"""

""" 
 #ces fonctions ne peuvent pas être appelées ici, il faut que le jeu soit en train de tourner, mais ça marche, le jeu les utilise

joueur.animationSautAffiche()
joueur.animationSautCache()
joueur.startCurseur() 
"""






def update(): #fonction update, lue par ursina chaque fois qu'une image est affichée
    """
    fonction lue par ursina à chaque frame, contient tout le programme ou presque
    """


    if joueur.regardeDroite: #on fait différentes coordonées pour les vecteurs de collision
        joueur.direction = Vec3(
            Vec3(0,0,0)
            + Vec3(0,0,0.8) * -1
            ).normalized()  
        
    else:
        joueur.direction = Vec3(
            Vec3(0,0,0)
            + Vec3(0,0,0.8) * 1
            ).normalized() 
    joueur.directionDeux = Vec3(
            Vec3(0.4,0,0) * -(held_keys['s']-held_keys['z'])
            + Vec3(0,0,0)
            ).normalized() 

    
    

    origin = joueur.position + (joueur.up*.5)


    #raycast (vecteurs qui détectent les collisions avec les entités avec un collider [c'est pourquoi l'entité sol contient un collider])
    #on en a plusieurs car ils sont pas disposés aux mêmes endroits, en général un aux pieds, un à la tête et différents pour les modes de jeu (2d et 3d)
    joueur.feet_ray = raycast(joueur.position+Vec3(0,-0.4,0), joueur.direction, ignore=(joueur,joueur.entity,joueur.entityDeux,joueur.entitySaute,joueur.entitySauteDeux,joueur.curseurAnimation,joueur.curseurAnimationDeux), distance=0.25, debug=False)
    joueur.rayCollision = raycast(origin,joueur.direction, ignore=(joueur,joueur.entity,joueur.entityDeux,joueur.entitySaute,joueur.entitySauteDeux,joueur.curseurAnimation,joueur.curseurAnimationDeux), distance=0.25, debug=False)
    joueur.rayCollisionProfondeurTete = raycast(origin,joueur.directionDeux, ignore=(joueur,joueur.entity,joueur.entityDeux,joueur.entitySaute,joueur.entitySauteDeux,joueur.curseurAnimation,joueur.curseurAnimationDeux), distance=0.4, debug=False)
    joueur.rayCollisionProfondeurPied = raycast(joueur.position+Vec3(0,-0.4,0),joueur.directionDeux, ignore=(joueur,joueur.entity,joueur.entityDeux,joueur.entitySaute,joueur.entitySauteDeux,joueur.curseurAnimation,joueur.curseurAnimationDeux), distance=0.4, debug=False)
    if joueur.regardeDroite:
        sensTemp=5
        tempOrientation2=.2
    else:
        sensTemp=-5
        tempOrientation2=.4

    #raycasts pour simuler une gravité
    joueur.rayBas = raycast(joueur.position+Vec3(0,-0.4,0),joueur.down, ignore=(joueur,joueur.entity,joueur.entityDeux,joueur.entitySaute,joueur.entitySauteDeux,joueur.curseurAnimation,joueur.curseurAnimationDeux), distance=0.1, debug=False)
    joueur.rayBas2d = raycast(Vec3(joueur.position.x,joueur.position.y,sensTemp)+(joueur.up*-.5),joueur.forward, ignore=(joueur,joueur.entity,joueur.entityDeux,joueur.entitySaute,joueur.entitySauteDeux,joueur.curseurAnimation,joueur.curseurAnimationDeux), distance=20, debug=False)
    
    #raycast pour le mode 2d, un à la hauteur de la tête, l'autre aux pieds
    joueur.rayFace2dTete = raycast(Vec3(joueur.position.x,joueur.position.y,sensTemp)+(joueur.up*.5)+(joueur.left*tempOrientation2),joueur.forward, ignore=(joueur,joueur.entity,joueur.entityDeux,joueur.entitySaute,joueur.entitySauteDeux,joueur.curseurAnimation,joueur.curseurAnimationDeux), distance=20, debug=False)
    joueur.rayFace2dPied = raycast(Vec3(joueur.position.x,joueur.position.y,sensTemp)+(joueur.up*-.4)+(joueur.left*tempOrientation2),joueur.forward, ignore=(joueur,joueur.entity,joueur.entityDeux,joueur.entitySaute,joueur.entitySauteDeux,joueur.curseurAnimation,joueur.curseurAnimationDeux), distance=20, debug=False)
    
    if (not joueur.rayBas.hit and not joueur.rayBas2d.hit) and not joueur.saut: #faut descendre le joueur si il ne saute pas et ne touche pas déjà le sol
        joueur.position += (0, -time.dt*2, 0)
    if joueur.directionDeux==Vec3(0,0,0): 
        joueur.rayCollisionProfondeurTete.distance=0.001
        joueur.rayCollisionProfondeurPied.distance=0.001
    if joueur.is_playing(): 
        if joueur.rayBas.hit or joueur.rayBas2d.hit:
            if joueur.piedCompteurNumerique<0:
                Fumee(Vec3(joueur.position.x,joueur.position.y-0.4,joueur.position.z))
                joueur.piedCompteurNumerique=joueur.pied1son.length*9
                if joueur.pied1Compteur:
                    joueur.pied1son.play()
                    joueur.pied1Compteur=False
                else:
                    joueur.pied2son.play()
                    joueur.pied1Compteur=False
            else:
                joueur.piedCompteurNumerique-=time.dt

    if joueur.curseurAnimation.enabled: #si le curseur est activé
        if joueur.compteurAnimationCurseur>=joueur.curseurAnimation.duration/2.1: #si l'animation est terminée
            joueur.curseurAnimation.enabled=False
            joueur.curseurAnimationDeux.enabled=False
            joueur.compteurAnimationCurseur=0
        else:
            joueur.compteurAnimationCurseur+=time.dt #sinon, on ajoute au compteur
    if camera.onTransition: #si la caméra est en train de tourner
        if camera.compteur<1: #compteur de temps pour l'animation de la caméra, même principe que pour le curseur au dessus
            camera.compteur+=time.dt
        else:
            if camera.mode2d: #si on est en 2d, on tourne le joueur pour qu'il regarde vers la caméra
                if joueur.rotation_y<180:
                    joueur.rotation_y=0
                else:
                    joueur.rotation_y=180
            if not camera.mode2d: #si on est en 3d on tourne le joueur 
                if joueur.rotation_y<90:
                    joueur.rotation_y=90
                else:
                    joueur.rotation_y=270

            camera.onTransition=False #on indique que la caméra a fini sa transition
            camera.compteur=0

    if not camera.onTransition and camera.mode2d: #on désactive le fait que la caméra suive le joueur si elle fait une animation
        camera.position=Vec3(joueur.position.x,joueur.position.y+1.2,joueur.position.z-20) # la camera suit le personnage principal
        camera.rotation_y=0
    elif not camera.mode2d and not camera.onTransition: #la caméra n'a pas la même position en fonction du mode 3d et 2d
        camera.position=Vec3(joueur.position.x-20,joueur.position.y+1.2,joueur.position.z) # la camera suit le personnage principal
        camera.rotation_y=90

    if joueur.saut: #si le joueur saute on affiche son sprite
        joueur.animationSautAffiche()
    else:
        joueur.animationSautCache()

    joueur.updateLocation() #on met à jour la position des 2 elements 3d qui composent joueur
    if joueur.tourneVersDroite_y: #si le joueur est en train de tourner vers la droite (animation)
        if camera.mode2d:
            if joueur.rotation_y>=180: #si l'animation est finie
                joueur.tourneVersDroite_y=False #on stop l'animation
                joueur.rotation_y=180 #on mets bien sa rotation sur l'axe y sur 180 pour éviter que ce soit un nombre supérieur ou à virgule
            else: 
                joueur.regardeDroite=True
                joueur.rotation_y+=time.dt*500 #on ajoute sur l'axe y une rotation de delta t * 500 (ce qui permet d'avoir une animation par rapport au temps 
                                            #qui s'écoule et non pas par rapport au nombre de fps, nombre qui pourrait varier, le temps lui, ne change pas)
        elif not camera.mode2d:
            if joueur.rotation_y>=270: #si l'animation est finie
                joueur.tourneVersDroite_y=False #on stop l'animation
                joueur.rotation_y=270 #on mets bien sa rotation sur l'axe y sur 180 pour éviter que ce soit un nombre supérieur ou à virgule
            else: 
                joueur.regardeDroite=True
                joueur.rotation_y+=time.dt*500 #on ajoute sur l'axe y une rotation de delta t * 500 (ce qui permet d'avoir une animation par rapport au temps 
                                            #qui s'écoule et non pas par rapport au nombre de fps, nombre qui pourrait varier, le temps lui, ne change pas)
    elif joueur.tourneVersGauche_y: #si on est pas en train de tourner vers la droite et qu'on tourne vers la gauche :
        if camera.mode2d:
            if joueur.rotation_y<=0: #si c'est plus petit que 0 (ce qui veut dire que l'animation est finie)
                joueur.tourneVersGauche_y=False #on stop l'animation
                joueur.rotation_y=0 #on met bien à 0 comme avec le 180 plus haut
                
            else:
                joueur.regardeDroite=False
                joueur.rotation_y-=time.dt*500 #même chose que plus haut
        elif not camera.mode2d:
            if joueur.rotation_y<=90: #si c'est plus petit que 0 (ce qui veut dire que l'animation est finie)
                joueur.tourneVersGauche_y=False #on stop l'animation
                joueur.rotation_y=90 #on met bien à 0 comme avec le 180 plus haut
                
            else:
                joueur.regardeDroite=False
                joueur.rotation_y-=time.dt*500 #même chose que plus haut


    if held_keys['e']:                            
        joueur.position += (0,0,time.dt*joueur.nbrVitesse()) 
    if held_keys['a']:
        joueur.position -= (0,0,time.dt*joueur.nbrVitesse())  
2


def input(key): #si une touche est appuyée (appelé une fois même si la touche est encore appuyée, contrairement à held_key, qui donne true tant que c'est appuyé)
    """
    fonction appelée par ursina quand une touche est appuyée
    """
    if key=="space":
        if joueur.rayBas.hit or joueur.rayBas2d.hit:
            joueur.saut=True

    if key=="l":
        joueur.startCurseur()
        if camera.orthographic: #change le mode de rendu de la caméra, on a ici un rendu totalement en 2d (c'est une projection orthogonale)
            camera.onTransition=True
            camera.animate_position(Vec3(joueur.position.x-20,joueur.position.y+1.2,joueur.position.z),1)
            camera.animate_rotation(Vec3(0,90,0),1)
            camera.mode2d = False
            camera.orthographic = False
            camera.scale=1
        else:
            camera.onTransition=True
            camera.animate_position(Vec3(joueur.position.x,joueur.position.y+1.2,joueur.position.z-20),1)
            camera.animate_rotation(Vec3(0,0,0),1)
            camera.mode2d = True
            camera.orthographic = True
            camera.scale=0.15
        

app.run() #lance l'application