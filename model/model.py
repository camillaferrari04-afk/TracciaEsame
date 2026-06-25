import copy

from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = []
        self._idMap = {}

    #OGGETTI PER DROPDOWN
    def ratings(self):
        return DAO.getallratings()

    #RIEMPIMENTO DEL GRAFO
    def creategraph(self, basso:float, alto:float):
        self._graph.clear()
        self.addnodes(basso, alto)
        self.addedges(basso, alto)
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def addnodes(self, basso, alto):
        self._nodes = []
        self._idMap = {}
        for n in DAO.getnodes(basso, alto):
            self._graph.add_node(n)
            self._nodes.append(n)
            self._idMap[n.id] = n

    def addedges(self, basso, alto):
        #dizionario id1, id2, weight
        for n in DAO.getedges(basso, alto):
            self._graph.add_edge(self._idMap[n["id1"]], self._idMap[n["id2"]], weight=n["weight"])

    #INFO AGGIUNTIVE SUL GRAFO
    #numero componenti connesse, con connessa piu lunga
    def getcompconnessa(self):
        connesse = list(nx.connected_components(self._graph))
        largest_cc = list(max(nx.connected_components(self._graph), key=len))
        return len(connesse), largest_cc

    #archi ordinati per peso decrescente. 3 archi più grandi
    def getarchimaggiori(self):
        archi = list(self._graph.edges(data=True))
        archi.sort(key=lambda x:x[2]["weight"], reverse=True)
        return archi[0:min(3, len(archi))]

########################################################################################################
# RICORSIONE
########################################################################################################
#####TIPO1 -> CICLO SUI VICINI
    def percorsoottimo(self):
        self.bestperc = []
        self.bestcost = 0
        parziale=[]
        costo=0

        def ricorsione(nodo, costoparziale, parziale):
            #uscita

            #aggiorno
            if costoparziale>self.bestcost:
                self.bestcost = costoparziale
                self.bestperc = copy.deepcopy(parziale)

            #ricorsione
            for n in self._graph.neighbors(nodo):
                if self.geteta(n)<self.geteta(parziale[-1]):
                    parziale.append(n)
                    ricorsione(n, costoparziale+self._graph.get_edge_data(parziale[-2],parziale[-1])["weight"], parziale)
                    parziale.pop()

        for n in self._graph.nodes():
            parziale.append(n)
            ricorsione(n, costo, parziale)
            parziale.pop()

        return self.bestcost, self.bestperc

    #CALCOLO DEL VALORE
    def geteta(self, nodo):
        annonascita = nodo.date_of_birth
        return 2026-annonascita.year

##### TIPO2 -> CICLO SULLE COMPONENTI
    def percorsoottimo(self, massimo_nodi):
        componenti = list(nx.connected_components(self._graph))
        parziale = []
        self.best_insieme = []
        self.best_costo = []

        def ricorsione(parziale, massimo_nodi, corrente, componenti):
            #condizione di uscita
            if len(parziale)==massimo_nodi:
                #condizione di ottimo
                if sum([a.ratingmedio for a in parziale]) > self.best_rating:
                    self.best_rating = sum([a.ratingmedio for a in parziale])
                    self.best_insieme = copy.deepcopy(parziale)
                return

            #non posso più raggiungere uscita->esco
            if len(componenti)-corrente < massimo_nodi:
                return

            #a ogni ciclo decido se prendere da questa componente o no
            #CASO 1: PRENDO CORRENTE -> ciclo sugli attori del componente
            for a in componenti[corrente]:
                parziale.append(a)
                ricorsione(parziale, massimo_nodi, corrente+1, componenti)
                parziale.pop()

            #CASO 2: NON PRENDO CORRENTE
            ricorsione(parziale, massimo_nodi, corrente+1, componenti)

        ricorsione(parziale, massimo_nodi, 0, componenti)

        return self.best_insieme, self.best_costo

