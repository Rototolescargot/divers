import sys

city="Vienne"

#renvoie le rang de la station dans la liste
def index(nom_station, table):
    for i in range(len(table)):
        if table[i][0]==nom_station:
            return i
            break
    sys.exit("Verifiez le nom des stations")

#renvoie les lignes dont fait partie la station
def lignes(indice_station, table):
    ligne = []
    k = 2
    while k in range(len(table[indice_station])):
        ligne.append(table[indice_station][k])
        k+=2
    return ligne

#renvoie les lignes communes à 2 stations
def lignes_communes(station1, station2, table):
    i = station1
    j = station2
    k = 2
    ligne = []
    while k in range(len(table[i])):
        l = 2
        while l in range(len(table[j])):
            if table[i][k]==table[j][l]:
                ligne.append([table[i][k], table[i][k-1], table[j][l-1]])
            l+=2
        k+=2
    return ligne

#renvoie toutes les autres stations d'une ligne
def voisins(ligne, index_station, table):
    voisins = []
    for i in range(len(table)):
        if ligne in table[i]:
            voisins.append(i)
    return voisins

#calcul de la distance (en nombre de stations) entre deux lignes sur une ligne
def poids(ligne, station1, station2, table): return abs(table[station1][table[station1].index(ligne)-1]-table[station2][table[station2].index(ligne)-1])

#indique le trajet entre deux stations reliées par une même ligne
def direct(ligne, station1, station2, table, terminus):
    dist = poids(ligne[0], station1, station2, table)
    for u in range(len(terminus)):
        if terminus[u][1]==ligne[0] and 1+(ligne[2]- ligne[1])/abs(ligne[1] - ligne[2])==int(terminus[u][2]):
            direction = terminus[u][0]
            break
    return "prenez la ligne " + ligne[0].decode('utf-8') + " en direction de "+direction.decode('utf-8')+" pour "+str(dist)+" station"+(dist>1)*"s"+" jusqu'à "+table[station2][0].decode('utf-8')

#calcul du trajet le plus court entre deux stations
def dijkstra(station1, station2, table):

    #calcul des distances à la station 1
    d = []
    p = []
    for i in range(len(table)):
        d.append(10000)
    d[index(station1, table)]=0
    while(len(p)<len(table)):
        tab = [[i,d[i]] for i in range(len(table)) if i not in p]
        mini = 10000
        for i in range(len(tab)):
            if tab[i][1]<mini:
                mini = tab[i][1]
                a = tab[i][0]
        p.append(a)
        for i in lignes(a, table):
            for j in voisins(i,a, table):
                d[j]=min(d[j], d[a]+poids(i,a,j,table))

    #calcul des distances à la station 2
    d2 = []
    p2 = []
    for i in range(len(table)):
        d2.append(10000)
    d2[index(station2, table)]=0
    while(len(p2)<len(table)):
        tab = [[i,d2[i]] for i in range(len(table)) if i not in p2]
        mini = 10000
        for i in range(len(tab)):
            if tab[i][1]<mini:
                mini = tab[i][1]
                a = tab[i][0]
        p2.append(a)
        for i in lignes(a, table):
            for j in voisins(i,a, table):
                d2[j]=min(d2[j], d2[a]+poids(i,a,j, table))

    #on ne choisit que les stations qui rapprochent de la station 2
    trajet = []
    for i in p:
        if d[i]+d2[i]<=d[index(station2, table)]:
            trajet.append(i)
            
    trajet.sort(key=lambda i:d[i])
    
    #suppression des détours
    neu_trajet=[]
    neu_trajet.append(trajet[0])
    for i in range(1,len(trajet)-1):
        if len(lignes_communes(trajet[i], trajet[i+1], table))>0 and len(lignes_communes(trajet[i], neu_trajet[len(neu_trajet)-1], table)):
            if min([poids(j[0], trajet[i], trajet[i+1], table) for j in lignes_communes(trajet[i], trajet[i+1], table)])==1 and min([poids(j[0], trajet[i], neu_trajet[len(neu_trajet)-1], table) for j in lignes_communes(trajet[i], neu_trajet[len(neu_trajet)-1], table)])==1:
                neu_trajet.append(trajet[i])
    neu_trajet.append(trajet[len(trajet)-1])
    trajet = neu_trajet
    
    return trajet

def instructions(station1, station2, table, terminus):
    trajet = dijkstra(station1, station2, table)
#    jettra = [table[i][0] for i in trajet]
#    print jettra
    i = 0
    instructions = []
    while i in range(len(trajet)-1): #tant que toutes les stations du trajet n'ont pas été visitées
        j=i+1 
        #on cherche une ligne entre la station i et celle immédiatement après
        ligne = lignes_communes(trajet[i], trajet[j], table)[0]
        #tant qu'on peut avancer sur cette ligne et tant qu'on n'atteint pas la destination
        while ligne[0] in table[trajet[j]] and trajet[j]!=index(station2, table):
            j+=1
        #si la station suivante n'est pas sur la même ligne
        if ligne[0] not in table[trajet[j]]:
            instructions.append([ligne, trajet[i], trajet[j-1]])
            i=j-1
        #si on a atteint le point d'arrivée
        if trajet[j]==index(station2, table) : 
            ligne = lignes_communes(trajet[i], index(station2, table), table)[0]
            instructions.append([ligne, trajet[i], index(station2, table)])
            break
        else :
            i=j
    #reglage parce que le nombre de stations pour la dernière correspondance ne marche pas
    #je ne sais pas pourquoi
    if len(instructions)>1:
       for i in range(1, len(instructions)):
           instructions[i][1]=instructions[i-1][2]
    texte = "Pour aller de " + station1.decode('utf-8') + " à "+ station2.decode('utf-8') +", "
    for l in range(len(instructions)):
        texte+= direct(instructions[l][0],instructions[l][1],instructions[l][2], table, terminus)
        if l<len(instructions)-1:
            texte+=" puis "
    texte+="."
    return texte

def open_file(city):#ouverture des fichiers 
    city =city.lower()
    f = city+".txt" #liste des stations
    file = open(f, 'r') 

    table=[]
    for line in file.readlines():
        line_table = []
        a = line.strip().split("_")
        for i in range(len(a)):
            line_table.append(a[i].encode('utf-8'))
        table.append(line_table)
        
    file.close()
        
    g = "terminus_"+city+".txt" #liste des terminus, utile pour déterminer la direction
    file = open(g, 'r')
    
    terminus=[]
    for line in file.readlines():
        line_table = []
        a = line.strip().split("_")
        for i in range(len(a)):
            line_table.append(a[i].encode('utf-8'))
        terminus.append(line_table)
    
    file.close()
    #réorganisation de la liste de stations + conversion du rang de la station dans la ligne en int
    for i in range(len(table)):
        table[i].reverse()
        j=1
        while j in range(len(table[i])):
            table[i][j]=int(table[i][j])
            j+=2
            
    return table, terminus

def main():
    table, terminus = open_file(city)
    
    a = "départ de : "
    station1 = input(a).encode("utf-8")
    b = "destination : "
    station2 = input(b).encode("utf-8")
    print("")
    
    if station1==station2:
        print ("La station de départ est la même que celle d'arrivée.")
    else:
        print (instructions(station1, station2, table, terminus))
        
if __name__== "__main__":
    main()
