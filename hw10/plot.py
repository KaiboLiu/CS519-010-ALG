import rna
import rna_liang
import time
import matplotlib.pyplot as plt




def get_colour(color):
    '''
    b---blue   c---cyan  g---green    k----black
    m---magenta r---red  w---white    y----yellow
    '''
    #color_set = ['r--','b--','m--','g--','c--','k--','y--']
    color_set = ['r','b','m','g','c','k','y']
    return color_set[color % 7]

def tune_draw(k_list, seq_list, legend, filename):
    t = [[],[],[],[]]
    
    for s in seq_list:
        for k in k_list:
            print('{}-best of len {}'.format(k,len(s)))

            t0 = time.time() 
            bench = rna_liang.kbest(s,k)
            t[3].append(time.time()-t0)

            t0 = time.time() 
            res = rna.kbest_alg2_heapn(s,k)
            t[0].append(time.time()-t0)
            check = rna.check_with_benchmark(res,bench,k)
            if check != True: print("alg2_heapn", check)

            t0 = time.time() 
            res = rna.kbest_alg2_heapk(s,k)
            t[1].append(time.time()-t0)
            check = rna.check_with_benchmark(res,bench,k)
            if check != True: print("alg2_heapk", check)

            t0 = time.time() 
            res = rna.kbest_lazy(s,k)
            t[2].append(time.time()-t0)
            check = rna.check_with_benchmark(res,bench,k)
            if check != True: print(check)

    import csv

    with open(filename+".csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(t)

    plt.figure()

    color = 0
    if len(k_list) == 1:    # tune seq length
        x_axis = tuple(map(len,seq_list))
        plt.xlim(0, len(seq_list[-1]))
        plt.title("{}-best".format(k_list[0]))
        plt.xlabel('length')
    else:
        x_axis = k_list     # tune k
        plt.xlim(k_list[0], k_list[-1])   
        plt.title("length={}".format(len(seq_list[0])))
        plt.xlabel('k-best')

    for i in range(4):
        plt.plot(x_axis,t[i], get_colour(color),label=legend[i])
        #plt.plot(x_axis,t[i], get_colour(color)+'o')
        color += 1

    plt.ylabel('time(s)')
    plt.ylim(0, t[3][-1])  
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.savefig(filename+".png")


if __name__ == "__main__":
    seq_list = [
            #"A",
            "ACAGU",
            "UUCAGGA",
            "CAUCGGGGUCUG",     # total 1223
            "UUGGACUUGAGAAAAG", # len 16
            "CCGUCAGGUCCGGAAGGAAGCAGCGGUA",
            "CAUCGGGGUCUGAGAUGGCCAUGAAGGGCACGUACUGUUU",     # len 40
            "GUCGGGCGGACGCAGCCUUCGCCAACCCGGUCAGGUCCGGAAGGAAGCAGCCGCAACGAAUU",
            "GUCGGGCGGACGGUGCUGUCGCCAACCCGGUCAGGUCCGGAAGGAAGCAGCCGUAACGAAUUUUUAUCGGGUCGUUCCGGC",
            "AAUUAUGCUAGUAGUGGGCAUUGUGCCUGUUUAGUCGGUCAGGUCUGAAAGGAAGCAGCCAGAAUGGGAUUCGAUGGGUCAUUACUAGCAUUAUUCUUA",
            "GCUGGCGGGCCCCUUCGCAUGGUUCGGCGGUGAAUCUGGUCAGGUCGGGAACGAAGCAGCCAUAGUCGUUCAGAACCAGUGCCGGAGUAAGGCUCGCCUACCGGUAUCCCU", # len 111
            "UCCUAGGUGGAGCGGGGGUGUCGUGGACCAGCGAGGGUGGCGCGCUGCGUUGACGCGGUGCUCUGCUUGGCUGUGUGUCGGUGUGGCCUGCCCCCCUGUAGAGGGGUGUCGUAGGCUACCCGUUGAAGCGAGGGAAACC",
            "GAUCCGUAACGCGAGCUUAUAACUCGAGCGGGGGCUAUAAAGGUGGUGUGGAACGAGCUGACUCGACCUGCCGGGUUGGGCCAGGGACUGCGGUGCUGGCUCGCCCGUUCCAAGUCGGGUAGUGGGCCAUGUGGCUUGGGCGAAGGCCUGGGUUUCUUGGCC",
            "GGUGGUCUGCCCGUUCCAAGUUGAGUAGUGGACCGCUUGGGGCCUAUGCGAAAGUUGGGCCUCACGGUCCAUAAUGUGGCAGGCACCGCGUGAGGCUGGCUUCACAGAGCAGCGACAACUGCCCGCUUCCAACGGUGGAAGGAUAACGGGCCGCUGCACUCCUAGGCCGCUUGGGCCUCGUAGCCAUC",
            "GAAUGGCUCGGAUUUGAUGGGCCAUUCAACUUAUAACAGGCUCCGAAGUGACCUGUAACAGUGCCAAAAUGCGGGAAUUAGCCACCUUGGUGGUGAAACCCGCAGCUGAUCACCGCGUCAGUUCAACGACUAGAUGGUACUGGCUGGUUCGUUCCAGUUAAGAUAUAGUCUCUCACCGGGGGUAAAUCCCAGUGCUUCACGGCAUUAAAU", # len 210
            "GUUGGGUUGACCCAGAUGGUUGGGUUCGGUAGGCUUAUAGUCUGGCCUGCCCUCUCCAAGCAUGGAGUUGGAUCACGUGGCUUAGUCGAAAGACCUGGGUUGCUUGAUUCCUAAAGUGGGGUGGACUGCGUGAGGCUGGUUUCACAGAGCAACGAACAGCUUCCGCUCUGUGCAGUGGAAGGAUAACGGGUCAGUGCUCAGCGAGUCCAGUUAACGCCCUGAUGGGCUGCUCCAACUAAACCACCACUUU"
            ]
    k_list = range(10,501,10)
    legend = ["alg2_1(heap n)", "alg2_2(heap k)", "alg3(pure lazy)", "benchmark"]

    print("check with benchmark: on")
    for _ in range(1):
        t0 = time.time()
        tune_draw(k_list, seq_list[9:10], legend, 't-k figure_'+time.asctime())
        print('tune k, time: {}'.format(time.time()-t0))

        t0 = time.time()
        tune_draw([50], seq_list, legend, 't-l figure_'+time.asctime())
        print('tune len, time: {}'.format(time.time()-t0))