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
    return Card([att0,att1,att2,att3])

## build the image list mapping for the web game
'''TODO: Have each card be able to get its own image src'''
def print_src_list():
    src_list=[]
    for card in fourdmastercardlist():
            src_list.append(cardmapping(card))
            
    return src_list

