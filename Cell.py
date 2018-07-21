class CellWithK:

    def __init__(self, ori, esi, k):
        self.ori = ori
        self.esi = esi
        self.k = k

    def get_k(self):
        return self.k

    def get_ori(self):
        return self.ori

    def get_esi(self):
        return self.esi

    def send_gossip(self):
        return self.ori, self.esi, self.k

    def gossip_rules(self, ori, esi, k):
        if self.k < k:
            self.esi = max(self.ori, esi)
            self.k = k
        elif self.k == k:
            self.esi = max(self.esi, esi)
        elif self.k > k:
            self.esi = max(self.esi, ori)

    def departure_response(self, k):
        if self.k > k:
            pass
        else:
            self.k = self.k + 1
            self.esi = self.ori


class CellWithTimer:

    def __init__(self, ori, esi, max_t):
        self.ori = ori
        self.esi = esi
        self.t = 0
        self.max_t = max_t

    def get_t(self):
        return self.t

    def get_ori(self):
        return self.ori

    def get_esi(self):
        return self.esi

    def send_gossip(self):
        return self.esi, self.t

    def gossip_rules(self, esi, t):
        if self.esi < esi:
            self.t = t
            self.esi = esi
        elif self.esi > esi:
            pass
        elif self.esi == esi:
            self.t = max(self.t, t)

    def update_timer(self):
        if self.ori == self.esi:
            self.t = 0
        elif self.ori != self.esi:
            self.t += 1
        if self.t == self.max_t:
            self.esi = self.ori
            self.t = 0
