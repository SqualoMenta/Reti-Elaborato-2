import tkinter as tk
from tkinter import messagebox, simpledialog
from network import Network

class NetworkGUI:
    """
    La classe per creare la gui che mostra le routing table complete, se si vuole vedere nel terminale ogni iterazione basta rimuovere add_edge_and_update e sostituirlo con add_edge e rimuovere il commento sul tasto simulate
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Network Routing Simulation")
        self.root.geometry("600x600")

        self.network = Network()

        bg_color = "gray20"
        fg_color ="white"
        btn_color = "dodger blue"
        btn_fg_color = "white"

        self.root.configure(bg=bg_color)

        self.title_label = tk.Label(root, text="Simulazione del Protocollo di Routing", fg=fg_color, bg=bg_color, font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        # Area per la visualizzazione delle tabelle di routing
        self.routing_table_label = tk.Label(root, text="Tabelle di Routing", fg=fg_color, bg=bg_color, font=("Helvetica", 10))
        self.routing_table_label.pack(pady=5)

        self.routing_text = tk.Text(root, height=20, width=60, state=tk.DISABLED, bg="gray4", fg=fg_color, font=("Consolas", 10))
        self.routing_text.pack(pady=10)

        # Pannello comandi
        self.command_frame = tk.Frame(root, bg=bg_color)
        self.command_frame.pack(pady=10)

        # Pulsanti per Test
        #self.initialize_button = tk.Button(self.command_frame, text="Testa", command=self.initialize_network)

        #Pulsante per far simulare il routing convergence
        self.simulate_button = tk.Button(self.command_frame, text="Simula", command=self.simulate_network, bg=btn_color, fg=btn_fg_color, font=("Helvetica", 10, "bold"))
        self.simulate_button.grid(row=0, column=2, padx=5, pady=5)

        # Pulsanti principali
        self.add_edge_button = tk.Button(self.command_frame, text="Add Edge", command=self.add_edge, bg=btn_color, fg=btn_fg_color, font=("Helvetica", 10, "bold"))
        self.add_edge_button.grid(row=0, column=0, padx=5, pady=5)

        self.add_node_button = tk.Button(self.command_frame, text="New Node", command=self.add_node, bg=btn_color, fg=btn_fg_color, font=("Helvetica", 10, "bold"))
        self.add_node_button.grid(row=0, column=1, padx=5, pady=5)

        self.remove_edge_button = tk.Button(self.command_frame, text="Remove Edge", command=self.remove_edge, bg=btn_color, fg=btn_fg_color, font=("Helvetica", 10, "bold"))
        self.remove_edge_button.grid(row=1, column=0, padx=5, pady=5)

        self.remove_node_button = tk.Button(self.command_frame, text="Remove Node", command=self.remove_node, bg=btn_color, fg=btn_fg_color, font=("Helvetica", 10, "bold"))
        self.remove_node_button.grid(row=1, column=1, padx=5, pady=5)

    def update_routing_table_display(self):
        """Aggiorna la visualizzazione delle tabelle di routing."""
        self.routing_text.config(state=tk.NORMAL)
        self.routing_text.delete(1.0, tk.END)
        for node_name, node in self.network.nodes.items():
            self.routing_text.insert(tk.END, f"Routing Table per Nodo {node_name}:\n")
            for dest, (dist, next_hop) in node.routing_table.items():
                self.routing_text.insert(tk.END, f"  Per {dest}: Distanza = {dist}, Next Hop = {next_hop}\n")
            self.routing_text.insert(tk.END, "\n")
        self.routing_text.insert(tk.END, "-----------------------------------------------------------\n")
        self.routing_text.config(state=tk.DISABLED)

    # def initialize_network(self):
    #     self.network.add_node('A')
    #     self.network.add_node('B')
    #     self.network.add_node('C')
    #     self.network.add_node('D')

    #     self.network.add_edge('A', 'B', 1)
    #     self.network.add_edge('B', 'C', 2)
    #     self.network.add_edge('A', 'C', 5)
    #     self.network.add_edge('C', 'D', 1)

    #     self.network.initialize_routing_tables()
    #     self.update_routing_table_display()

    def simulate_network(self):
        """Simula il routing e aggiorna le tabelle di routing (graficamente)."""
        self.network.simulate()
        self.update_routing_table_display()

    def add_edge(self):
        """Aggiunge un arco al grafo."""
        node1 = simpledialog.askstring("Input", "Inserisci il primo nodo:")
        node2 = simpledialog.askstring("Input", "Inserisci il secondo nodo:")
        weight = simpledialog.askinteger("Input", "Inserisci il peso dell'arco:")

        if node1 and node2 and weight:
            try:
                self.network.add_edge(node1, node2, weight) #possibile sostituire con add_edge se attivo il taso simulate
                self.update_routing_table_display()
            except KeyError as e:
                messagebox.showerror("Errore", f"Nodo non trovato: {e}")

    def add_node(self):
        """Aggiungi un nodo al grafo."""
        node_name = simpledialog.askstring("Input", "Inserisci il nome del nodo:")
        if node_name:
            self.network.add_node_after(node_name)
            self.update_routing_table_display()

    def remove_edge(self):
        """Rimuovi un arco dal grafo."""
        node1 = simpledialog.askstring("Input", "Inserisci il primo nodo:")
        node2 = simpledialog.askstring("Input", "Inserisci il secondo nodo:")

        if node1 and node2:
            try:
                self.network.remove_edge_and_update(node1, node2)
                self.update_routing_table_display()
            except KeyError as e:
                messagebox.showerror("Errore", f"Nodo non trovato: {e}")

    def remove_node(self):
        """Rimuovi un nodo dal grafo."""
        node_name = simpledialog.askstring("Input", "Inserisci il nome del nodo da rimuovere:")
        if node_name:
            try:
                self.network.remove_node_and_update(node_name)
                self.update_routing_table_display()
            except KeyError as e:
                messagebox.showerror("Errore", f"Nodo non trovato: {e}")

# Creazione della finestra principale di Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkGUI(root)
    root.mainloop()
