'''
Open Combat Flow - enforce.py
@purpose Enforces the format of blocks and dice strings.
@author Owen Mellema
@date 2-25-19
'''
import opencombatflow.character as c

'''
ENFORCEMENT BLOCK
    (NOTE)
    I decided not to add this to the DSD, because 1). It is only relevant for the purpose of rapid development of protocol enforcement, and 2). It has a list as the top level structure, not a dictionary.

    (LIST)
    At the top level, the enforcementBlock is a list. Each element of the list corresponds to an element specified by the DSD. At each index in the list, there is a dictionary detailing information about the elemtn, as defined below.
        (MANDATORY)
        "name": The name of the key. (string)
        "type": The type of the element at the key. This can be a type (eg, 'int', 'str', etc.) or a string, specifying a specific type of block.

        (CONDITIONALLY MANDATORY)
        "dictElement": What type of element each key in a dictionary must be of. Only nessesary if "type" is dict.

        (NON-MANDATORY)
        "mandatory": If true, this key must be present. Otherwise, or if it not provided, it is assumed to be non-mandatory.
'''
blockContext = {}
def enforce(blockToCheck, blockType):
    '''
    Enforce rules for the given blockType. blockType is a string.
    If blockType =:
    -"action" test actionBlock
    -"range" test rangeBlock
    -"reaction" test reactionBlock
    -"damage" test damageBlock
    -"log" test logBlock
    @param blockToCheck The block to check.
    @param blockType The type of block the blockToCheck should be.
    @raise KeyError If there is a syntax error with the block.
    '''

    global actionBlockPrototype, rangeBlockPrototype, reactionBlockPrototype, damageBlockPrototype
    global blockContext

    blockContext = blockToCheck

    if blockType == 'action':
        _enforceHelper(blockToCheck, actionBlockPrototype)
    elif blockType == 'range':
        _enforceHelper(blockToCheck, rangeBlockPrototype)
    elif blockType == 'reaction':
        _enforceHelper(blockToCheck, reactionBlockPrototype)
    elif blockType == 'damage':
        _enforceHelper(blockToCheck, damageBlockPrototype)
    elif blockType == 'log':
        #Do log testing. This requires a different kind of check.
        assert 'messageType' in blockToCheck
        assert type(blockToCheck['messageType']) == str
        messageType = blockToCheck['messageType']
        required = []
        if messageType ==  'startOfTurn':
            required = ['character']
        elif messageType ==  'action':
            required = ['action']
        elif messageType ==  'attackHit':
            required = ['action', 'damage']
        elif messageType ==  'attackFailure':
            required = ['action']
        elif messageType ==  'reaction':
            required = ['action', 'reaction']
        elif messageType ==  'death':
            required = ['action', 'character']
        else:
            raise KeyError(f"Message Type {messageType} is not valid. (Evaluating {blockContext})")
        
        #Check to make sure all required keys are present.
        for i in required:
            if i not in blockToCheck:
                raise KeyError(f"Message Type {messageType} requires key {i} (Evaluating {blockContext})")
        

def _enforceDiceString(diceString):
    '''
    PRIVATE: Makes sure the dice string is a valid dice string.
    '''
    if type(diceString)==int:
	    return

    condChar = ""
    if ">" in diceString:
        condChar = ">"
    elif "<" in diceString:
        condChar = "<"
    elif "=" in diceString:
        condChar = "="
    else:
        _evaluateDiceStringHelper(diceString)
        return

    #Get values before and after the conditional.
    _evaluateDiceStringHelper(diceString.split(condChar)[0])
    _evaluateDiceStringHelper(diceString.split(condChar)[1])

def _evaluateDiceStringHelper(diceString):
    '''
    PRIVATE: Helps with _evaluateDiceString. Enforces dice string without conditionals.
    '''
    #Convert all "-" into "+-"
    diceStringReady = "+-".join(diceString.split('-'))

    #Evaluate the new string.
    for statement in diceStringReady.split('+'):
        #See if the statement is a dice statement, by testing if there is a 'd' in it.
        if "d" in statement:
            try:
                before_d = int(statement.split('d')[0]) #This will cause an error if it cannot be converted to int
                after_d = int(statement.split('d')[0]) #This will cause an error if it cannot be converted to int
            except:
                raise KeyError(f"Invalid Syntax for Dice String {diceString}")
            assert len(statement.split('d')) == 2, "Dice statements must by of the form xdy, where x and y are integers."
        elif statement == "":
            continue
        else: #Otherwise, we assume that it is a constant.
            try:
                int(statement) #This will cause an error if it cannot be converted to int
            except:
                raise KeyError(f"Invalid Syntax for Dice String {diceString}")
	
