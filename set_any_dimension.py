import math
import random
import card_functions_set as c


## this is set up to play setgames of different types corresponding to different numbers of card attributes or different 'dimensions'

    
#TODO: find a way to generate these on demand (lazy) instead of writing them as seperate functions



def master_list(dim, indices):
    former_indices = indices
    ret = []
    for i in range(3):
        indices = former_indices + (i,)
        if dim == 1:
            ret += [c.Card(indices)]
        else:
            ret += master_list(dim-1, indices)
    return ret


##print print_src_list()


def get_dimension_list(dims):
    return master_list(dims, ()) 


class board(object):
    def __init__(self,dimension,cardsonboard = None,cardsremoved = None):
        ## each of the inputs is a list, except for the dimension
        ## each game board will start with empty lists
        ## dimensionlist will be a global list that we'll input
        self.cardsonboard = [] if cardsonboard == None else cardsonboard
        self.cardsremoved = [] if cardsremoved == None else cardsremoved
        self.dimension = dimension
        self.mastercardlist = get_dimension_list(dimension)
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
