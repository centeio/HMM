

class Model():

    def __init__(self):
        self.states = ['0','1','2','3','4','5','6','7','8','9']
        self.symbols = ['A','C','G','T']
        self._trans_dict = {'0': {'0': 0.3,'1': 0, '2': 0.35,'3': 0.35, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '1': {'0': 0.3,'1': 0, '2': 0.35,'3': 0.35, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '2': {'0': 0.3,'1': 0, '2': 0.35,'3': 0.35, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '3': {'0': 0.3,'1': 0, '2': 0.35,'3': 0.35, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '4': {'0': 0.3,'1': 0, '2': 0.35,'3': 0.35, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '5': {'0': 0.3,'1': 0, '2': 0.35,'3': 0.35, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '6': {'0': 0.3,'1': 0, '2': 0.35,'3': 0.35, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '7': {'0': 0.3,'1': 0, '2': 0.35,'3': 0.35, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '8': {'0': 0.3,'1': 0, '2': 0.35,'3': 0.35, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '9': {'0': 0.3,'1': 0, '2': 0.35,'3': 0.35, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
                            }
        self._emit_dict = {'0': {'A': 0.25, 'C':0.25, 'G':0.25, 'T': 0.25}, 
                            '1': {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25}, 
                            '2': {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25},
                            '3': {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25},
                            '4': {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25},
                            '5': {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25},
                            '6': {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25},
                            '7': {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25},
                            '8': {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25},
                            '9': {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25}}

        self._init_p = {'0':1,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0}

    def prob_emit(self, state, symbol):
        #TODO train
        return self._emit_dict[state][symbol]

    def prob_trans(self, fromstate, tostate):
        #TODO train
        return self._trans_dict[fromstate][tostate]

    def is_silent(self, state):
        for value in self._symbols:
            if(self._emit_dict[state][value] != 0):
                return false

        return true

    def viterbi(self, obs):
        vit = [{}]
        path = {}     
        # Initialize
        for y in self.states:
            vit[0][y] = self._init_p[y] * self._emit_dict[y][obs[0]]
            path[y] = [y]

        print(vit)
        for t in range(1, len(obs)):
            vit.append({})
            newpath = {}     
            for y in self.states:
                (prob, state) = max((vit[t-1][y0] * self._trans_dict[y0][y] * self._emit_dict[y][obs[t]], y0) for y0 in self.states)
                vit[t][y] = prob
                newpath[y] = path[state] + [y]     

            path = newpath
        n = 0
        if len(obs)!=1:
            n = t
        (prob, state) = max((vit[n][y], y) for y in self.states)
        return (prob, path[state])

    def forward(self, obs):
        fwd = [{}]     
        # t == 0
        for y in self.states:
            fwd[0][y] = self._init_p[y] * self._emit_dict[y][obs[0]]
        # t > 0
        for t in range(1, len(obs)):
            fwd.append({})     
            for y in self.states:
                fwd[t][y] = sum((fwd[t-1][y0] * self._trans_dict[y0][y] * self._emit_dict[y][obs[t]]) for y0 in self.states)
        prob = sum((fwd[len(obs) - 1][s]) for s in self.states)
        return prob

    


if __name__ == "__main__":
    m = Model()
    prob, path = m.viterbi('AAGT')
    print(prob, path)

    p = m.forward('AAGT')
    print(p)