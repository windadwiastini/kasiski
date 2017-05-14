
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    myMessage = """Alan Mathison Turing was a British mathematician, logician, cryptanalyst, and computer scientist. He was highly influential in the development of computer science, providing a formalisation of the concepts of "algorithm" and "computation" with the Turing machine. Turing is widely considered to be the father of computer science and artificial intelligence. During World War II, Turing worked for the Government Code and Cypher School (GCCS) at Bletchley Park, Britain's codebreaking centre. For a time he was head of Hut 8, the section responsible for German naval cryptanalysis. He devised a number of techniques for breaking German ciphers, including the method of the bombe, an electromechanical machine that could find settings for the Enigma machine. After the war he worked at the National Physical Laboratory, where he created one of the first designs for a stored-program computer, the ACE. In 1948 Turing joined Max Newman's Computing Laboratory at Manchester University, where he assisted in the development of the Manchester computers and became interested in mathematical biology. He wrote a paper on the chemical basis of morphogenesis, and predicted oscillating chemical reactions such as the Belousov-Zhabotinsky reaction, which were first observed in the 1960s. Turing's homosexuality resulted in a criminal prosecution in 1952, when homosexual acts were still illegal in the United Kingdom. He accepted treatment with female hormones (chemical castration) as an alternative to prison. Turing died in 1954, just over two weeks before his 42nd birthday, from cyanide poisoning. An inquest determined that his death was suicide; his mother and some others believed his death was accidental. On 10 September 2009, following an Internet campaign, British Prime Minister Gordon Brown made an official public apology on behalf of the British government for "the appalling way he was treated." As of May 2012 a private member's bill was before the House of Lords which would grant Turing a statutory pardon if enacted."""
    myKey = 'LEMON'
    myMode = 'encrypt' # set 'encrypt' atau 'decrypt'

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)

    print('%sed message:' % (myMode.title()))
    print(translated)
    # pyperclip.copy(translated)
    print()


def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')


def translateMessage(key, message, mode):
    translated = [] # menyimpan string pesan yang di enkripsi/dekripsi

    keyIndex = 0
    key = key.upper()

    for symbol in message: # perulangan tiap karakter pada pesan
        num = LETTERS.find(symbol.upper())
        if num != -1: # -1 berarti symbol.upper() tidak ditemukan dalam LETTER
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex]) # tambah jika enkripsi
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex]) # kurang jika dekripsi

            num %= len(LETTERS) # handle the potential wrap-around

            # menambahkan simbol yang dienkripsi/dekripsi ke akhir kata
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            keyIndex += 1 # pindah ke huruf selanjutnya dari kunci
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # Jika simbol tidak ada dalam LETTERS, maka diterjemahkan sbg simbol tsb
            translated.append(symbol)

    return ''.join(translated)


if __name__ == '__main__':
    main()