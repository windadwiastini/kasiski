# Kasiski Attack

import re
import vigenereCipher, detectEnglish

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SILENT_MODE = False # jika di set True, percobaan tidak di print
MAX_KEY_LENGTH = 8 # panjang key tidak akan lebih dari angka ini
NONLETTERS_PATTERN = re.compile('[^A-Z]')

def hackVigenere(ciphertext):
    # fungsi kasiskiExamination(ciphertext) akan me-return list dari semua kemungkinan
    # panjang keyword dalam integer di sebuah list (faktor pembagi dari jarak antar perulangan)
    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    if not SILENT_MODE:
        keyLengthStr = ''
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += '%s ' % (keyLength)
        print('Kemungkinan panjang kunci adalah: ' + keyLengthStr + '\n')

    for keyLength in allLikelyKeyLengths:
        if not SILENT_MODE:
            print('Mencari kata kunci dengan panjang %s ...' % keyLength)

        if keyLength==2:
            fo = open('2letter.txt')
        elif keyLength==3:
            fo = open('3letter.txt')
        elif keyLength==4:
            fo = open('4letter.txt')
        elif keyLength==5:
            fo = open('5letter.txt')
        elif keyLength==6:
            fo = open('6letter.txt')
        elif keyLength==7:
            fo = open('7letter.txt')
        elif keyLength==8:
            fo = open('8letter.txt')

        words = fo.readlines()
        fo.close()

        for word in words:
            word = word.strip()  # menghilangkan line baru pada akhir kata
            # meng-dekrip pesan dengan tiap kata kunci
            decryptedText = vigenereCipher.decryptMessage(word, ciphertext)
            # pengecekan tiap kata hasil dekrip dalam bahasa inggris, jika hasil return True maka akan di-print
            if detectEnglish.isEnglish(decryptedText, wordPercentage=40):
                print()
                print('Enkripsi yang mungkin:')
                print('Kunci ' + str(word) + ': ' + decryptedText[:100])
                print()
                print('Tekan D jika enkripsi benar, atau Enter untuk melanjutkan mencoba:')
                response = raw_input('> ')
                if response.upper().startswith('D'):
                    return decryptedText
                else:
                    continue

def main():
    #ciphertext = """LJV BQST NEZL QMED LJV MAMPKAUF AVAT LJV DAY YVNF JQLNP LJV HKVTRNF LJV CML KETA LJV HUYJVSF KRFT TW EFUXV HZNP."""
    #ciphertext = """U YE BV GMPFXAV U UAET PAR WJCKHMUTBG U UAET PAR WQKWEC A PQNX LGM ZGFPWTB C EGFZTG ULUA IPP G OBTN NC ZXITP"""
    ciphertext = """sixzb elqfr t augu jsg oyw e tocamzsfd m xcip cai nwammf jsg oep qk rrdxubl lrp w jtpx oyhekg apip mbf"""
    hackedMessage = hackVigenere(ciphertext)

    if hackedMessage != None:
        print('Copy message ke clipboard:')
        print(hackedMessage)
        # pyperclip.copy(hackedMessage)
    else:
        print('Gagal mengenkripsi.')

def findRepeatSequencesSpacings(message):
    # mencari 3 - 5 sekuens huruf berulang dalam string message.
    # me-return dictionary dengan huruf berulang dan list nilai dari jarak antara huruf yang berulang

    # menghilangkan karakter-karakter non-letters dari message
    message = NONLETTERS_PATTERN.sub('', message.upper())

    # perulangan untuk mencari sekuens yang berulang dalam message dan menghitung jaraknya
    seqSpacings = {}
    for seqLen in range(3, 6):
        # loop ini memastikan kita mengiterasi setiap substring yang mungkin dari panjang seqLen dalam string message
        for seqStart in range(len(message) - seqLen):
            # menyimpan sekuens dalam seq
            seq = message[seqStart:seqStart + seqLen]

            # mencari perulangan dari sekuens yang didapat sampai akhir dari string message
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # sekuens huruf berulang ketemu
                    if seq not in seqSpacings:
                        seqSpacings[seq] = [] # inisialisasi list kosong

                    # Append (memasukan) jarak antara kata berulang ke dalam seqSpacing
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings


def getUsefulFactors(num):
    # me-return list dari factor yang kurang dari MAX_KEY_LENGTH

    if num < 2:
        return [] # angka yang kurang dari 2 adalah faktor yang tidak digunakan

    factors = [] # inisialisasi list factor

    # cek integer sampai MAX_KEY_LENGTH
    for i in range(2, MAX_KEY_LENGTH + 1): # 1 tidak termasuk
        if num % i == 0:
            factors.append(i)
            factors.append(int(num / i))
    if 1 in factors:
        factors.remove(1)
    return list(set(factors))


def getItemAtIndexOne(x):
    return x[1]


def getMostCommonFactors(seqFactors):
    # menghitung berapa banyak sebuah faktor ada dalam seqFactors
    factorCounts = {} # key is a factor, value is how often if occurs

    # seqFactors memiliki nilai seperti: {'GFD': [2, 3, 4, 6, 9, 12], 'ALW': [2, 3, 4, 6, ...], ...}
    # dimana nilai int tersebut adalah faktor dari jarak perulangan
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1

    # Meletakan faktor dan banyaknya faktor tsb muncul ke dalam tuple, kemudian dibuat list
    # sehingga bisa diurutkan
    factorsByCount = []
    for factor in factorCounts:
        # menyisihkan faktor yang lebih dari MAX_KEY_LENGTH
        if factor <= MAX_KEY_LENGTH:
            # factorsByCount adalah sebuah list yang berisi tuple: (factor, factorCount)
            # factorsByCount memiliki nilai seperti ini: [(3, 497), (2, 487), ...]
            factorsByCount.append( (factor, factorCounts[factor]) )

    # mengurutkan faktorsByCount berdasarkan faktorCounts dari besar ke kecil
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)

    return factorsByCount


def kasiskiExamination(ciphertext):
    # mencari sekuens dari 3 sampai 5 huruf yang berulang
    # dalam ciphertext. repeatedSeqSpacing memiliki nilai seperti:
    # {'EXG': [192], 'NAF': [339, 972, 633], ... }
    # berbentuk dictionary dengan sekuens huruf yang berulang dan list nilai dari jarak antar sekuens huruf dalam integer

    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)

    # seqFactors menyimpan sekuens kata berulang dan factor dari jaraknya yang didapat dari fungsi getUsefulFactors
    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    # getMostCommonFactors me-return list dari 2 tuple integer (int pertama adalah nilai faktor,
    # yang kedua adalah berapa banyak angka faktor itu muncul dan disimpan dalam factorsByCount
    factorsByCount = getMostCommonFactors(seqFactors)

    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])

    return allLikelyKeyLengths

# untuk memanggil fungsi main
if __name__ == '__main__':
    main()