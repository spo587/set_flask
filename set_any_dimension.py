import math
import random


## this is set up to play setgames of different types corresponding to different numbers of card attributes or different 'dimensions'

class card(object):
    def __init__(self,attributes):
        '''attributes is a tuple of length=card dimension'''
        self.attributes = attributes
    def getdimension(self):
        return len(self.attributes)
    def printcard(self):
        return self.attributes

def isset(card1,card2,card3):
    '''determines if the three given cards are a set'''
    ans=0
    for i in range(len(card1.attributes)):
        if (card1.attributes[i]+card2.attributes[i]+card3.attributes[i])%3==0:
            ans+=1
    return ans==len(card1.attributes)
    
def makeset(card1,card2):
    '''given two cards, determine the card needed to make a set'''
    dimension = card1.getdimension()
    attributes = []
    
    masterset = set([0, 1, 2])
    
    for i in range(dimension):
        used_elements = set()
        current1 = card1.attributes[i] 
        current2 = card2.attributes[i]
        used_elements.add(current2)   
        used_elements.add(current1)
    
        if len(used_elements) == 1:
             attributes.append(current1)
        else:
            attributes.append((set.difference(masterset, used_elements).pop()))

        
    card3 = card(attributes)
    return card3    
            
    
    
def issuperset(card1,card2,card3,card4):
    '''detemines whether the four cards are a superset'''
    if makeset(card1,card2).attributes == makeset(card3,card4).attributes\
    or makeset(card2,card3).attributes == makeset(card1,card4).attributes\
    or makeset(card1,card3).attributes == makeset(card2,card4).attributes:
        return True
    return False
       

def settype((card1,card2,card3)):
    '''a function to determine the number of differences in a given set'''
    assert isset(card1,card2,card3) is True
    numdiffs=0
    for i in range(len(card1.attributes)):
        if card1.attributes[i]!=card2.attributes[i]:
            numdiffs+=1
    return numdiffs
    
'''TODO: find a way to generate these on demand (lazy) instead of writing them as seperate functions'''

def twodmastercardlist():
    '''creates a list of all nine two-dimensional cards'''
    mastercardlist=[]
    for i in range(3):
        for j in range(3):
            mastercardlist.append(card((i,j)))
    return mastercardlist

  
    
def threedmastercardlist():
    '''list of all 27 three d cards'''
    threedmastercardlist=[]
    for i in range(3):
        for j in range(3):
            for t in range(3):
            
                threedmastercardlist+=[card((i,j,t)),]
    return threedmastercardlist

def fourdmastercardlist():
    '''list of all 81 4-d cards, for a standard game'''
    fourdmastercardlist=[]
    for i in range(3):
            for j in range(3):
                for t in range(3):
                    for n in range(3):
                        fourdmastercardlist+=[card((n,t,j,i)),]
    #random.shuffle(fourdmastercardtuple)
    return fourdmastercardlist


def cardmapping(card):
    '''converts each card to a number 0-80'''
    cardsum = 0
    for i in xrange(len(card.attributes)):
        cardsum += card.attributes[i] * (3 ** i)
    return cardsum

def reversecardmapping(num):
    '''do this better!!'''
    att3 = num/27
    att2 = (num - 27) / 9
    att1 = (num - 27 - 9) / 3
    att0 = (num - 27 - 9 - 3) 
    return card([att0,att1,att2,att3])

## build the image list mapping for the web game
'''TODO: Have each card be able to get its own image src'''
def print_src_list():
    src_list=[]
    for card in fourdmastercardlist():
            src_list.append(cardmapping(card))
            
    return src_list

##print print_src_list()

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

def getDimensionList(dims):
    if dims == 2:
        return twodmastercardlist()
    elif dims == 3:
        return threedmastercardlist()
    elif dims == 4:
        return fourdmastercardlist()
    else:
        return False


class board(object):
    def __init__(self,dimension,cardsonboard = None,cardsremoved = None):
        ## each of the inputs is a list, except for the dimension
        ## each game board will start with empty lists
        ## dimensionlist will be a global list that we'll input
        self.cardsonboard = [] if cardsonboard == None else cardsonboard
        self.cardsremoved = [] if cardsremoved == None else cardsremoved
        self.dimension = dimension
        self.mastercardlist = getDimensionList(dimension)
        ## shuffle the cardlist at the beginning of each game
        self.cardlist = self.mastercardlist[:]

    def dealcards(self,numcards): # TODO check for empty deck! (Complicated)
        '''a random deal that adds numcards cards to the existing board'''
        for i in xrange(numcards):
            selectedcard = random.choice(self.cardlist)
            self.cardsonboard.append(selectedcard)
            self.cardlist.remove(selectedcard)
   
    def clearboard(self):
        self.cardsonboard = []
       
    def isthereaset(self):
        for t in threecardcombos(len(self.cardsonboard)):
            if isset(self.cardsonboard[t[0]],self.cardsonboard[t[1]],self.cardsonboard[t[2]]):
                return True
        return False
        
    ## take away the first set found
    def detectsetandremove(self):
        for t in threecardcombos(len(self.cardsonboard)):

            card1 = self.cardsonboard[t[0]]
            card2 = self.cardsonboard[t[1]]
            card3 = self.cardsonboard[t[2]]
            
            if isset(card1,card2,card3) is True:
                
                
                
                ## uncomment print statements to see the game as it progresses in
                ## the playgame() function below
                print 'set!'
                print card1.attributes
                print card2.attributes
                print card3.attributes
                self.cardsonboard.remove(card1)
                self.cardsonboard.remove(card2)
                self.cardsonboard.remove(card3)
                self.cardsremoved += [card1,card2,card3,]
                
                break

    def detectsetandremoveadvanced(self):
        '''removes sets preferentially with the lowest number of differences instead of the first set detected'''
        i=1
        while i<=self.dimension:
            for t in threecardcombos(len(self.cardsonboard)):
                card1=self.cardsonboard[t[0]]
                card2=self.cardsonboard[t[1]]
                card3=self.cardsonboard[t[2]]
               
                
                if isset(card1,card2,card3) is True and settype((card1,card2,card3))==i:
                    #print 'set!'
