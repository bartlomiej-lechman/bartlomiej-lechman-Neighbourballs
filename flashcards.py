import string
import random


def addCard(filename, question, answer, category, number):
    # filename = 'flashcards.txt'
    # fileptr = open(filename, 'a')
    '''with open('flashcards.txt', 'a') as writer:
        writer.writelines([question, "\t", answer, "\t\t\t\t\t", note, "\t", "\n"])'''
    # fileptr.writelines([question, "\t", answer, "\t\t\t\t\t", note, "\t", "\n"])
    # fileptr.close()
    # return [question, answer, "", "", "", "", note]
    filename.put(str(number), question=question, answer=answer, category=category, hard=50)


def parseline(line):
    wordlist = string.split(line, '\t')
    if len(wordlist) == 1 and wordlist[0] == "":
        return []
    else:
        return wordlist


def readtxt(filename, cardlist):
    card = []
    # open(filename, "a").close()  # touch file
    fileptr = open(filename)
    with open('flashcards.txt', 'r') as reader:
        for line in reader:
            card = parseline(line)

            if len(card) > 0:
                cardlist.append(card)
    # line  = fileptr.read()
    '''for line in fileptr:
        card = parseline(line)
        print "card %s" % card
        if len(card) > 0:
            cardlist.append(card)
    fileptr.close()'''
    return cardlist


def getquestion(card):
    if not card:
        return ""
    return card['question']


def getcategory(card):
    if not card:
        return ""
    return card['kategoria']


def getanswer(card):
    if not card:
        return ""
    return card['answer']


def gettype(card):
    if not card:
        return ""
    return card[2]


def getnotes(card):
    if not card:
        return ""
    return card[6]


def getrandomcard(cardlist):
    '''if len(cardlist) > 0:
        return cardlist[random.randint(0, len(cardlist) - 1)]
    else:
        return []'''
    if len(cardlist) > 0:
        number = str(random.randint(0, len(cardlist) - 1))
        return cardlist.get(number)
    else:
        return


def readcards():
    mycardlist = []
    mycardlist = readtxt('flashcards.txt', mycardlist)
    return mycardlist