def _enforceType(toCheck, requestedType, dictElement = None):
    '''
    PRIVATE: Checks to make sure that variables match specifications for types. Depending upon the value of requestedType, this has different tests that it performs:
    -If requestedType is a Type, it will check to make sure that toCheck is of that type.
    -If requestedType is a Type of dict, and dictElement is not None, raise an error if each element of the dictionary is not of dictElement.
    -If requestedType is a string equal to "DS", it makes sure that toCheck is a valid dice string.
    -If requestedType is any string besides "DS", it checks that toCheck is a valid block of the type requestedType.
    '''
    global blockContext
    if type(requestedType) == type: #If we are doing a check of a 'normal' variable test. (IE, not specified by a string.) We tell this by seeing if requestedType is of type type, or of type string
        if not issubclass(type(toCheck), requestedType): #See if the types match. The "issubclass" function determines if toCheck has a parent of requestedType 
            raise KeyError(f"The element {toCheck} is of type {type(toCheck)}, not of required type {requestedType}. (Evaluating {blockContext})") #If they don't match, raise an error.
        if requestedType == dict and dictElement is not None: #If the type is a dictionary, run additional testing of the given dictionary.
            for internalKey in toCheck: #Check each individual key in the dictionary.
                _enforceType(toCheck[internalKey], dictElement) #Test each element.
    elif type(requestedType) == str: #If the requestedType is a string, perform special testing, including block and dicestring, as specified by the string.
        if requestedType == "DS": #If requested type is 'DS', we enforce the dice string.
            _enforceDiceString(toCheck)
        else: #If it is not 'DS', we assume that it is a specification of a block, and we let enforce take care of it.
            enforce(toCheck, requestedType)

def _enforceHelper(blockToCheck, enforcementBlock):
    '''
    PRIVATE: This is to enforce protocols using a pre-determined enforcement block. Please use an appropriate front-end channel to access this functionality.
    '''
    global blockContext

    for keyToCheck in enforcementBlock:
        #Check if mandatory elements are present.
        keyName = keyToCheck['name']
        if keyToCheck.get('mandatory', False) == True and keyName not in blockToCheck:
            raise KeyError(f"The Key {keyName} must be present in this block. (Evaluating {blockContext})")
        elif keyName not in blockToCheck:
            continue

        #Check if given values were consistent with required values.
        element = blockToCheck[keyName]
        _enforceType(element, keyToCheck['type'], dictElement=keyToCheck['dictElement'] if 'dictElement' in keyToCheck else None)
    
#Prototypes
actionBlockPrototype = [
    {
        'name': 'range',
        'type': 'range',
        'mandatory': True,
    },
    {
        'name': 'user',
        'type': c.Character,
        'mandatory': True,
    },
    {
        'name': 'name',
        'type': str,
        'mandatory': True,
    },
    {
        'name': 'damage',
        'type': dict,
        'dictElement': 'DS'
    },
    {
        'name': 'effect',
        'type': dict,
        'dictElement': 'DS'
    },
    {
        'name': 'chance',
        'type': 'DS',
    },
    {
        'name': 'failureCondition',
        'type': 'action',
    }, 
]

rangeBlockPrototype = [
    {
        'name': 'center',
        'type': int,
    },
    {
        'name': 'range',
        'type': int,
    },
    {
        'name': 'group',
        'type': str,
    },
    {
        'name': 'character',
        'type': c.Character,
    },
]

reactionBlockPrototype = [
    {
        'name': 'user',
        'type': c.Character,
        'mandatory': True
    },
    {
        'name': 'name',
        'type': str,
    },
    {
        'name': 'resistance',
        'type': dict,
        'dictElement': 'DS'
    },
    {
        'name': 'action',
        'type': 'action',
    },
]

damageBlockPrototype = [
    {
        'name': 'damageTaken',
        'type': int
    },
    {
        'name': 'effects',
        'type': dict,
        'dictElement': int
    },
]