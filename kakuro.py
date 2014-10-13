'''
Created on 18 Dec 2011

@author: Lelouch
'''
from csp import *
from utils import *
from csp_search import *
from input_puzzles import *

import time

#Kakuro Problem
class Kakuro(CSP):
    """
    classdocs
    """
    def __init__( self, sel ):
        """
        Constructor
        """
        numbers = list( range(1,10) )
        
        self.puzzles = []
        self.node_list = []
        self.puzzles.append( puzzle0 )
        self.puzzles.append( puzzle1 )
        self.puzzles.append( puzzle2 )
        self.puzzles.append( puzzle3 )
        self.puzzles.append( puzzle4 )
        self.down_rules_dict = DefaultDict( [] )
        self.right_rules_dict = DefaultDict( [] )
        self.selected_puzzle = self.puzzles[sel]
        
        self.has_conflict_calls = 0
        self.nodes_counter = 0
        neighbors = self.parse_neighbours()
        variables_list = neighbors.keys()
        variables_list.sort()
        domain=dict()    
        for i in variables_list:
            domain[i] = numbers[:]
        
        CSP.__init__(self, variables_list, domain, neighbors, self.has_conflict)        

    #Parsing twn geitonikwn variables    
    def parse_neighbours( self ):
        board_height = len( self.selected_puzzle )
        board_length = len( self.selected_puzzle[0] )
        
        current_row = 0
        current_column = 0
        dict1 = DefaultDict( [] )
        
        for row in self.selected_puzzle:
            current_column = 0 
            for column in row:
                                
                if ( isinstance( column, list ) ):                                                         #An vrei kanona a8roismatow
                        if ( column[0] != '' ):                                                            #An einai ka8etos kanonas a8roismatos
                            for i in range( current_row+1, board_height ):                                 #Koitaei olous ta apo katw kelia
                                neighbours_list = []
                                    
                                if ( self.selected_puzzle[i][current_column] == '_' ):                     #Kai otan vriskei variable 
                                    self.down_rules_dict[(i,current_column)] = column[0]
                                    
                                    if ( ( ( i, current_column ) in dict1.keys() ) == False ):             #An dn uparxei hdh sto le3iko 
                                        for j in range( current_column-1, 0, -1 ):                         #Vriskei olous tous geitones ths se stavro
                                            if ( self.selected_puzzle[i][j] == '_' ):
                                                neighbours_list.append( (i,j) )
                                            else:
                                                break
                                               
                                        for j in range( current_column+1, board_length ):
                                            if ( self.selected_puzzle[i][j] == '_' ):
                                                neighbours_list.append( (i,j) )
                                            else: 
                                                break
                                                
                                        for k in range( i-1, 0, -1 ):
                                            if ( self.selected_puzzle[k][current_column] == '_' ):
                                                neighbours_list.append( (k,current_column) )
                                            else:
                                                break
                                            
                                        for k in range( i+1, board_height ):
                                            if ( self.selected_puzzle[k][current_column] == '_' ):
                                                neighbours_list.append( (k,current_column) )
                                            else: 
                                                break
                                    
                                        dict1[(i,current_column)] = neighbours_list
                                
                        if ( column[1] != '' ):                                                                 #Omoiws an vrei orizontio kanona a8roismatos
                            
                                for i in range( current_column+1, board_length ):
                                    neighbours_list = []
                                    
                                    if ( self.selected_puzzle[current_row][i] == '_' ):
                                        self.right_rules_dict[(current_row,i)] = column[1]
                                        if ( ( ( current_row, i ) in dict1.keys() ) == False ):
                                    
                                            for k in range( i - 1, 0, -1 ):
                                                if ( self.selected_puzzle[current_row][k] == '_' ):
                                                    neighbours_list.append( (current_row,k) )
                                                else:
                                                    break
        
                                            for k in range( i + 1, board_length ):
                                                if ( self.selected_puzzle[current_row][k] == '_' ):
                                                    neighbours_list.append( (current_row,k) )
                                                else: 
                                                    break                                                                                 
                                                
                                            for j in range( current_row - 1, 0, -1 ):
                                                if ( self.selected_puzzle[j][i] == '_' ):
                                                    neighbours_list.append( (j,i) )
                                                else:
                                                    break
                                                    
                                            for j in range( current_row+1, board_height ):
                                                if ( self.selected_puzzle[j][i] == '_' ):
                                                    neighbours_list.append( (j,i) )
                                                else: 
                                                    break
                                        
                                            dict1[(current_row, i)] = neighbours_list
                                        
                current_column += 1
            current_row += 1
        return dict1      
    
    #Elegxei an mporei na sxhmatistei to sum_remainder apo kapoia upolista ths listas availables h opoia exei mege8os = me unassigned_neighbors
    def check_for_possible_sum( self, sum_remainder, unassigned_neighbors, availables ):              
            f = lambda x: [[y for j, y in enumerate(set(x)) if (i >> j) & 1] for i in range(2**len(set(x)))]
            all_different_sums = f( availables )
            for i in all_different_sums :
                if ( sum(i) == sum_remainder and len(i) == unassigned_neighbors ):
                    return True  
            return False                 
    
    #Elegxos gia conflicts
    def has_conflict( self, var, val, assignment ):
        self.has_conflict_calls += 1
        if ( var in self.down_rules_dict ):                   #An uparxei ka8etos kanonas gi auth th metavlhth sto le3iko ka8etwn kanonwn
            down_sum_rule = self.down_rules_dict[var]
        else: 
            down_sum_rule = 0
            
        if ( var in self.right_rules_dict ):                  #An uparxei orizontios kanonas gi auth th metavlhth sto le3iko orizontiwn kanonwn
            right_sum_rule = self.right_rules_dict[var]
        else: 
            right_sum_rule = 0
            
        down_sum = val                                        #ka8eto a8roisma
        right_sum = val                                       #orizontio
        right_availables = [1,2,3,4,5,6,7,8,9]
        down_availables = [1,2,3,4,5,6,7,8,9]
        right_availables.remove( val )                        #afairw to val apo tis dia8esimes times
        down_availables.remove( val )
        right_unassigned_neighbors = 0
        down_unassigned_neighbors = 0
        
        for neighbor in self.neighbors[var]:
            if neighbor in assignment: #An o geitonas einai assigned
                if ( assignment[neighbor] == val ):                     #Den epitrepw idia timh se geitones
                    return True
                if ( right_sum_rule != 0 and neighbor[0] == var[0] ):   #An uparxei orizontios kanonas kai elegxw se orizontio geitona
                        right_sum += assignment[neighbor]               #Au3anw to orizontio a8roisma me to assignment tou geitona
                        right_availables.remove( assignment[neighbor] ) #Afairw apo ta orizontia dia8esima
                        
                if ( down_sum_rule != 0 and neighbor[1] == var[1] ):    #An uparxei ka8etos kanonas kai elegxw se ka8eto geitona
                        down_sum += assignment[neighbor]                #Au3anw to ka8eto a8roisma me to assignment tou geitona
                        down_availables.remove( assignment[neighbor] )  #Afairw apo ta ka8eta dia8esimaa
            else: #An o geitonas dn einai assigned
                if ( neighbor[0] == var[0] ):
                    right_unassigned_neighbors += 1                     #Den einai assigned oloi oi orizontioi
                if ( neighbor[1] == var[1] ):
                    down_unassigned_neighbors += 1                      #Den einai assigned oloi oi orizontioi
        
        #Akolou8oun ta constraints mou
        if ( down_sum_rule != 0 and down_sum >= down_sum_rule and down_unassigned_neighbors > 0 ):
            return True
        
        if ( right_sum_rule != 0 and right_sum >= right_sum_rule and right_unassigned_neighbors > 0 ):
            return True
         
        if ( down_sum_rule != 0 and down_sum_rule != down_sum and down_unassigned_neighbors == 0 ):
            return True 
        
        if ( right_sum_rule != 0 and right_sum_rule != right_sum and right_unassigned_neighbors == 0 ):
            return True 
        
        if ( down_sum_rule != 0 ): 
            down_sum_remainder = down_sum_rule - down_sum
            if ( self.check_for_possible_sum( down_sum_remainder, down_unassigned_neighbors, down_availables ) == False ):
                return True
            
        if ( right_sum_rule != 0 ):
            right_sum_remainder = right_sum_rule - right_sum
            if ( self.check_for_possible_sum( right_sum_remainder, right_unassigned_neighbors, right_availables ) == False ):
                return True
              
        return False  
    
