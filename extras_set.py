def threecardcombos(numcardsonboard):
    '''returns list of tuples for all possible threecard combinations given a number of cards, where each tuple is a possible combination of three cards
    numcardsonboard=int
    returns: list of tuples'''
    listofthreecardcombos=[]
    for i in range(numcardsonboard-2):
        for j in range(i+1,numcardsonboard-1):
            for k in range(j+1,numcardsonboard):
                listofthreecardcombos.append((i,j,k))
    return listofthreecardcombos


def fourcardcombos(numcards):
    '''samesies for four cards. we'll want this for superset'''
    listoffourcardcombos=[]
    for i in range(numcards-3):
        for j in range(i+1,numcards-2):
            for k in range(j+1,numcards-1):
                for t in range(k+1,numcards):
                    listoffourcardcombos.append((i,j,k,t))
    return listoffourcardcombos

