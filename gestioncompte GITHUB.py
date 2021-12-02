#-------------------------------------------------------------------------------
# Name:        compte et stock de patates
#
# Author:      Jules
#
# Created:     26/11/2021
# Copyright:   (c) jules 2021
#
#version: 8.0
#
#Version pour GitHub
#
#But : commander des patates en fonction d'un compte, d'un lieu, d'une sorte et d'un nombre.
#-------------------------------------------------------------------------------

import mysql.connector




connection = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                passwd = '') #se connecter

cursor = connection.cursor()

cursor.execute("USE comptep") #aller dans la bonne database.



def start(): #fonction qui demandde à l'utilisateur si il a un compte.
    CoIn = input("Connexion (1) ou inscription (2) ?") #demander à l'utilisateur si il souhaite s'incrire ou se connecter.
    if CoIn == "1": #si la personne tape 1 alors elle veut se connecter.
        Mail = input("Votre adresse mail : ") #demander à l'utilisateur son mail
        Mdp = input("Veuillez rentrer votre mot de passe : ") #demander à l'utilisateur son mdp
        cursor.execute('SELECT * FROM compte WHERE mail="'+Mail+'"') #regarder dans la table compte et dans la colonne mail si le mail rentré par l'utilisateur est existant.
        verif = cursor.fetchall() #enregistre ma requête précédente dans une variable
        if verif != 0: #si la valeur renvoyée par ma requête précédente est autre chose que 0 cela veut dire qu'il y a déjà un mail d'enregistré. Alors,
            pas = input("Vous n'avez pas de compte à cette adresse mail. Voulez vous en créer un ? ") #demander à l'utilisateur si il veut un compte.
            if pas == "oui": #si oui alors l'envoyer vers la fonction creation de compte.
                creationcompte(Mail)
                Co = input("Voulez vous commander ? ") #je lui demande après si elle souhaite commander.
                if Co == "oui": #si oui alors je lance la fonction commander.
                    commander0(Mail)
                else: #si non, je lui dis au revoir.
                    print("Pas de soucis. Au revoir.")
            else: #si non, lui dire au revoir.
                print("Pas de soucis, nous espérons vous revoir un jour. Bonne journée.")

        else: #ici la valeur qui est stocké dans verif vaut 0 donc il n'y a pas d'adresse mail enregistré.
            connection1(Mail, Mdp) #je revnvoie la personne vers connexion.
            Co = input("Voulez vous commander ? ") #et lui demande après si elle souhaite commander.
            if Co == "oui": #si oui alors je lance la fonction commander.
                commander0(Mail)
            else: #si non, je lui dis au revoir.
                print("Pas de soucis. Au revoir.")

    elif CoIn == "2": #la peronne demande à s'inscrire
        Mail = input("Votre adresse mail : ") #demander à l'utilisateur son mail
        cursor.execute('SELECT * FROM compte WHERE mail="'+Mail+'"') #regarder dans la table compte et dans la colonne mail si le mail rentré par l'utilisateur est existant.
        verif2 = cursor.fetchall() #enregistre ma requête précédente dans une variable
        if len(verif2) != 0:
            if verif2[0][3] == Mail: #si la valeur renvoyée par ma requête précédente est autre chose que 0 cela veut dire qu'il y a déjà un mail d'enregistré. Alors,
                Mdp = input("Vous avez déjà un compte à cette adresse mail. Votre mot de passe : ")#elle va pouvoir se connecter.
                connection1(Mail, Mdp) #je renvoie la personne vers connexion.
                Co2 = input("Voulez vous commander ?  ")
                if Co2 == "oui":
                    commander0(Mail)
                else:
                    print("Pas de soucis. Merci de votre passage. Au revoir.")



        else:
            creationcompte(Mail) #elle va pouvoir se créer un compte.
            Co3 = input("Voulez vous commander ?  ")
            if Co3 == "oui":
                commander0(Mail)
            else:
                print("Pas de soucis. Merci de votre passage. Au revoir.")

    else: #la personne ne sait pas écrire.
        print("Vous n'avez pas choisi une valeur possible.")





