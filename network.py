from node import Node

class Network:
    """
    La rappresentazione del Network in se.

    Attributi:
        nodes: dizionario dei nodi {node_name: Node(node_name)}.
        edges: dizionario degli archi {node_name1: {vicino1: weight1, ...}, ...}.
    """
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def __add_node(self, node_name):
        """
        Aggiunge un nodo al Network.

        Argomenti:
            node_name: id del nodo.
        """
        self.nodes[node_name] = Node(node_name)

    def add_edge(self, node1, node2, weight):
        """
        Crea l'arco tra nodo1 e 2 aggiungendo il peso come valore.
        Poi viene aggiunto anche alla routing table

        Argomenti:
            node1: l'id del primo nodo.
            node2: l'id del secondo nodo.
            weight: il peso dell'arco.
        """
        self.edges.setdefault(node1, {})[node2] = weight
        self.edges.setdefault(node2, {})[node1] = weight

        self.nodes[node1].routing_table[node2] = (weight, node2)
        self.nodes[node2].routing_table[node1] = (weight, node1)

    # def initialize_routing_tables(self):
    #     """
    #     Inizializza tutte le routing table con il nodo stesso (a distanza zero) e i nodi vicini a distanza uguale al peso dell'arco
    #     """
    #     for node_name, node in self.nodes.items():
    #         node.routing_table[node_name] = (0, node_name)
    #         for neighbor, weight in self.edges.get(node_name, {}).items():
    #             node.routing_table[neighbor] = (weight, neighbor)

    def simulate(self):
        """
        Algoritmo al centro del calcolo delle distanze dei router. Stampa anche 
        le routing table a ogni passo.

        A ogni iterazione ogni nodo raccoglie informazioni sui vicini e aggiorna 
        la propria routing table di conseguenza.
        """
        iteration = 0
        changes = True
        while changes:
            iteration += 1
            print(f"Iterazione {iteration}:")
            changes = False
            for node_name, node in self.nodes.items():
                neighbors = {
                    neighbor: (self.edges[node_name][neighbor], self.nodes[neighbor].routing_table)
                    for neighbor in self.edges.get(node_name, {})
                }
                if node.update_routing_table(neighbors):
                    changes = True

            if changes:
                for node in self.nodes.values():
                    node.print_routing_table()
            else:
                print("Nessun cambiamento, convergenza ottenuta")
            print("-" * 50)  # Separatore tra le iterazioni

    def add_node_after(self, node_name):
        """
        Metodo per aggiungere nodi dopo aver eseguito la simulazione.

        Argomenti:
            node_name: nodo da aggiungere.
        """
        self.__add_node(node_name)
        self.nodes[node_name].routing_table[node_name] = (0, node_name)
    
    def add_edge_and_update(self, node1, node2, weight):
        """
        Metodo per aggiungere un singolo arco dopo la simulazione.

        Argomenti:
            node1: l'id del primo nodo.
            node2: l'id del secondo nodo.
            weight: il peso dell'arco.
        """
        self.add_edge(node1, node2, weight)
        self.simulate()

    def remove_node_and_update(self, node_name):
        """
        Metodo per rimuovere un nodo (simula un guasto a un router).

        Prima il nodo viene rimosso dal Network,
        poi vengono rimossi tutti gli archi legati al nodo,
        poi ogni routing table viene rifatta per 
        garantire che non venga utilizzato.

        Argomenti:
            node_name: id del nodo da rimuovere.
        """
        if node_name in self.nodes:
            del self.nodes[node_name]

            if node_name in self.edges:
                neighbors = list(self.edges[node_name].keys())

                for neighbor in neighbors:
                    del self.edges[neighbor][node_name]

                del self.edges[node_name]

            self.__reset_routing_table()

            self.simulate()

    def remove_edge_and_update(self, node1, node2):
        """
        Metodo per la  rimozione di un arco (simula un guasto sulla linea).

        Args:
            node1: l'id del primo nodo.
            node2: l'id del secondo nodo.
        """

        if node1 in self.edges and node2 in self.edges[node1]:
            del self.edges[node1][node2]
            del self.edges[node2][node1]

            self.__reset_routing_table()
            self.simulate()

    def __reset_routing_table(self):
        """
        Metodo che resetta tutte le routing table.
        """
        for node_name, node in self.nodes.items():
            node.routing_table.clear()
            node.routing_table[node_name] = (0, node_name)
            for neighbor, weight in self.edges.get(node_name, {}).items():
                node.routing_table[neighbor] = (weight, neighbor)