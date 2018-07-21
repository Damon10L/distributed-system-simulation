import random as rnd
from matplotlib import pyplot as plt
from Cell import CellWithK


class Gossip:

    def __init__(self, network_size):  # network_size is 25
        self.network_size = network_size
        self.om = 0  # index of the first max value x
        self.sm = 0  # index of the second max value x
        self.cells = []
        self.edges = []
        self.estimate_values = []
        self.generate_cells()
        self.initialize_esi()
        self.create_graph()
        self.run()
        self.draw()

    #   attributes has to be clarified before methods

    #   generate cells according to the width and height
    def generate_cells(self):
        for i in range(0, self.network_size):
            ori = rnd.randint(1, 900)
            cl = CellWithK(ori, ori, 0)
            self.estimate_values.append([])
            self.cells.append(cl)
        sec_max = CellWithK(900, 900, 0)
        one_max = CellWithK(999, 999, 0)
        self.sm = rnd.randint(0, 24)
        self.om = rnd.randint(0, 24)
        self.cells[self.sm] = sec_max
        self.cells[self.om] = one_max

    def create_graph(self):  # The graph MUST be a connected graph
        for row in range(0, self.network_size):
            self.edges.append([])
            for col in range(0, self.network_size-1):  # Deciding the neighbours of each cell
                self.edges[row].append(col-1)
                self.edges[row].append(col+1)
        self.edges[self.network_size-1].append(self.network_size-2)
        self.edges[self.network_size-1].append(self.network_size-3)

    def initialize_esi(self):
        for i in range(0, self.network_size):
            self.estimate_values[i].append(self.cells[i].get_esi())

    def randompick(self, l):
        try:
            index = l[rnd.randint(0, len(l)-1)]
            new_index = index
            return self.cells[index]
        except IndexError:
            while new_index == index:
                new_index = l[rnd.randint(0, len(l) - 1)]
            return self.cells[new_index]

    def run(self):  # (only) two agents are selected randomly to exchange their information in gossip
        cnt = 0
        while cnt < 500:  # break condition is all esi == 9
            for p in range(0, self.network_size):
                try:
                    # gossip messaging
                    # neighbour = self.randompick(self.edges[p])  # randomly pick a neighbour to exchange package
                    # base = self.cells[p]
                    # ori, esi, k = neighbour.send_gossip()
                    # ori_n, esi_n, k_n = base.send_gossip()
                    # base.gossip_rules(ori, esi, k)
                    # neighbour.gossip_rules(ori_n, esi_n, k_n)
                    # current_esi = base.get_esi()

                    # deterministic crowding messaging
                    for i in range(0, 2):
                        try:
                            neighbour = self.cells[self.edges[p][i]]
                            base = self.cells[p]
                            ori, esi, k = neighbour.send_gossip()
                            ori_n, esi_n, k_n = base.send_gossip()
                            base.gossip_rules(ori, esi, k)
                            neighbour.gossip_rules(ori_n, esi_n, k_n)
                            current_esi = base.get_esi()
                        except IndexError:
                            pass

                    for q in range(0, self.network_size):
                        try:
                            self.estimate_values[q].append(self.cells[q].get_esi())
                        except IndexError:
                            self.estimate_values[q].append(0)
                            pass
                    self.estimate_values[p].pop()
                    self.estimate_values[p].append(current_esi)
                    # if cnt == 230:
                    #     self.drop_cell()
                    cnt = cnt + 1
                    if cnt == 230:
                        self.drop_cell_in_crowding()
                except IndexError:
                    print("Error Detected")



    def drop_cell(self):
        neighbour = self.randompick(self.edges[self.om])
        base = self.cells[self.om]
        ori_n, esi_n, k_n = base.send_gossip()
        neighbour.departure_response(k_n)
        self.cells.remove(self.cells[self.om])
        self.edges.remove(self.edges[self.om])
        self.network_size -= 1

    def drop_cell_in_crowding(self):
        for i in range(0, len(self.edges[self.om])):
            neighbour = self.cells[self.edges[self.om][i]]
            base = self.cells[self.om]
            ori_n, esi_n, k_n = base.send_gossip()
            neighbour.departure_response(k_n)
        self.cells.remove(self.cells[self.om])
        self.network_size -= 1

    def draw(self):
        for i in range(0, self.network_size):
            plt.plot(range(0, len(self.estimate_values[i])), self.estimate_values[i])
            print(self.estimate_values[i])
            print(i)
        print(self.om)
        print(self.sm)
        plt.show()


if __name__ == '__main__':
        sim = Gossip(25)
