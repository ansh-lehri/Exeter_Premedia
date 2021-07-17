import time
from memory_profiler import profile


class Preprocess:
    
    
    # __init__ method is profiled to calculate memory consumption of process. It includes initialisation of all objects and 
    # calling of functions.
    @profile
    def __init__(self):

        self.find_words = self.read_find_words("find_words.txt")
        self.french_dict = self.read_french_dictionary("french_dictionary.csv")
        self.words_replaced = []
        self.set_words_replaced = set()
        self.set_size = 0
        self.process_file("t8.shakespeare.txt","t8.shakespeare.translated.txt")
        self.create_frequency_csv()
        
        print("List of words replaced: \n")
        print(self.words_replaced)
        print()
        print("Count of each word replaced:\n")
        print(self.find_words)
        print()
        
    
    
    # uses self.find_words and self.french_dict to write English word, French Word and Number of times the english word is 
    # replaced(Frequency) in a Frequency.csv file.
    def create_frequency_csv(self):
        
        import csv
        with open("Frequency.csv",'a+',encoding="utf-8",newline='') as freqfile:
            writer = csv.writer(freqfile,delimiter=',')
            writer.writerow(["English word","French word","Frequency"])
            for key in list(self.find_words.keys()):
                writer.writerow([key]+[self.french_dict[key]]+[self.find_words[key]])       
        
        return
   
    
    # reads find_words.txt file and returns dictionary of words.
    def read_find_words(self,path):
        
        from collections import defaultdict
        
        words_dict = defaultdict(int)
        
        with open(path,'r',encoding="utf-8") as fileobj:
            for line in fileobj:
                words_dict[line.split("\n")[0]]=0
                
                
        return dict(words_dict)
        
    
    # reads french_dictionary.csv and returns dictionary of words to translate.
    def read_french_dictionary(self,path):
    
        import csv
        
        a_csv_file = open(path, "r",encoding="utf-8")
        dict_reader = csv.DictReader(a_csv_file,fieldnames=['English','French'])
        
        french_dict = {row['English']:row['French'] for row in dict_reader}
        
        a_csv_file.close()
        return french_dict
    
    
    # process each line of input file. Splits the line on " " and check if each word belongs to list of words to replace.
    # If does, the word is replaced with its French alternative and self.find_words value for the replaced word is incremented by one.
    def find_replace(self,line,outputobj):
    
        sentence_words = line.split(" ")
        new_line = ""
        
        for word in sentence_words:
        
            if word in self.find_words.keys():
                new_line+=self.french_dict[word]
                new_line+=" "
                self.find_words[word]+=1
                
                self.set_size = len(self.set_words_replaced)
                self.set_words_replaced.add(word)
                if self.set_size!=len(self.set_words_replaced):
                    self.words_replaced.append(word)
                
            else:
                new_line+=word
                new_line+=" "
        
        
        new_line=new_line.rstrip(" ")        
        outputobj.write(new_line)
        return
            
    
    # opens input file = "t8.shakespeare.txt" and output file = "t8.shakespeare.translated.txt" and perform find and replace 
    # process line by line
    def process_file(self,input_file,output_file):
    
        with open(output_file,'a+',encoding="utf-8") as outputobj:
            with open(input_file,'r',encoding="utf-8") as inputobj:
                for line in inputobj:
                    #print(line)
                    self.find_replace(line,outputobj)
                    
                    
        del self.set_words_replaced
        del self.set_size
        
        return
    



if __name__=="__main__":

    
    start = time.time()       
    
    # Calling Preprocess object
    Preprocess()
    
    print("Total execution time: \n")
    print(time.time()-start)


