import sqlite3 as s3
import os
os.chdir('C:\\cpge')

#1/
def executeRequete(r):
    con=s3.connect("Entreprise.sqlite")
    cur=con.cursor()
    cur.execute(r)
    L=cur.fetchall()  #L est une liste de tuples
    con.commit()
    con.close()
    return L
    
#2
def insererEnfant(num,nom,age,sc,emp):
    con=s3.connect("Entreprise.sqlite")
    cur=con.cursor()
    
    #Tester si le numero numf existe deja
    req="select numf from enfant where numf=?"
    cur.execute(req,[num])
    if cur.fetchone()!=None:   #cur.fetchone() retourne un tuple
        valeur_retour = False
    else:
        #Tester si le le nume existe dans la table employe
        req="select nume from employe where nume=?"  
        cur.execute(req,[emp])
        if cur.fetchone()==None:
             valeur_retour  = False
        else:
            req="insert into enfant values(?,?,?,?,?)"
            cur.execute(req,[num,nom,age,sc,emp])
            con.commit()
            valeur_retour  = True
            
    con.close()
    return valeur_retour

#3
def NombreEnfant(num):
    con=s3.connect("Entreprise.sqlite")
    cur=con.cursor()
    req="select count(nume) from enfant where nume=?"
    cur.execute(req,[num])
    t=cur.fetchone()   #t est un tuple      
    con.close()
    return t[0]

#4
def ListeEnfant():
    return executeRequete("select numf, nomf, age,employe.nume, nome from enfant,employe where enfant.nume=employe.nume order by employe.nume asc,age desc")
    
def liste():
    L=ListeEnfant()
    for l in L:
        print(l)
    

#5
def copierFichier(fich):
    #récupérer la liste des enfants
    L=ListeEnfant()   
    
    #ouverture du fichier en création
    f=open(fich,"w")
    
    #parcourir la liste L et ecrire dans le ficher f
    for l in L:
        f.write(str(l[0])+","+l[1]+","+str(l[2])+","+str(l[3])+","+l[4]+"\n")
    
    #fermer le fichier
    f.close()
    
#6
def AfficherFichier(fich):
    #ouverture du fichier en lecture
    f=open(fich,"r")
    
    #parcourir le fichier et afficher ligne par ligne
    for ligne in f:
        print(ligne,end='')
        #print(ligne.rstrip())

    
    #fermer le fichier
    f.close()
    
#7
def copierFichiers():
    #récupérer la liste des enfants
    L=ListeEnfant()   
    for l in L:
        fich=l[4]+"_"+str(l[3])+".txt"
        f=open(fich,"a")
        f.write(str(l[0])+","+l[1]+","+str(l[2])+"\n")
        #fermer le fichier
        f.close()



def copierFichiers2():
    #récupérer la liste des enfants
    L=ListeEnfant()   
    n=len(L)
    i=0
    while i<n-1:
        l=L[i]
        fich=l[4]+'_'+str(l[3])
        f=open(fich+".txt","w")
        f.write(str(l[0])+","+l[1]+","+str(l[2])+"\n")
        xnume=l[3]
        i+=1
        l=L[i]
        while xnume==l[3]and i<n-1 :
            f.write(str(l[0])+","+l[1]+","+str(l[2])+"\n")
            i+=1
            l=L[i]
        f.close()
    
    
    #traitement pour le dernier tuple
    if xnume==l[3]:
        f=open(fich+".txt","a")
    else:
        fich=l[4]+'_'+str(l[3])
        f=open(fich+".txt","w")
    
    f.write(str(l[0])+","+l[1]+","+str(l[2])+"\n")
    f.close()
    
#8
def afficheFichiers():
    #extraire la liste (nome,nume) des employés qui ont des enfants
    L=executeRequete("select nome,nume from employe where nume in (select nume from enfant)")
    
    #construire la liste des noms des fichiers correspondants aux employés ayant des enfants
    LF=[]
    for l in L:
        LF.append(l[0]+'_'+str(l[1])+'.txt')
        
    
    #parcourir les fichiers de la liste LF et afficher les enfants de chaque employé
    i=0
    for fich in LF:
        print("Nom Employé",i+1,':',L[i][0] )
        print("\tN°Enf\tNom\t\t\tAge")
        f=open(fich,'r')
        for ligne in f:
            ligne=ligne.rstrip()
            ligne=ligne.split(',')  #convertir une chaine en liste
            print("\t%s\t\t%s\t\t%s" % (ligne[0],ligne[1],ligne[2]))
        f.close()
        print()
        i+=1
    