while (1):    
    user_selection = raw_input( "Please choose a puzzle( puzzle0, puzzle1, puzzle2, puzzle3 or puzzle4 ): " )
    sel = 5 
    if ( user_selection == "puzzle0" ):
        sel = 0
    elif (user_selection == "puzzle1" ):
        sel = 1
    elif ( user_selection == "puzzle2" ):
        sel = 2
    elif ( user_selection == "puzzle3" ):
        sel = 3
    elif ( user_selection == "puzzle4" ):
        sel = 4
    elif ( user_selection == "exit" ):
        break
    else:
        print( "Invalid Command" )
        continue
        
    kakuro = Kakuro(sel)    
    print "Forward Checking"
    start_time = time.clock()
    result = backtracking_search( kakuro, inference=forward_checking )
    print "Running time: ", time.clock() - start_time 
    print result 
    
    kakuro = Kakuro(sel)        
    print( "\nForward Checking - MRV")
    start_time = time.clock()
    result = backtracking_search( kakuro, inference=forward_checking, select_unassigned_variable=mrv)
    print "Running time: ", time.clock() - start_time 
    print result 
    
    kakuro = Kakuro(sel)    
    print( "\nBackTracking")
    start_time = time.clock()
    result = backtracking_search( kakuro )
    print "Running time: ", time.clock() - start_time 
    print result 
    
    kakuro = Kakuro(sel)    
    print( "\nBackTracking - MRV")
    start_time = time.clock()
    result = backtracking_search( kakuro, select_unassigned_variable=mrv)
    print "Running time: ", time.clock() - start_time 
    print result
    print "\n" 