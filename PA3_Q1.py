import PySimpleAutomata  
from graphviz import Digraph

def transDiagram():
    
    print('Do you want to creat a diagram for DFA or NFA? Please type NFA or DFA.')
    typeOfFA = input()
    
    if(typeOfFA != 'DFA' and typeOfFA != 'NFA'):
        print('Error input. Exiting program.')
    exit() 
    
    print('Please enter the alphabet symbol and separated by white spaces.')
    alphabetInput = input()
    alphabetInput = alphabetInput.split()
    
    #Creating an array of alphabet symbols
    alphabetArray = []
    
    numOfAlphSymb = len(alphabetInput)
    for i in range(numOfAlphSymb):
        alphabetArray.append(alphabetInput[i])
        
    #Asking the user to enter all the states
    print('Please enter the states separated by white spaces.')
    statesInput = input()
    statesInput = statesInput.split()
    numOfInputStates = len(statesInput)

    #Asking the user to enter the start state
    print('Please enter the Start state out of the list you entered.')
    startState = input()

    #Asking the user to enter the final state / states
    print('Please enter the Final state or states out of the list you entered.')
    print('If there are several Final states, separate them by white spaces.')
    finalStates = input()
    
    #For each state, creating a node in the diagram and a row in the table
    #Creating a class for a diagram
    dot = Digraph()
    updatedStatesInput = []
    
    for i in range(numOfInputStates):
        if ((startState == statesInput[i]) and (startState in finalStates)):
            #creat a node named fake and label is invisbleState
            dot.node('Fake', 'invisbleState', style = 'invisible') 
            dot.node(startState, startState, root = 'true', shape = 'doublecircle')
            dot.edge('Fake', startState, style = 'bold')
            
            updatedStatesInput.append('->*' + statesInput[i])
            
        elif(startState == statesInput[i]):
            dot.node('Fake', 'invisbleState', style = 'invisible')
            dot.node(startState, startState, root = 'true')
            dot.edge('Fake', startState, style = 'bold')
            
            updatedStatesInput.append('->' + statesInput[i])
            
        elif(statesInput[i] in finalStates):
            dot.node(statesInput[i], statesInput[i], shape = 'doublecircle')
            
            updatedStatesInput.append('*' + statesInput[i])
            
        else:
            dot.node(statesInput[i], statesInput[i])
            
            updatedStatesInput.append(statesInput[i])
            
    #Creating the FA diagram
    for i in range(numOfInputStates):
        print('Entering input for row '+ str(updatedStatesInput[i]) + ':')
        
        localList = []
        
        for j in range(numOfAlphSymb):
            
            print('Please enter an input for alphabetical symbol '+ str(alphabetArray[j]) + '.')
            print('If there are several states for one cell, separate them by commas, do not use whitespace.')
            print('If there are no transiton states in the cell, indicate it by 0')
            
            localInput = input()
            
            if (typeOfFA == 'DFA'):
                localList.append(localInput)
            else:
                localList.append('{' + localInput + '}')
                
            if (',' in localInput):
                state_list = []
                state_list = localInput.split(',')
                for k in range(len(state_list)):
                    dot.edge(str(statesInput[i]), state_list[k], label = str(alphabetArray[j]))
                    
            elif (localInput != '0'):
                dot.edge(str(statesInput[i]), localInput, label = str(alphabetArray[j]))
                

    return dot.render('FA_diagram.gv', view=True) 

var = transDiagram()
print(var)



