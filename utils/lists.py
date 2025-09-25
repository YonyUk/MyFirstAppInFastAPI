def first(seq,predicate):
    '''
    return the first element of the sequence that verify the predicate

    param:
        seq ---> sequence of elements
    
    param:
        predicate ---> function that recieve a value from the given sequence and return true or false
    '''
    for element in seq:
        if predicate(element):
            return element
    return None

def remove(seq,predicate):
    '''
    remove all elements that verify the predicate from de sequence

    param:
        seq ---> sequence of elements
    
    param:
        predicate ---> function that recieve a value from the given sequence and return true or false
    '''
    return list(_remove(seq,predicate))

def _remove(seq,predicate):
    for element in seq:
        if not predicate(element):
            yield element
