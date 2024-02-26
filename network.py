import pickle

import networkx as nx
from matplotlib import pyplot as plt


class Network:
    def __init__(self):
        self.computers = nx.Graph()

    def add_computer(self, computer):
        self.computers.add_node(computer)

    def add_link(self, computer1, computer2, time):
        self.computers.add_edge(computer1, computer2, time=time)

    def remove_link(self, computer1, computer2):
        try:
            self.computers.remove_edge(computer1, computer2)
        except nx.NetworkXError:
            raise ValueError("⚠️ Il n'y a pas de lien direct entre ces deux ordinateurs")

    def draw(self):
        print(self.computers)

        plt.figure(figsize=(10, 8))

        pos = nx.spring_layout(self.computers, scale=10)
        edge_labels = nx.get_edge_attributes(self.computers, 'time')

        nx.draw_networkx_nodes(self.computers, pos, node_color='lightblue', node_size=1200)
        nx.draw_networkx_edges(self.computers, pos)
        bbox = dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5')
        nx.draw_networkx_labels(self.computers, pos, font_size=7, bbox=bbox)
        nx.draw_networkx_edge_labels(self.computers, pos, edge_labels=edge_labels)

        plt.axis('off')

        plt.tight_layout()  # Adjust spacing between elements
        plt.show()

    def save(self, filename):
        with open(f'./network/{filename}', 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load(filename):
        with open(f'./network/{filename}', 'rb') as file:
            return pickle.load(file)

    def find_page_from(self, source, page):
        distances = {}
        previous = {}

        for computer in self.computers:
            distances[computer] = float('inf')
            previous[computer] = None

        distances[source] = 0
        process_tab = [source]
        visited = []
        have_the_page = []

        while process_tab:
            current = min(process_tab, key=lambda x: distances[x])
            process_tab.remove(current)
            visited.append(current)

            if current.get_page(page):
                have_the_page.append(current)

            for adj, value in self.computers.adj.get(current).items():
                if adj not in visited:
                    process_tab.append(adj)
                    temp = distances[current] + value['time']
                    if temp < distances[adj]:
                        distances[adj] = temp
                        previous[adj] = current

        path = []
        destination = min(have_the_page, key=lambda x: distances[x]) if have_the_page else None
        distance = distances.get(destination)
        while destination:
            path.append((destination, f"{distances[destination]}"))
            destination = previous[destination]
        path.reverse()

        return [path, distance]

    def get_computer_by_ip(self, ip):
        for computer in self.computers:
            if computer.ip == ip:
                return computer
        return None
