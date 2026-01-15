import networkx as nx
from datetime import datetime
from database.dao2 import DAO



class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.refuges = None # dizionario con tutti i nodi che rispettano l'anno massimo
        self.connessioni = []
        self.dict_connessioni = None # dizionario con tutte le connessioni


    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        # TODO

        # prendo i rifugi coinvolti
        self.refuges = DAO.get_all_rifugi(year)

        # prendo le connessioni
        self.connessioni = DAO.get_connessioni(year)

        # riempio il dizionario (l'ho fatto io per capire)
        for connessione in self.connessioni:
            id_rifugio1 = connessione.id_rifugio1
            id_rifugio2 = connessione.id_rifugio2
            h1, h2 = sorted((id_rifugio1, id_rifugio2))
            r1 = self.refuges[h1]
            r2 = self.refuges[h2]
            if (r1, r2) not in self.dict_connessioni:
                self.dict_connessioni[r1, r2] = connessione

        # pulisco il grafo e lo ricreo
        self.G.clear()

        # aggiungo i nodi(oggetti rifugio)
        self.G.add_nodes_from(self.refuges.values())

        # aggiungo le Connessioni, cioè i sentieri

        # DALLA LISTA
        for connessione in self.connessioni:
            r1 = connessione.rifugio1
            r2 = connessione.rifugio2

            # aggiungi l'arco
            self.G.add_edge(r1, r2)

        # DAL DIZIONARIO
        for conn in self.dict_connessioni.values():
            r1 = conn.rifugio1
            r2 = conn.rifugio2
            self.G.add_edge(r1, r2)

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        # TODO
        return list(self.G.nodes())

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        # TODO
        return len(list(self.G.neighbors(node)))

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # TODO
        return nx.number_connected_components(self.G)

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """
        tic = datetime.now()
        a = self.get_reachable_dfs(start)
        print(f"DFS: {datetime.now() - tic} - {len(a)}")

        tic = datetime.now()
        b = self.get_reachable_bfs(start)
        print(f"BFS: {datetime.now() - tic} - {len(b)}")

        tic = datetime.now()
        c = self.get_reachable_iterative(start)
        print(f"ITER: {datetime.now() - tic} - {len(c)}")

        tic = datetime.now()
        d = self.get_reachable_recursive(start)
        print(f"REC: {datetime.now() - tic} - {len(d)}")

        return a

    def tree(self, start):
        albero = nx.dfs_tree(start)
        rifugi = []
        for nodo, vicino in albero():
            rifugi.append(vicino)
        return rifugi

    def get_reachable_dfs(self, start):
        """ Usa networkx.bfs tree per ottenere i nodi raggiungibili (no nodo iniziale)"""
        # va per profondità lungo un ramo finché possibile, poi torna indietro (backtracking)
        albero = nx.dfs_tree(self.G,start)
        nodes = list(albero.nodes)
        if start in nodes:
            nodes.remove(start)
        return nodes


    def get_reachable_bfs(self, start):
        """ Usa networkx.bfs_tree per ottenere i nodi raggiungibili (no nodo iniziale)"""
        # va per livelli: prima quelli vicini e poi quelli a distanza maggiore
        albero = nx.bfs_tree(self.G, start)
        nodes = list(albero.nodes)
        if start in nodes:
            nodes.remove(start)
        return nodes

    def get_reachable_iterative(self, start):
        """Implementazione iterativa (simile a BFS) che restituisce tutti i nodi raggiungibili."""
        from collections import deque

        visited = []
        to_be_visited = deque() # una doble-ended queue (coda a doppia estremità)

        # add starting node to visited
        visited.append(start)

        # add neighbors of starting node to queue
        to_be_visited.extend(self.G.neighbors(start))

        while to_be_visited:
            temp = to_be_visited.popleft() # prende l'elemento in testa alla coda

            # mark visited
            visited.append(temp)

            neighbors = list(self.G.neighbors(temp))
            not_visited_n = []

            # filter neighbors already visited
            for n in neighbors:
                if n not in visited:
                    not_visited_n.append(n)

            # filter neighbors already in to_be_visited
            not_visited_n = [n for n in not_visited_n if n not in to_be_visited]

            # enqueue remaining
            to_be_visited.extend(not_visited_n)

        # remove starting node from result
        if start in visited:
            visited.remove(start)
        return visited

    def get_reachable_recursive(self, start):
        """Versione ricorsiva (DFS) per ottenere i nodi raggiungibili"""
        visited = []
        self._recursive_visit(start, visited)
        if start in visited:
            visited.remove(start)
        return visited

    def _recursive_visit(self, start, visited):
        visited.append(start)
        neighbors = list(self.G.neighbors(start))
        for n in neighbors:
            if n not in visited:
                self._recursive_visit(n, visited)

        # TODO