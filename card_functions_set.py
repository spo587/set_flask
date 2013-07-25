class Card(object):
    def __init__(self,attributes):
        '''Attributes is a tuple of length=card dimension. Each attribute contains 0-2, 
        characteristic of that attribute'''
        self.attributes = attributes
    def getdimension(self):
        return len(self.attributes)

def isset(card1,card2,card3):
    '''Determines if the three given cards are a set.'''
    ans=0
    for i in range(len(card1.attributes)):
        if (card1.attributes[i]+card2.attributes[i]+card3.attributes[i])%3==0:
            ans+=1
    return ans==len(card1.attributes)
    
def makeset(card1,card2):
    '''Given two cards, determine the card needed to make a set.'''
    dimension = card1.getdimension()
    attributes = []
    
    masterset = set([0, 1, 2])
    
    for i in range(dimension):
        used_elements = set()
        used_elements.add(card1.attributes[i])   
        used_elements.add(card2.attributes[i])
    
        if len(used_elements) == 1:
             attributes.append(card1.attributes[i])
        else:
            attributes.append((set.difference(masterset, used_elements).pop()))
    
    card3 = Card(attributes)
    return card3    
            
def issuperset(card1,card2,card3,card4):
    '''detemines whether the four cards are a superset'''
    for i in range(1,4):
        cards = [card1, card2, card3, card4]
        set1 = makeset(cards[0], cards.pop(i)).attributes
        set2 = makeset(cards.pop(), cards.pop()).attributes
        if set1 == set2:
            return True
    return False
       
def settype((card1,card2,card3)):
    '''a function to determine the number of differences in a given set'''
    assert isset(card1,card2,card3) is True
    
    numdiffs = sum([card1.attributes[i]!=card2.attributes[i] \
            for i in range(len(card1.attributes))])

    return numdiffs

