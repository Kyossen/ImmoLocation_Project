# Project_13_ImmoLocation

Le projet ImmoLocation est une application web.
ImmoLocation est une application web de réservation.    Elle permet de reserver patout dans le monde, une chambre d'hôtel, un camping, une maison ou encore un appartement.        
Elle vous permettra d'obtenir les coordonnées de ce bien, mais également ceux du propriétaire en cas de besoin avant location.         
Cette application vous permettra d'effectuer une location de manière sécurisé par PayPal.     
Elle permet également, via le contact du propriétaire, la possibilité de négocier avec ce dernier afin de pouvoir payer en main propre le montant de la location.


## Courte explications des fonctionnalités de base:

### Inscirption/Connexion
-Un utilisateur peux s'inscire et ce connecter à la palteforme

### Mise à disposition d'un bien
-Un utilisateur peux créer une annonce
-Un utilisateur peux gérer sa location (modifier les photos, prix, etc ...)

### Côté reservation
-Un utilisateur peux rechercher une location via le nom d'une ville ou d'un pays
-Un utilisateur peux louer l'annonce de son choix quant il le souhaite, à condition que cette dernière soit disponible au dates préalblement choisi par l'utilisateur


## A savoir:
Ce code est disposé à être mise en ligne.      
Ce code permet à l'application de communiquer avec ses utilisateurs par le bias d'une adresse email de votre choix.

### Installation du code en production
-git clone https://github.com/Kyossen/ImmoLocation_Project.git         
-pip3 install -r requirements.txt        
-Accéder au fichier __init__.py puis effectuer les démarches suivantes:        
  -DEBUG = True -> DEBUG = False        
  -PAYPAL_TEST = True -> PAYPAL_TEST = False        
  -Configurer l'accès à la base de données avec vos identifiants         
  -Configurer l'accès à votre adresse email         

### Lancer le serveur
-sudo python3 manage.py runserver        

## Pré-requis:
-HTML 5        
-CSS 3 / BootStrap       
-JavaScript / Jquery        
-Python 3.x / Django 2.22 (minimum)        
-PosteGreSQL           
