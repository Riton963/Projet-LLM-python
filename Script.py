import string
import random


## Compte la fréquence d'apparition de chaque lettre dans un fichier donnée
def compter_lettres(fichier):
    ## Ajoute les caractères @ et # qui represente la fin et le dubut d'un mot
    alphabet = string.ascii_lowercase + "#" + "@"
    compteur_lettres = dict.fromkeys(alphabet, 0)
    total_lettres = 0

    with open(fichier, 'r', encoding='utf-8') as f:
        for ligne in f:
            mots = ligne.strip().lower().split()
            for mot in mots:
                for lettre in mot:
                    if lettre in compteur_lettres:
                        compteur_lettres[lettre] += 1
                        total_lettres += 1


    probabilites = {lettre: (compteur / total_lettres)*100 for lettre, compteur in compteur_lettres.items()}

    return probabilites

## Compte la fréquence d'apparition de chaque lettre avant une autre lettre dans un fichier
def compter_lettres_precedentes(fichier):
    alphabet = string.ascii_lowercase
    compteur_lettres = {lettre: {precedente: 0 for precedente in alphabet} for lettre in alphabet}
    total_lettres = 0

    with open(fichier, 'r', encoding='utf-8') as f:
        for ligne in f:
            mots = ligne.strip().lower().split()
            for mot in mots:
                for i in range(1, len(mot)):
                    lettre = mot[i]
                    precedente = mot[i - 1]

                    if lettre in compteur_lettres and precedente in compteur_lettres[lettre]:
                        compteur_lettres[lettre][precedente] += 1
                        total_lettres += 1

    probabilites = {lettre: {precedente: (compteur / total_lettres)*100 for precedente, compteur in precedentes.items()} for lettre, precedentes in compteur_lettres.items()}

    return probabilites

## Compte la fréquence d'apparition de chaque double lettre precedent une lettre dans un fichier
def compter_double_lettres_precedentes(fichier):
    alphabet = string.ascii_lowercase + "#" + "@"
    compteur_lettres = {lettre: {premiere_precedente + deuxieme_precedente: 0 for premiere_precedente in alphabet for deuxieme_precedente in alphabet} for lettre in alphabet}
    total_lettres = {lettre: 0 for lettre in alphabet}

    with open(fichier, 'r', encoding='utf-8') as f:
        for lettre_globale in alphabet:
            ## réinitialiser le curseur de lecture au début du fichier a chaque itération
            f.seek(0)
            for ligne in f:
                mots = ligne.strip().lower().split()
                for mot in mots:
                    for i in range(1, len(mot)):
                        if mot[i] == lettre_globale:
                            premiere_precedente = mot[i-1]
                            if i >= 2:
                                deuxieme_precedente = mot[i-2]
                            else:
                                deuxieme_precedente = "#"

                            paire_precedentes = deuxieme_precedente + premiere_precedente
                            if paire_precedentes in compteur_lettres[lettre_globale]:
                                compteur_lettres[lettre_globale][paire_precedentes] += 1
                                total_lettres[lettre_globale] += 1

    probabilites = {lettre: {paire_precedentes: (compteur / total_lettres[lettre])*100 if total_lettres[lettre] != 0 else 0 for paire_precedentes, compteur in compteur_lettres[lettre].items()} for lettre in alphabet}
    return probabilites

## Calcul la proba d'une lettre suivante selon les deux lettres precedentes
def calcul_propa_lettre_suivante(double_lettres, fichier):
    probabilites_double_lettres_precedentes = compter_double_lettres_precedentes(fichier)
    lettres_freq = {}
    total_freq = 0.0

    for lettre, double_lettre_stat in probabilites_double_lettres_precedentes.items():
        for doubles_lettres_key, double_lettres_freq_key in double_lettre_stat.items():
            if doubles_lettres_key == double_lettres:
                if '@' not in doubles_lettres_key:
                    lettres_freq[lettre] = double_lettres_freq_key
                    total_freq += double_lettres_freq_key
                else:   
                    lettres_freq[lettre] = 0.0
                
    if total_freq == 0:
        return {lettre: 1 for lettre in lettres_freq}
    else:
        proba = {lettre: (lettre_freq / total_freq)*100 for lettre, lettre_freq in lettres_freq.items()}
        return proba
    
calcul_propa_lettre_suivante('#o', "./liste_francais.txt")
    

def generer_mot_aleatoire(fichier):
    probabilites_lettres = compter_lettres(fichier)

    alphabet = list(probabilites_lettres.keys())
    mot = "#" + random.choices(alphabet, weights=probabilites_lettres.values(), k=1)[0]
    mot_fini = False
    i = 2
    
    while not mot_fini:
        double_lettres_precedentes = mot[i-2] + mot[i-1]

        lettre_suivante_proba = calcul_propa_lettre_suivante(double_lettres_precedentes, fichier)
        lettre_suivante = random.choices(alphabet, weights=lettre_suivante_proba.values(), k=1)[0]
        if lettre_suivante != "@":
            mot += lettre_suivante
            i += 1
        else:
            mot_fini = True

    ## Des caracteres qui se trouvent uniquement en debut ou en fin de mot, donc pas d'inscidence
    mot = mot.replace("#", "").replace("@", "")
    return mot


probabilites_lettres = compter_lettres('./liste_francais.txt')

probabilites_double_lettres_precedentes = compter_double_lettres_precedentes('./liste_francais.txt')

for i in range(25):
    print(generer_mot_aleatoire('./liste_francais.txt'))
