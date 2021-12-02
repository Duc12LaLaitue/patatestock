# patatestock
Gérer un stock de patates via python et mysql.
Taper 1 ou 2 au lancement du programme pour choisir soit ce connecter soit créer un compte.
Vous pouvez commencer par créer la base de données. 

#Voici la BDS.

import mysql.connector as mysql

db = mysql.connect(
    host = input("host ? "),
    user = input("user ? "),
    password = input("password ? ")
)

cursor = db.cursor()
cursor.execute("create database comptep;")
cursor.execute("use comptep;")
cursor.execute("create table compte (idutilisateur float primary key auto_increment not null, nom varchar(250) not null, mdp varchar(250) not null, mail varchar(250));")
cursor.execute("create table achat (idmagasin int not null, idutilisateur1 varchar(250) not null, user_id int not null, nbpatatecommander int not NULL, sortepatatecommander, foreign key (idmagasin) references magasin(idmagasin), foreign key (idutilisateur1) references magasin(idutilisateur));")
cursor.execute("create table magasin (idmagasin int primary key auto_increment not null, lieumagasin varchar(250) not null);")
cursor.execute("create table stock (sortepatate varchar(250) not null,  nbpatates float not NULL, idmagasin int, foreign key (idmagasin) references magasin(idmagasin));")
