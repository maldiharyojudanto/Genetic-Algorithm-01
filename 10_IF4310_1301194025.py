import random
import math

JUMLAH_POPULASI = 50   #jumlah populasi antara 50-100
MUTASI_RATE = 0.01     #mutasi rate antara ~1%
CROSSOVER_RATE = 0.65  #crossover rate antara 60% - 70%
JUMLAH_GEN = 16        #jumlah gen setiap kromosom (x,y)
JUMLAHGENERASI = 20    #jumlah generasi (jika terlalu sedikit terjebak lokal optimum, jika besar akan membutuhkan waktu lama)

#######################################################################
###                     Kelompok 10 | IF-43-10                     ####
###  Anggota : - Bima Mahardika Wirawan (1301194304)               ####
###            - M. Aldi Haryojudanto (1301194025)                 ####
###            - Fiyona Anmila Syamsir (1301194201)                ####
#######################################################################

def bangkitkanPopulasi(n,JUMLAH_GEN):
    populasi = [[int(random.choice([1,0])) for i in range(JUMLAH_GEN)] for j in range(n)]
    return populasi

#DECODE CHROMOSOME (BINARY ENCODING)
def keDesimal(Des):
    return int("".join(map(str,Des)),2) #mengubah binary ke desimal
def decodeChromosome(chrome):
    JUMLAH_GEN = round(len(chrome)/2)
    x = keDesimal(chrome[:JUMLAH_GEN])
    y = keDesimal(chrome[JUMLAH_GEN:])
    pembagi = 2**(len(chrome)/2)-1  #rumus pembagi atau sigma N 2^i binary encoding
    xbin = -1+((2-(-1))/pembagi)*x  #rumus bin encoding variabel x
    ybin = -1+((1-(-1))/pembagi)*y  #rumus bin encoding variabel y
    return (xbin,ybin)

#PERHITUNGAN FITNESS
def h(x,y):
    return((math.cos(x**2))*(math.sin(y**2)))+(x+y) #fungsi h(x,y) = (cos x^2 * sin y*2) + (x+y)
def hitungFitness(populasi):
    fitness = []
    for i in populasi:
        x,y = decodeChromosome(i)
        fitness.append(h(x,y)) #karena mencari nilai maksimum maka f=h #inverse kalau minimum
    return fitness

#CROSSOVER (SINGLE POINT)
def crossover(parent1,parent2,rate):
    if random.random() <= rate:
        titik_potong = random.choice(range(round(len(parent1)/2),len(parent1)-1)) #menentukan titik potong
        temp = parent1[titik_potong:]
        parent1[titik_potong:] = parent2[titik_potong:]
        parent2[titik_potong:] = temp
    return parent1,parent2

#MUTASI
def mutasi(chrome,rate):
    m = chrome.copy()
    for i in range(len(m)):
        if m[i] == 1:
            m[i] = 0
        elif m[i] == 0:
            m[i] = 1
    return m

#SELEKSI ORANG TUA (TOURNAMENT)
def tournament(populasi,fitness,n):
    acak = random.sample(range(n),round(n/2)) #membuat bilangan acak untuk memilih kandidat turnamen
    kandidat = [fitness[acak[i]] for i in range(round(n/2))]
    rank = sorted(zip(kandidat,acak), key=lambda k: k[0], reverse=True) #mengurutkan rank berbasis dari fitness
    return populasi[rank[0][1]], fitness[rank[0][1]] #mengembalikan individu terbaik dari populasi berbasis fitness rank

#PERGANTIAN GENERASI (GENERAL REPLACEMENT)
def pergantianGenerasi(populasi,fitness):
    max = round(len(populasi)/5) 
    elit = []
    rank = sorted(zip(populasi,fitness), key=lambda k: k[1], reverse=True) #mengurutkan rank berbasis dari populasi
    for i in range(max):
        elit.append(rank[i][0])
    return elit

#MAIN FUNCTION
def main():
    populasi = bangkitkanPopulasi(JUMLAH_POPULASI,JUMLAH_GEN) #memanggil fungsi bangkitkan populasi
    #jSumlah generasi adalah 20
    for generasi in range(JUMLAHGENERASI):
        n_fitness = hitungFitness(populasi)
        populasiBaru = pergantianGenerasi(populasi,n_fitness)
        while len(populasiBaru) < JUMLAH_POPULASI:
            ortu1,*_ = tournament(populasi,n_fitness,JUMLAH_POPULASI)
            ortu2,*_ = tournament(populasi,n_fitness,JUMLAH_POPULASI)
            anak1,anak2 = ortu1.copy(),ortu2.copy()
            anak1,anak2 = crossover(anak1,anak2,CROSSOVER_RATE)
            anak1 = mutasi(anak1,MUTASI_RATE)
            anak2 = mutasi(anak2,MUTASI_RATE)
            populasiBaru.extend([anak1,anak2])
        print("Generasi ke",generasi+1)
        print(*zip(populasiBaru,n_fitness),sep="\n")
        populasi = populasiBaru
    n = round(JUMLAH_POPULASI/5) #survivor selection (generational selection)
    elit = list(zip(populasi[:n],n_fitness[:n]))
    print("======================Hasil======================")
    print(*elit,sep="\n")
    print("=================================================")
    print("Kromosom terbaik :",elit[0],sep="\n")
    print("(x,y) = ",decodeChromosome(elit[0][0]))
    print("=====================Selesai=====================")

if __name__ == "__main__":
    main()