def creationcompte(Mail):
    Nom = input("Quel est votre nom ? ") #demander à l'utilisateur son nom
    Mdp = input("Vous devez choisir votre mot de passe.")

    cursor.execute('SELECT mail FROM compte WHERE mail="'+Mail+'"') #je regarde si l'email est bien enregistré.
    resultat = cursor.fetchall()


    entrerinfo = (Nom, Mdp, Mail) #valeur que l'on souhaite insérer dans la table compte.
    cursor.execute("INSERT INTO compte (nom, mdp, mail) VALUES(%s, %s, %s)", entrerinfo)#rentrer des valeurs dans la table compte
    print("Vous avez été enregistré dans nos boutiques en ligne.")

def commander0(Mail):
    cursor.execute('SELECT idutilisateur FROM compte WHERE mail="'+Mail+'"')
    for (comptep,) in cursor:
        USERID = (comptep)
        print(USERID)


    cursor.execute('SELECT * FROM magasin')
    nomMagasin = cursor.fetchall()
    for i in nomMagasin:
        print(str(i[1]) + "\n")

    magasin = input("Dans quelle magasin voulez vous commander ?")

    cursor.execute('SELECT idmagasin FROM magasin WHERE lieumagasin="'+magasin+'"')
    for (comptep,) in cursor:
        IDmagasin = (comptep)
        print(IDmagasin)
        TIDmagasin = str(IDmagasin)

    cursor.execute('SELECT idmagasin FROM stock WHERE idmagasin="'+TIDmagasin+'"')
    for (comptep,) in cursor:
        IDmagasinSt = (comptep)
        IDmagasinStock = str(IDmagasinSt)


    cursor.execute('SELECT * FROM stock WHERE idmagasin="'+TIDmagasin+'"')
    reste = cursor.fetchall()
    print("Nous avons encore : \n")
    for i in reste:
        if i[1] == 0:
            print("Patate :" + str(i[0]) + " plus en stock.")
        else:
            print("Patate :" + str(i[0]) + " et il en reste " + str(i[1])+ "\n")


    sorte = input("Quelle sorte de patate voulez vous ?") #pr le moment rien d'autre que normandie.
    nombre = input("Combien en voulez vous ?")


    cursor.execute('SELECT * FROM stock WHERE sortepatate = "'+sorte+'" AND nbpatates >= "'+nombre+'" AND idmagasin = "'+IDmagasinStock+'"')
    resultat = cursor.fetchall()



    cursor.execute('SELECT nbpatates FROM stock WHERE sortepatate = "'+sorte+'" ')
    nbreste = cursor.fetchall()


    if resultat == []:
        print("Mince, il n'y a pas assez de stock. Nous sommes limité.")
    else:
        print("Merci pour vos achats.")
        entrercommande = (sorte, nombre, USERID, IDmagasin) #valeur que l'on souhaite insérer dans la table stock
        cursor.execute("INSERT INTO achat (sortepatatecommander, nbpatatecommander, idutilisateur1, idmagasin) VALUES(%s, %s, %s, %s)", entrercommande)#rentrer des valeurs dans la table achat

        liste = []
        # initialisation de liste
        for tupl in nbreste:
            for i in tupl:
                liste.append(i)

        test = float(nombre)
        ok = liste[0] - test #calculer reste des stocks.

        sql = "UPDATE stock SET nbpatates = %s WHERE idmagasin = %s" #remplacer l'ancien reste des stocks par le nouveau.
        value = (ok, IDmagasinStock)
        cursor.execute(sql, value)

def connection1(Mail, Mdp): #gère la connection.
    cursor.execute('SELECT * FROM compte WHERE mail="'+Mail+'"') #je regarde si l'email est bien enregistré.
    resultReq = cursor.fetchall()




    if resultReq[0][2] == Mdp:
        print("Vous êtes bien connecté sous le nom de "+resultReq[0][1])
    else:
        print("Mauvais Mot de Passe.")




cursor = connection.cursor()


def admin(nom1, mdp1): #gère la partie admin pour ajouter des stocks.
    cursor.execute('Select * from compte where nom="'+nom1+'"')
    resultReq = cursor.fetchall()
    if len(resultReq) != 0:
        if resultReq[0][2] == mdp1:
            So = input("Sorte :")
            Nb = input("Nombre :")
            Ma = input("Magasin :")
            sql = "UPDATE stock SET nbpatates = %s WHERE idmagasin = %s"
            value = (Nb, Ma)
            cursor.execute(sql, value)
        else:
            print("Mauvais Mot de Passe.")
    else:
        print("Vous n'êtes pas administrateur.")





start()
