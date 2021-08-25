import PySimpleAutomata  
from graphviz import Digraph

class NFA:
    def __init__(self):
        self.states = []
        self.alphabets = []
        self.final_states = []
        self.start_state = []
        self.transition_functions = []    
    
    def construct_nfa_from_txtFile(self, lines):
        self.alphabets = str(lines[0]).split()
        self.states = str(lines[1]).split()
        self.start_state = str(lines[2]).split()
        self.final_states = str(lines[3]).split()
        
        for i in range(4, len(lines)):
            transition_fun_line = lines[i].split()
            
            starting_state = transition_fun_line[0]
            transition_alphabet = transition_fun_line[1]
            ending_state = transition_fun_line[2]
            
            transition_function = (starting_state, transition_alphabet, ending_state)
            self.transition_functions.append(transition_function)  
            
    def printNFA(self):
        print('Below is the input NFA: ')
        print('The alphabet is: ')
        print(self.alphabets)
        print('The input states are: ')
        print(self.states)
        print('The Start state is: ')
        print(self.start_state)
        print('The Final state is: ')
        print(self.final_states)
        print('The Transistion Function are: ')
        print(self.transition_functions)
   

class DFA:
    def __init__(self):
        self.states = []
        self.alphabets = []
        self.final_states = []
        self.final_states2 = []
        self.start_state = []
        self.transition_functions = [] 
        self.transition_functions2 = [] 
        self.q = []
    
    def convert_from_nfa(self, nfa):
        self.alphabets = nfa.alphabets
        self.start_state = nfa.start_state 
        
        nfa_transition_dict = {}
        dfa_transition_dict = {}
        
        # Combine NFA transitions
        
        for transition in nfa.transition_functions:
            starting_state = transition[0]
            transition_alphabet = transition[1]
            ending_state = transition[2]
            
            if (starting_state, transition_alphabet) in nfa_transition_dict: #it should be false at the begining bc of empty dic
                nfa_transition_dict[(starting_state, transition_alphabet)].append(ending_state)
            else:
                nfa_transition_dict[(starting_state, transition_alphabet)] = [ending_state]
            
        self.q.append((start_state,))
    
        # Convert NFA transitions to DFA transitions
        for dfa_state in self.q:
            for alphabet in nfa.alphabets:
                if len(dfa_state) == 1 and (dfa_state[0], alphabet) in nfa_transition_dict:
                    dfa_transition_dict[(dfa_state, alphabet)] = nfa_transition_dict[(dfa_state[0], alphabet)]
                    
                    if tuple(dfa_transition_dict[(dfa_state, alphabet)]) not in self.q:
                        self.q.append(tuple(dfa_transition_dict[(dfa_state, alphabet)]))
                else:
                    destinations = []
                    final_destination = []
                    
                    for nfa_state in dfa_state:
                        if (nfa_state, alphabet) in nfa_transition_dict and nfa_transition_dict[(nfa_state, alphabet)] not in destinations:
                            destinations.append(nfa_transition_dict[(nfa_state, alphabet)])
                    
                    if not destinations:
                        final_destination.append(None)
                    else:  
                        for destination in destinations:
                            for value in destination:
                                if value not in final_destination:
                                    final_destination.append(value)
                        
                    dfa_transition_dict[(dfa_state, alphabet)] = final_destination
                        
                    if tuple(final_destination) not in self.q:
                        self.q.append(tuple(final_destination))
                        
        # Convert NFA states to DFA states            
        for key in dfa_transition_dict:
            a = str((tuple(key[0])))
            b = str(key[1])
            c = str(tuple(dfa_transition_dict[key]))
            self.transition_functions.append(a + b + c)
            #print(self.transition_functions)
        
        for key in dfa_transition_dict:
            self.transition_functions2.append(('q' + str(self.q.index(tuple(key[0]))), key[1], 
                                              'q' + str(self.q.index(tuple(dfa_transition_dict[key])))))
            
           
        for q_state in self.q:
            for nfa_final_state in nfa.final_states:
                if nfa_final_state in q_state:
                    self.final_states = q_state
                    
        for q_state in self.q:
            for nfa_final_state in nfa.final_states:
                if nfa_final_state in q_state:
                    self.final_states2.append("q" + str(self.q.index(q_state)))
                    
       
        '''
        firstNode = []
        dg = []
        secondNode = []
        updatedStatesInput = []
        dot = Digraph()
        for key in dfa_transition_dict:
            firstNode.append(('q' + str(self.q.index(tuple(key[0])))))
            dg.append(key[1])
            secondNode.append('q' + str(self.q.index(tuple(dfa_transition_dict[key]))))
            
        numOfInputStates = len(firstNode)
        
        for i in range(numOfInputStates):
            if (a in firstNode[i]) and (a == b):
                print('1')
                dot.node('Fake', 'q', style = 'invisible')
                dot.edge('Fake', a, style = 'bold')
                dot.node(a, a, root = 'true', shape = 'doublecircle')
                updatedStatesInput.append('->*' + firstNode[i])
            elif(a in firstNode[i]):
                # print('2'）
                dot.node('Fake', 'q', style = 'invisible')
                dot.edge('Fake', a, style = 'bold')
                dot.node(a, a, root = 'true')
                updatedStatesInput.append('->' + firstNode[i])
            elif(firstNode[i] in b):
                print('3')
                dot.node(firstNode[i], firstNode[i], shape = 'doublecircle')
                updatedStatesInput.append('*' + firstNode[i])
            else:
                #print('4')
                dot.node(firstNode[i], firstNode[i])
                updatedStatesInput.append(firstNode[i])
                
        dot.edge(updatedStatesInput[0],secondNode[0],label = str(dg[0]))
        dot.node('Fake', 'q', style = 'invisible')
        dot.edge('Fake', updatedStatesInput[0], style = 'bold')
        dot.node(updatedStatesInput[0], updatedStatesInput[0], root = 'true')
        
        dot.edge(updatedStatesInput[1],secondNode[1],label = str(dg[1]))
        dot.edge(updatedStatesInput[2],secondNode[2],label = str(dg[2]))
        dot.edge(updatedStatesInput[3],secondNode[3],label = str(dg[3]))
        dot.edge(updatedStatesInput[4],secondNode[4],label = str(dg[4]))
        dot.edge(updatedStatesInput[5],secondNode[5],label = str(dg[5]))'''
        
        #draw pic
        firstNode = []
        secondNode = []
        transtEdge = []

        for key in dfa_transition_dict:
            a = str((tuple(key[0])))
            b = str(key[1])
            c = str(tuple(dfa_transition_dict[key]))
            self.transition_functions.append(a + b + c)
            #print(transition_functions)
            firstNode.append(a)
            secondNode.append(c)
            transtEdge.append(b)
        dot = Digraph()
        dot.node('Fake', 'q', style = 'invisible')
        dot.edge('Fake', firstNode[0], style = 'bold')
        dot.node(firstNode[0], firstNode[0], root = 'true')
        dot.edge(firstNode[0], secondNode[0], label = transtEdge[0])
        dot.edge(firstNode[1], secondNode[1], label = transtEdge[1])
        dot.edge(firstNode[2], secondNode[2], label = transtEdge[2])
        dot.edge(firstNode[3], secondNode[3], label = transtEdge[3])
        dot.edge(firstNode[4], secondNode[4], label = transtEdge[4])
        dot.edge(firstNode[5], secondNode[5], label = transtEdge[5])
        dot.node(firstNode[5], firstNode[5], shape = 'doublecircle')
         
        return dot.render('FA_diagram1.gv', view=True) 
            
    
    def print_dfa(self):
        print('Below is DFA: ')
        print('The alphabet is: ')
        print(' '.join(self.alphabets))
        print('The new states are: ')
        print(self.q)
        print('The final state is: ')
        print(self.final_states)
        print('The Start state is: ')
        print(self.start_state)   
        print('The Transistion Function are: ')
        for a in self.transition_functions:
            print(a)
        print('-----------------')
        print('Another Transistion Function are: ')   
        for b in self.transition_functions2:
            print(b)
        print('In this transition, the final state is: ')   
        print(self.final_states2)

        
        

file = open('NFA_Input.txt', 'r')

lines = file.readlines()



nfa = NFA()
dfa = DFA()
nfa.construct_nfa_from_txtFile(lines)
dfa.convert_from_nfa(nfa)

nfa.printNFA()
print('-----------------')
print('-----------------')
dfa.print_dfa()
        