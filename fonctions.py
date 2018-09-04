# Functions ##########################################

def index_to_question(indexes):
    #Takes a list of indexes and returns question labels
    L = []
    for index in indexes:
        L.append('Q'+str(index+1))
    return L