##                    print card1.attributes
##                    print card2.attributes
##                    print card3.attributes
                    self.cardsonboard.remove(card1)
                    self.cardsonboard.remove(card2)
                    self.cardsonboard.remove(card3)
                    self.cardsremoved+=[card1,card2,card3,]
                    return 'not deadboard'
                
            i+=1
                
    ## find the number of sets on the board (without removal)
    def numsetsonboard(self):
        ans=0
        for t in threecardcombos(len(self.cardsonboard)):
            if isset(self.cardsonboard[t[0]],self.cardsonboard[t[1]],self.cardsonboard[t[2]]):
                ans+=1
        return ans
    ## this might be unnecessary

    def printsetsonboard(self):
        '''specifies all the sets on the board'''
        listofsets = []
        for t in threecardcombos(len(self.cardsonboard)):
            if isset(self.cardsonboard[t[0]],self.cardsonboard[t[1]],self.cardsonboard[t[2]]):
                # print 'set!'
                #                                                 print self.cardsonboard[t[0]].attributes
                #                                                 print self.cardsonboard[t[1]].attributes
                #                                                 print self.cardsonboard[t[2]].attributes
                listofsets += [cardmapping(self.cardsonboard[t[0]]),cardmapping(self.cardsonboard[t[1]]),cardmapping(self.cardsonboard[t[2]]),]
        return listofsets
    
    def printsupersetsonboard(self):
        listofsupersets = []
        for t in fourcardcombos(len(self.cardsonboard)):
            
            if issuperset(self.cardsonboard[t[0]],self.cardsonboard[t[1]],self.cardsonboard[t[2]],self.cardsonboard[t[3]]):
                
                listofsupersets += [cardmapping(self.cardsonboard[t[0]]),cardmapping(self.cardsonboard[t[1]]),cardmapping(self.cardsonboard[t[2]]),cardmapping(self.cardsonboard[t[3]]),]
        return listofsupersets

    ## what cards are on the current board
    def printboard(self):
        for i in range(len(self.cardsonboard)):
            print self.cardsonboard[i].attributes

def playgame(dimension,detectiontype):
    '''function to play a game with cards of specified dimension and detection type
    dimension=int
 
    detectiontype=str: 'simple' or 'complex
    uncomment print statements to see the game as it goes. leave them in to return only the number
    of deadboards'''
    numsets = 0
    deadboards = 0
    board1 = board(dimension)
    board1.dealcards(dimension * 3)
    print 'board=', board1.printboard()
    while len(board1.cardlist) >= 0:
        if board1.isthereaset():
            if detectiontype == 'simple':
                board1.detectsetandremove() #TODO have this return a variable (False if there is a dead board)
            elif detectiontype=='complex':
                board1.detectsetandremoveadvanced() #TODO this too!
            numsets+=1
            print "Num sets: ", numsets
            if len(board1.cardlist)>=3:
                board1.dealcards(3)
            print 'board=', board1.printboard()
            
            
        elif len(board1.cardlist)>=3:
            deadboards+=1
            print 'deadboard'
            board1.dealcards(3)
            print 'new board=', board1.printboard()
            
            
        else:
            print 'game over!'
            print 'total number of sets in game=',numsets
            break
##    
    print 'game over!'
    print 'final board=',board1.printboard()
    if len(board1.cardsonboard)>=12:
        deadboards+=1
    print "Num cards on board: ", len(board1.cardsonboard)
    print "Num cards removed: ", len(board1.cardsremoved)
    print "Num cards left in deck: ", len(board1.cardlist)
    print 'number of sets: ', numsets
    print 'number of deadboards: ',deadboards

## below, some functions to test some statistics/mathy stuff   
         
def randomdealdeadboards(numcards,numtrials,dimension):
    
    numdeadboards=0
    for i in range(numtrials):
        #print 'new board'
        board2=board([],[],dimension,dimensionlist)
        #print board2.cardlist
        board2.dealcards(numcards)
        #board2.printboard()
        
        if board2.isthereaset() is False:
            #print 'deadboard!!'
            numdeadboards+=1
            print board2.printboard()
    return numdeadboards



def deadboards(numgames,detectiontype):
    '''returns a list with the number of deadboards in a number of games of a certain type'''
    listofdeadboards=[]
    for i in range(numgames):
        listofdeadboards.append(playgame(4,detectiontype))
        ## i've left the print statement in below at an attempt to debug...you'll see what happens
        ## the program works for a while, then it just stops all of a sudden
        print listofdeadboards
    return listofdeadboards

def average(x):
    return sum(x)/float(len(x))
    
    
if __name__ == '__main__':
    playgame(4,'simple')
