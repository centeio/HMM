from util import io
import re
import pickle

DEBUG = True
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
                            0:{(' ','A'):0,(' ','C'):0,(' ','G'):0,(' ','T'):0,('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0,"total": 0},
                            1:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0,"total":0},
                            2:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0,"total":0},
                            3:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0,"total":0},
                            4:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0,"total":0},
                            5:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0,"total":0},
                            6:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0,"total":0},
                            7:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0,"total":0},
                            8:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0,"total":0},
                            9:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0,"total":0}

                         }

        self._codons = {
                        "FIRST":{
                                    0:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0},
                                    1:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0},
                                    2:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0}
                                    ,"total": 0
                                },
                        "MID":{
                                    0:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0},
                                    1:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0},
                                    2:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0}
                                    ,"total":0
                                },
                        "LAST":{
                                    0:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0},
                                    1:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0},
                                    2:{('A','A'):0,('A','C'):0,('A','G'):0,('A','T'):0,('C','A'):0,('C','C'):0,('C','G'):0,('C','T'):0,('G','A'):0,('G','C'):0,('G','G'):0,('G','T'):0,('T','A'):0,('T','C'):0,('T','G'):0,('T','T'):0}
                                    ,"total":0
                                }
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

        
        if(DEBUG):
            print ("EMIT_DICT",self._emit_dict)
            print("nGene->to->gene", self._non_gene_to_gene)
            print("NGene->to->nGene", self._non_gene_to_non_gene)
            print("6->to->4", self._mid_to_mid_codon)

    def persist(self, path):
        pickle.dump(self,open( path, "wb" ))

    
    @staticmethod
    def retrieve(path):
        return pickle.load(open( path, "rb" ) )

def main():
    t = Trainer()
    t.train("./NC_000913_3.fasta", "./NC_000913_3.gb")
    t.persist("./trained.p")
    t3 = Trainer.retrieve("./trained.p")

if __name__ == '__main__':
    main()