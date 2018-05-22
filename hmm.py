from util import io
from trainer import Trainer

class Model():

    def __init__(self):
        self.states = ['0','1','2','3','4','5','6','7','8','9']
        self.symbols = ['A','C','G','T']
        self._emit_dict = {
                    0:{(' ','A'):1,(' ','C'):1,(' ','G'):1,(' ','T'):1,('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total": 20},
                    1:{('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total":16},
                    2:{('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total":16},
                    3:{('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total":16},
                    4:{('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total":16},
                    5:{('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total":16},
                    6:{('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total":16},
                    7:{('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total":16},
                    8:{('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total":16},
                    9:{('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total":16}
                    }

        self._trans_dict = {
                    '0':{'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0},
                    '1':{'0':0,'1':0,'2':1,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0},
                    '2':{'0':0,'1':0,'2':0,'3':1,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0},
                    '3':{'0':0,'1':0,'2':0,'3':0,'4':1,'5':0,'6':0,'7':0,'8':0,'9':0},
                    '4':{'0':0,'1':0,'2':0,'3':0,'4':0,'5':1,'6':0,'7':0,'8':0,'9':0},
                    '5':{'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':1,'7':0,'8':0,'9':0},
                    '6':{'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0},
                    '7':{'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':1,'9':0},
                    '8':{'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':1},
                    '9':{'0':1,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0}
                    }

        self._init_p = {'0':1,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0}

    def prob_emit(self, state, current, prev=' '):
        #TODO train
        return self._emit_dict[int(state)][(prev,current)]

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
            vit[0][y] = self._init_p[y] * self.prob_emit(y,current=obs[0])
            path[y] = [y]


        for t in range(1, len(obs)):
            vit.append({})
            newpath = {}        
            for y in self.states:
                (prob, state) = max((vit[t-1][y0] * self.prob_trans(y0,y) * self.prob_emit(y,obs[t],obs[t-1]), y0) for y0 in self.states)
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
            fwd[0][y] = self._init_p[y] * self.prob_emit(state=y,current=obs[0])
        # t > 0
        
        for t in range(1, len(obs)):
            fwd.append({})  
            for y in self.states:
                fwd[t][y] = sum((fwd[t-1][y0] * self.prob_trans(fromstate=y0, tostate=y) * self.prob_emit(state=y,prev=obs[t-1], current=obs[t])) for y0 in self.states)
        
        prob = sum((fwd[len(obs) - 1][s]) for s in self.states)
        return prob
    
    def set_emit_dict(self, dictionary):
        self._emit_dict = dictionary

    def set_trans_dict(self, dictionary):
        self._trans_dict = dictionary

def intervals(path):
    start = False
    r=[]
    for i in range(len(path)):
        if(path[i]=='1'):
            r.append(i)
            start = True
        if(start and path[i]=='9'):
            r.append(i)
            start = False

    return list(zip(r[0::2],r[1::2]))

if __name__ == "__main__":
    #train
    print("Training...")
    t = Trainer()
    t.train("./input/train/NC_000913_3.fasta", "./input/train/NC_000913_3.gb")
    t.persist("./trained.p")
    #t = Trainer.retrieve("./trained.p")
    #create model
    m = Model()
    #setting trained info
    m.set_trans_dict(t.get_trans_dict())
    m.set_emit_dict(t.get_emit_dict())


    print("NC_000913_3 (same)...")
    coli = io.read_fasta(io.read_file("./input/test/NC_000913_3.fasta"))
    coli = coli[:1250]
    print("Viterbi...")
    prob, path = m.viterbi(coli)
    #print(prob, path)
    print("GENES", intervals(path))
    print("Forward...")
    p = m.forward(coli)
    print("Probability",p)

    print("CU928164.2 (likely)...")
    coli = io.read_fasta(io.read_file("./input/test/CU928164.2.fasta"))
    coli = coli[:1250]
    print("Viterbi...")
    prob, path = m.viterbi(coli)
    #print(prob, path)
    print("GENES", intervals(path))
    print("Forward...")
    p = m.forward(coli)
    print("Probability",p)


    print("FRDV01000033.1 (different)...")
    coli = io.read_fasta(io.read_file("./input/test/FRDV01000033.1.fasta"))
    coli = coli[:1250]
    print("Viterbi...")
    prob, path = m.viterbi(coli)
    #print(prob, path)
    print("GENES", intervals(path))
    print("Forward...")
    p = m.forward(coli)
    print("Probability",p)

