from collections import deque

def parcours_largeur(capacite_residuelle, source, destination):
    """
    Renvoie le tableau des prédécesseurs pour le chemin trouvable par BFS.
    """
    n = len(capacite_residuelle)
    visite = [False] * n
    predecesseur = [-1] * n
    file = deque([source])
    visite[source] = True

    while file:
        u = file.popleft()
        for v in range(n):
            if not visite[v] and capacite_residuelle[u][v] > 0:
                predecesseur[v] = u
                visite[v] = True
                file.append(v)
                if v == destination:
                    return predecesseur
    return None

def ford_fulkerson(capacite, source, destination):
    n = len(capacite)
    # Graphe résiduel initial = copie de la capacité
    residuel = [ligne[:] for ligne in capacite]
    flot_total = 0

    chemin = parcours_largeur(residuel, source, destination)
    while chemin:
        # Trouver le flot minimal du chemin
        flot_chemin = float('inf')
        v = destination
        while v != source:
            u = chemin[v]
            flot_chemin = min(flot_chemin, residuel[u][v])
            v = u

        # Mettre à jour les capacités résiduelles
        v = destination
        while v != source:
            u = chemin[v]
            residuel[u][v] -= flot_chemin
            residuel[v][u] += flot_chemin
            v = u

        flot_total += flot_chemin
        chemin = parcours_largeur(residuel, source, destination)

    return flot_total, residuel

