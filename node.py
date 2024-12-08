class Node:
    """
    La classe rappresenta un nodo del Network.

    Attributi:
        name: l'id del nodo.
        routing_table: dizionario della tabella {destinazione: (distanza, prossimo_nodo)}.
    """
    def __init__(self, name):
        self.name = name
        self.routing_table = {}

    def update_routing_table(self, neighbors):
        """
        Metodo che prende in input le informazioni sui vicini del router, così 
        ottiene la distanza dagli altri nodi e aggiorna la propria routing 
        table basandosi su quella dei vicini.
        Eseguendo questo metodo abbastanza volte viene calcolata per ogni nodo 
        la distanza da ogni altro nodo nella rete

        Argomenti:
            neighbors: dizionario dei vicini con 
            {idVicino: (peso_fino_al_vicino, routing_table_del_vicino)}.

        Returns:
            True: c'è stata una modifica alla routing table.
            False: nessuna modifica necessaria.
        """
        updated = False
        for neighbor, (cost_to_neighbor, neighbor_table) in neighbors.items():
            for dest, (neighbor_distance, neighbor_next_hop) in neighbor_table.items():
                new_distance = cost_to_neighbor + neighbor_distance
                if dest not in self.routing_table or new_distance < self.routing_table[dest][0]:
                    self.routing_table[dest] = (new_distance, neighbor)
                    updated = True
        return updated

    def print_routing_table(self):
        """
        Metodo di stampa della routing table
        """
        print(f"Routing Table per Nodo {self.name}:")
        for dest, (dist, next_hop) in self.routing_table.items():
            print(f"  Per {dest}: Distanza = {dist}, Next Hop = {next_hop}")
        print()