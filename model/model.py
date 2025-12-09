import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.lista_rifugi = []
        self.dizionario_rifugi = {}
        self.lista_rifugi_grafo = []
        self._rifugi_visitati = set()
        self._rifugi_vicini = []

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        # meglio pulirlo prima per sicurezza
        self.G.clear()

        # carico i rifugi e costruisco il dizionario
        rifugi = DAO.read_all_rifugi()
        self.lista_rifugi = rifugi
        for rifugio in self.lista_rifugi:
            self.dizionario_rifugi[rifugio.id] = rifugio

        # posso leggere le connessioni

        listaConnessioni = DAO.read_all_connessioni()
        for c in listaConnessioni:
            if c.anno <= year:
                u_nodo = self.dizionario_rifugi[c.id_rifugio1]
                v_nodo = self.dizionario_rifugi[c.id_rifugio2]
                self.G.add_edge(u_nodo, v_nodo)

        # TODO

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """

        return list(self.G.nodes)
        # TODO

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """

        return self.G.degree(node)

        # TODO

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """

        return nx.number_connected_components(self.G)

        # TODO

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

        # Se partiamo da A:
        # Visitiamo A
        # Passiamo a B (vicino di A)
        # Passiamo a D (vicino di B)
        # D non ha vicini non visitati → torniamo a B → torniamo ad A
        # Passiamo a C (altro vicino di A)
        # Fine
        self._rifugi_visitati = set()
        self._rifugi_vicini = []

        # aggiungo il nodo sorgente ai rifugi visitati
        self._rifugi_visitati.add(start)

        # quando ho controllato tutti i vicini: ho visitato

        # controllo tutti i vicini del rifugio iniziale
        rifugi_vicini = self.G.neighbors(start)

        # visito tutti i rifugi vicini
        for rifugio in rifugi_vicini:
            if rifugio not in self._rifugi_visitati:
                # devo aggiungere tutti i rifugi a loro vicini
                self._rifugi_vicini.append(rifugio)
                self.ricorsione(rifugio)
        return self._rifugi_vicini

    def ricorsione(self, nodo_corrente):

        # condizione terminale
        if nodo_corrente in self._rifugi_visitati:
            # se il rifugio è già stato visitato vado indietro
            return
        else:
            # se non è stato ancora visitato: lo visito
            self._rifugi_visitati.add(nodo_corrente)
            rifugi_vicini = self.G.neighbors(nodo_corrente)
            for rifugio in rifugi_vicini:
                if rifugio not in self._rifugi_visitati:
                    self._rifugi_vicini.append(rifugio)
                    self.ricorsione(rifugio)


        # TODO

    # primo metodo

    """
    def get_reachable_bfs_tree(self, start):
        # albero di visita
        albero = nx.dfs_tree(self.G, start)

        # escludo il nodo di partenza stesso (start)
        nodi_raggiungibili = []
        for elemento in albero:
            if elemento != start:
                nodi_raggiungibili.append(elemento)

        return nodi_raggiungibili
    """
