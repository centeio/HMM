from util import io
import re
import pickle

DEBUG = False
REGEX = "(?<=gene            )\d+..\d+"

STATE_0 = 0
STATE_1 = 1
STATE_2 = 2
STATE_3 = 3
STATE_4 = 4
STATE_5 = 5
STATE_6 = 6
STATE_7 = 7
STATE_8 = 8
STATE_9 = 9

class Trainer(object):
    def __init__(self):
        self._emit_dict = {
                            0:{(' ','A'):1,(' ','C'):1,(' ','G'):1,(' ','T'):1,('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total": 20},
                            1:{(' ','A'):1,(' ','C'):1,(' ','G'):1,(' ','T'):1,('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total": 20},
                            2:{(' ','A'):1,(' ','C'):1,(' ','G'):1,(' ','T'):1,('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total": 20},
                            3:{(' ','A'):1,(' ','C'):1,(' ','G'):1,(' ','T'):1,('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total": 20},
                            4:{(' ','A'):1,(' ','C'):1,(' ','G'):1,(' ','T'):1,('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total": 20},
                            5:{(' ','A'):1,(' ','C'):1,(' ','G'):1,(' ','T'):1,('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total": 20},
                            6:{(' ','A'):1,(' ','C'):1,(' ','G'):1,(' ','T'):1,('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total": 20},
                            7:{(' ','A'):1,(' ','C'):1,(' ','G'):1,(' ','T'):1,('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total": 20},
                            8:{(' ','A'):1,(' ','C'):1,(' ','G'):1,(' ','T'):1,('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total": 20},
                            9:{(' ','A'):1,(' ','C'):1,(' ','G'):1,(' ','T'):1,('A','A'):1,('A','C'):1,('A','G'):1,('A','T'):1,('C','A'):1,('C','C'):1,('C','G'):1,('C','T'):1,('G','A'):1,('G','C'):1,('G','G'):1,('G','T'):1,('T','A'):1,('T','C'):1,('T','G'):1,('T','T'):1,"total": 20}

                         }

        self._trans_dict = {'0': {'0': 0,'1': 0, '2': 0,'3': 0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '1': {'0': 0,'1': 0, '2': 1,'3': 0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '2': {'0': 0,'1': 0, '2': 0,'3': 1, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '3': {'0': 0,'1': 0, '2': 0,'3': 0, '4':1, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '4': {'0': 0,'1': 0, '2': 0,'3': 0, '4':0, '5':1, '6':0, '7':0, '8':0, '9':0},
                            '5': {'0': 0,'1': 0, '2': 0,'3': 0, '4':0, '5':0, '6':1, '7':0, '8':0, '9':0},
                            '6': {'0': 0,'1': 0, '2': 0,'3': 0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0},
                            '7': {'0': 0,'1': 0, '2': 0,'3': 0, '4':0, '5':0, '6':0, '7':0, '8':1, '9':0},
                            '8': {'0': 0,'1': 0, '2': 0,'3': 0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':1},
                            '9': {'0': 1,'1': 0, '2': 0,'3': 0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
                            }

        #counting number of states changes
        self._non_gene_to_gene = 0
        self._non_gene_to_non_gene = 0
        self._mid_to_last_codon = 0
        self._mid_to_mid_codon = 0

    def count_genes(self, sequence, begin, end):
        '''
            This function handles the gene sequence inside the sequence
            it populates the _codons dictionary
        '''
        first_codon = sequence[begin-1:begin+3]
        
        a,b,c,d  = first_codon
        self._emit_dict[STATE_1][(a,b)] +=1
        self._emit_dict[STATE_1]["total"] +=1
        self._emit_dict[STATE_2][(b,c)] +=1
        self._emit_dict[STATE_2]["total"] +=1
        self._emit_dict[STATE_3][(c,d)] +=1
        self._emit_dict[STATE_3]["total"] +=1
        
        
        mid_codons = [sequence[i-1:i+3] for i in range(begin+3,end-3,3)]
        for a,b,c,d in mid_codons:
            self._emit_dict[STATE_4][(a,b)] +=1
            self._emit_dict[STATE_4]["total"] +=1
            self._emit_dict[STATE_5][(b,c)] +=1
            self._emit_dict[STATE_5]["total"] +=1
            self._emit_dict[STATE_6][(c,d)] +=1
            self._emit_dict[STATE_6]["total"] +=1
            self._mid_to_mid_codon +=1
            

        self._mid_to_last_codon += 1

        last_codon = sequence[end-4:end]
        #print("LAST_CODON",last_codon)

        a,b,c,d = last_codon
        self._emit_dict[STATE_7][(a,b)] +=1
        self._emit_dict[STATE_7]["total"] +=1
        self._emit_dict[STATE_8][(b,c)] +=1
        self._emit_dict[STATE_8]["total"] +=1
        self._emit_dict[STATE_9][(c,d)] +=1
        self._emit_dict[STATE_9]["total"] +=1
            
    def train(self, seq_path, gb_path):
        #getting data from files
        seq = io.read_fasta(io.read_file(seq_path))
        gene = io.read_file(gb_path)
        r = re.findall(REGEX,gene)
        r = [n.split('..') for n in r]
        intervals = [(int(b),int(e)) for b,e in r ]
        
        #looping over the sequence
        state = "NON_GENE"
        self._emit_dict[STATE_0][(' ',seq[0])] += 1
        self._emit_dict[STATE_0]["total"] += 1
        j=0
        gene_interval = intervals[j]

        for i in range(1,len(seq)):
            
            #if is a gene interval, handle with count_genes function
            if(i == gene_interval[0]):
                self._non_gene_to_gene += 1
                
                if(j < len(intervals)-1):
                    j+=1
                
                self.count_genes(seq,i,gene_interval[1])
                i = gene_interval[1]
                gene_interval = intervals[j]
                state = "GENE"
                continue

            if(state=="NON_GENE"):
                self._non_gene_to_non_gene +=1 
            
            #if not, update gene dict
            pred = seq[i-1]
            current = seq[i]
            self._emit_dict[STATE_0][(pred,current)] += 1
            self._emit_dict[STATE_0]["total"] += 1
            state = "NON_GENE"

        #updating trans dict
        weight = (self._non_gene_to_non_gene+self._non_gene_to_gene) 
        self._trans_dict['0']['0'] = self._non_gene_to_non_gene / weight
        self._trans_dict['0']['1'] = self._non_gene_to_gene / weight

        weight = self._mid_to_mid_codon + self._mid_to_last_codon
        self._trans_dict['6']['4'] = self._mid_to_mid_codon / weight
        self._trans_dict['6']['7'] = self._mid_to_last_codon / weight

        #TODO atualizar o dicionario com as probabilidades baseado na lógica abaixo
        for state in self._emit_dict:
            #gets the counts tuples such as (('A','T'), 123123)
            counts = [(elem,self._emit_dict[state][elem]) for elem in self._emit_dict[state]]
            
            tempDict = {}
            for base in ['A','C','T','G',' ']:
                tempDict[base] = sum([c for (elem,c) in counts if elem[0]==base])
            
            for elem in self._emit_dict[state]:
                if elem == "total":
                    continue
                self._emit_dict[state][elem] = self._emit_dict[state][elem]/tempDict[elem[0]]

        if(DEBUG):
            print ("EMIT_DICT",self._emit_dict)
            print ("TRANS_DICT", self._trans_dict)
            
    def persist(self, path):
        pickle.dump(self,open( path, "wb" ))

    @staticmethod
    def retrieve(path):
        return pickle.load(open( path, "rb" ) )

    '''
    GETTERS
    '''
    def get_trans_dict(self):
        return self._trans_dict

    def get_emit_dict(self):
        return self._emit_dict
    
#Example of usage
# def main():
#     t = Trainer()
#     t.train("./NC_000913_3.fasta", "./NC_000913_3.gb")
#     t.persist("./trained.p")
#     t3 = Trainer.retrieve("./trained.p")

# if __name__ == '__main__':
#    main()