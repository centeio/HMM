from util import io
import re
import pickle

DEBUG = True
REGEX = "(?<=gene            )\d+..\d+"

class Trainer(object):
    def __init__(self):
        self._non_gene = {
                            (' ','A'):0,
                            (' ','C'):0,
                            (' ','G'):0,
                            (' ','T'):0,
                            ('A','A'):0,
                            ('A','C'):0,
                            ('A','G'):0,
                            ('A','T'):0,
                            ('C','A'):0,
                            ('C','C'):0,
                            ('C','G'):0,
                            ('C','T'):0,
                            ('G','A'):0,
                            ('G','C'):0,
                            ('G','G'):0,
                            ('G','T'):0,
                            ('T','A'):0,
                            ('T','C'):0,
                            ('T','G'):0,
                            ('T','T'):0,
                            "total": 0
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
        self._codons["FIRST"][0][(a,b)] +=1
        self._codons["FIRST"][1][(b,c)] +=1
        self._codons["FIRST"][2][(c,d)] +=1
        self._codons["FIRST"]["total"] += 3
        
        mid_codons = [sequence[i-1:i+3] for i in range(begin+3,end-3,3)]
        for a,b,c,d in mid_codons:
            self._codons["MID"][0][(a,b)] +=1
            self._codons["MID"][1][(b,c)] +=1
            self._codons["MID"][2][(c,d)] +=1
            self._mid_to_mid_codon +=1
            self._codons["MID"]["total"] += 3

        self._mid_to_last_codon += 1

        last_codon = sequence[end-4:end]
        #print("LAST_CODON",last_codon)

        a,b,c,d = last_codon
        self._codons["LAST"][0][(a,b)] +=1
        self._codons["LAST"][1][(b,c)] +=1
        self._codons["LAST"][2][(c,d)] +=1
        self._codons["LAST"]["total"] += 3
            


    def train(self, seq_path, gb_path):
        #getting data from files
        seq = io.read_fasta(io.read_file(seq_path))
        gene = io.read_file(gb_path)
        r = re.findall(REGEX,gene)
        r = [n.split('..') for n in r]
        gen_seq = [seq[int(b):int(e)] for b,e in r ]
        intervals = [(int(b),int(e)) for b,e in r ]
        
        #looping over the sequence
        state = "NON_GENE"
        self._non_gene[(' ',seq[0])] += 1
        self._non_gene["total"] += 1
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
            self._non_gene[(pred,current)] += 1
            self._non_gene["total"] += 1
            state = "NON_GENE"

        
        if(DEGUB):
            print ("FIRST",self._codons["FIRST"])
            print ("MID",self._codons["MID"])
            print ("LAST",self._codons["LAST"])
            print("NON_GENE",self._non_gene)
            print("nGene->to->gene", self._non_gene_to_gene)
            print("NGene->to->nGene", self._non_gene_to_non_gene)
            print("6->to->4", self._mid_to_mid_codon)
            print("6->to->7", self._mid_to_last_codon)
            print("TOTAL", 
                        self._codons["LAST"]["total"] +
                        self._codons["MID"]["total"] +
                        self._codons["FIRST"]["total"] +
                        self._non_gene["total"]
            )

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