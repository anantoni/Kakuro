from csp import *
from utils import *
from csp_search import *
import time

# Map-Coloring Problem

class MapColoring(CSP):
    """ 
    >>> backtracking_search(australia)
    {'WA': 'R', 'Q': 'R', 'T': 'R', 'V': 'R', 'SA': 'G', 'NT': 'B', 'NSW': 'B'}
    >>> backtracking_search(australia, select_unassigned_variable=mrv)
    {'WA': 'R', 'Q': 'R', 'T': 'R', 'V': 'R', 'SA': 'G', 'NT': 'B', 'NSW': 'B'}
    >>> backtracking_search(australia, inference=forward_checking)
    {'Q': 'R', 'T': 'R', 'WA': 'R', 'V': 'R', 'SA': 'G', 'NT': 'B', 'NSW': 'B'}
    >>> backtracking_search(australia, inference=mac)
    {'WA': 'R', 'Q': 'R', 'T': 'R', 'V': 'R', 'SA': 'G', 'NT': 'B', 'NSW': 'B'}
    >>> backtracking_search(usa, select_unassigned_variable=mrv, inference=mac)
    {'WA': 'R', 'DE': 'G', 'DC': 'R', 'WI': 'G', 'WV': 'B', 'HI': 'R', 'FL': 'B', 'WY': 'R', 'NH': 'G', 'NJ': 'B', 'NM': 'R', 'TX': 'G', 'LA': 'B', 'NC': 'R', 'ND': 'R', 'NE': 'B', 'TN': 'B', 'NY': 'G', 'PA': 'R', 'RI': 'G', 'NV': 'R', 'VA': 'G', 'CO': 'G', 'CA': 'G', 'AL': 'R', 'AR': 'R', 'VT': 'R', 'IL': 'B', 'GA': 'G', 'IN': 'G', 'IA': 'R', 'MA': 'B', 'AZ': 'B', 'ID': 'G', 'CT': 'R', 'ME': 'R', 'MD': 'Y', 'KA': 'R', 'OK': 'B', 'OH': 'Y', 'UT': 'Y', 'MO': 'G', 'MN': 'B', 'MI': 'R', 'AK': 'R', 'MT': 'B', 'MS': 'G', 'SC': 'B', 'KY': 'R', 'OR': 'B', 'SD': 'G'}
    >>> min_conflicts(usa, 100000)
    {'WA': 'R', 'DE': 'G', 'DC': 'R', 'WI': 'G', 'WV': 'B', 'HI': 'R', 'FL': 'B', 'WY': 'R', 'NH': 'G', 'NJ': 'B', 'NM': 'R', 'TX': 'G', 'LA': 'B', 'NC': 'R', 'ND': 'R', 'NE': 'B', 'TN': 'B', 'NY': 'G', 'PA': 'R', 'RI': 'G', 'NV': 'R', 'VA': 'G', 'CO': 'G', 'CA': 'G', 'AL': 'R', 'AR': 'R', 'VT': 'R', 'IL': 'B', 'GA': 'G', 'IN': 'G', 'IA': 'R', 'OK': 'B', 'AZ': 'B', 'ID': 'G', 'CT': 'R', 'ME': 'R', 'MD': 'Y', 'KA': 'R', 'MA': 'B', 'OH': 'Y', 'UT': 'Y', 'MO': 'G', 'MN': 'B', 'MI': 'R', 'AK': 'R', 'MT': 'B', 'MS': 'G', 'SC': 'B', 'KY': 'R', 'OR': 'B', 'SD': 'G'}
    """

    def __init__(self, colors, neighbors):
        """Make a CSP for the problem of coloring a map with different colors
        for any two adjacent regions.  Arguments are a list of colors, and a
        dict of {region: [neighbor,...]} entries.  This dict may also be
        specified as a string of the form defined by parse_neighbors."""
        if isinstance(neighbors, str):
            neighbors = parse_neighbors(neighbors)
        domain=dict()    
        for i in neighbors.keys():
            domain[i]=colors[:]
        self.has_conflict_calls = 0
        self.arc_conflict_calls = 0
        self.nconflicts_calls = 0
        self.nodes_counter = 0
        CSP.__init__(self, neighbors.keys(), domain, neighbors, self.has_conflict)        
                   
    def has_conflict(self, var, val, assignment):
        self.has_conflict_calls += 1
        "A constraint saying two neighboring variables must differ in value."
        for neighbor in self.neighbors[var]:
            if neighbor in assignment:
                if assignment[neighbor] == val:
                    return True 
        return False  
    
    def arc_conflict(self, A, a, B, b):
        self.arc_conflict_calls += 1
        "A constraint saying two neighboring variables must differ in value."
        if a != b :
            return False
        else:
            return True 
             
    def nconflicts(self, var, val, assignment):   
        self.nconflicts_calls += 1  
        conflicts=0

        for neighbor in self.neighbors[var]:
            if neighbor in assignment:
                if assignment[neighbor] == val:
                    conflicts+=1 
        return conflicts

def parse_neighbors(neighbors, vars=[]):
    """Convert a string of the form 'X: Y Z; Y: Z' into a dict mapping
    regions to neighbors.  The syntax is a region name followed by a ':'
    followed by zero or more region names, followed by ';', repeated for
    each region name.  If you say 'X: Y' you don't need 'Y: X'.
    >>> parse_neighbors('X: Y Z; Y: Z')
    {'Y': ['X', 'Z'], 'X': ['Y', 'Z'], 'Z': ['X', 'Y']}
    """
    dict = DefaultDict([])
    for var in vars:
        dict[var] = []
    specs = [spec.split(':') for spec in neighbors.split(';')]
    for (A, Aneighbors) in specs:
        A = A.strip()
        dict.setdefault(A, [])
        for B in Aneighbors.split():
            dict[A].append(B)
            dict[B].append(A)
    return dict



australia1 = MapColoring(list('RGB'), """SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: """)
australia2 = MapColoring(list('RGB'), """SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: """)
australia3 = MapColoring(list('RGB'), """SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: """)


usa1 = MapColoring(list('RGBY'),
        """WA: OR ID; OR: ID NV CA; CA: NV AZ; NV: ID UT AZ; ID: MT WY UT;
        UT: WY CO AZ; MT: ND SD WY; WY: SD NE CO; CO: NE KA OK NM; NM: OK TX;
        ND: MN SD; SD: MN IA NE; NE: IA MO KA; KA: MO OK; OK: MO AR TX;
        TX: AR LA; MN: WI IA; IA: WI IL MO; MO: IL KY TN AR; AR: MS TN LA;
        LA: MS; WI: MI IL; IL: IN KY; IN: OH KY; MS: TN AL; AL: TN GA FL;
        MI: OH IN; OH: PA WV KY; KY: WV VA TN; TN: VA NC GA; GA: NC SC FL;
        PA: NY NJ DE MD WV; WV: MD VA; VA: MD DC NC; NC: SC; NY: VT MA CT NJ;
        NJ: DE; DE: MD; MD: DC; VT: NH MA; MA: NH RI CT; CT: RI; ME: NH;
        HI: ; AK: """)

usa2 = MapColoring(list('RGBY'),
        """WA: OR ID; OR: ID NV CA; CA: NV AZ; NV: ID UT AZ; ID: MT WY UT;
        UT: WY CO AZ; MT: ND SD WY; WY: SD NE CO; CO: NE KA OK NM; NM: OK TX;
        ND: MN SD; SD: MN IA NE; NE: IA MO KA; KA: MO OK; OK: MO AR TX;
        TX: AR LA; MN: WI IA; IA: WI IL MO; MO: IL KY TN AR; AR: MS TN LA;
        LA: MS; WI: MI IL; IL: IN KY; IN: OH KY; MS: TN AL; AL: TN GA FL;
        MI: OH IN; OH: PA WV KY; KY: WV VA TN; TN: VA NC GA; GA: NC SC FL;
        PA: NY NJ DE MD WV; WV: MD VA; VA: MD DC NC; NC: SC; NY: VT MA CT NJ;
        NJ: DE; DE: MD; MD: DC; VT: NH MA; MA: NH RI CT; CT: RI; ME: NH;
        HI: ; AK: """)

usa3 = MapColoring(list('RGBY'),
        """WA: OR ID; OR: ID NV CA; CA: NV AZ; NV: ID UT AZ; ID: MT WY UT;
        UT: WY CO AZ; MT: ND SD WY; WY: SD NE CO; CO: NE KA OK NM; NM: OK TX;
        ND: MN SD; SD: MN IA NE; NE: IA MO KA; KA: MO OK; OK: MO AR TX;
        TX: AR LA; MN: WI IA; IA: WI IL MO; MO: IL KY TN AR; AR: MS TN LA;
        LA: MS; WI: MI IL; IL: IN KY; IN: OH KY; MS: TN AL; AL: TN GA FL;
        MI: OH IN; OH: PA WV KY; KY: WV VA TN; TN: VA NC GA; GA: NC SC FL;
        PA: NY NJ DE MD WV; WV: MD VA; VA: MD DC NC; NC: SC; NY: VT MA CT NJ;
        NJ: DE; DE: MD; MD: DC; VT: NH MA; MA: NH RI CT; CT: RI; ME: NH;
        HI: ; AK: """)

france1 = MapColoring(list('RGBY'),
        """AL: LO FC; AQ: MP LI PC; AU: LI CE BO RA LR MP; BO: CE IF CA FC RA
        AU; BR: NB PL; CA: IF PI LO FC BO; CE: PL NB NH IF BO AU LI PC; FC: BO
        CA LO AL RA; IF: NH PI CA BO CE; LI: PC CE AU MP AQ; LO: CA AL FC; LR:
        MP AU RA PA; MP: AQ LI AU LR; NB: NH CE PL BR; NH: PI IF CE NB; NO:
        PI; PA: LR RA; PC: PL CE LI AQ; PI: NH NO CA IF; PL: BR NB CE PC; RA:
        AU BO FC PA LR""")

france2 = MapColoring(list('RGBY'),
        """AL: LO FC; AQ: MP LI PC; AU: LI CE BO RA LR MP; BO: CE IF CA FC RA
        AU; BR: NB PL; CA: IF PI LO FC BO; CE: PL NB NH IF BO AU LI PC; FC: BO
        CA LO AL RA; IF: NH PI CA BO CE; LI: PC CE AU MP AQ; LO: CA AL FC; LR:
        MP AU RA PA; MP: AQ LI AU LR; NB: NH CE PL BR; NH: PI IF CE NB; NO:
        PI; PA: LR RA; PC: PL CE LI AQ; PI: NH NO CA IF; PL: BR NB CE PC; RA:
        AU BO FC PA LR""")

france3 = MapColoring(list('RGBY'),
        """AL: LO FC; AQ: MP LI PC; AU: LI CE BO RA LR MP; BO: CE IF CA FC RA
        AU; BR: NB PL; CA: IF PI LO FC BO; CE: PL NB NH IF BO AU LI PC; FC: BO
        CA LO AL RA; IF: NH PI CA BO CE; LI: PC CE AU MP AQ; LO: CA AL FC; LR:
        MP AU RA PA; MP: AQ LI AU LR; NB: NH CE PL BR; NH: PI IF CE NB; NO:
        PI; PA: LR RA; PC: PL CE LI AQ; PI: NH NO CA IF; PL: BR NB CE PC; RA:
        AU BO FC PA LR""")

print("====AUSTRALIA====")
print("\nFC-MRV:")
start_time = time.clock()
result = backtracking_search( australia1, inference=forward_checking, select_unassigned_variable=mrv )
print "Running time: ", time.clock() - start_time 
print( result )

print( "\nMAC:" )
start_time = time.clock()
result = backtracking_search(australia2, inference=mac)
print "Running time: ", time.clock() - start_time 
print( result )

print( "\nMin-conflicts:" )
start_time = time.clock()
result = min_conflicts( australia3 )
print "Running time: ", time.clock() - start_time
print( result )

print("\n====USA====")
print("\nFC-MRV:")
start_time = time.clock()
result = backtracking_search( usa1, inference=forward_checking, select_unassigned_variable=mrv )
print "Running time: ", time.clock() - start_time
print( result )

print( "\nMAC:" )
start_time = time.clock()
result = backtracking_search( usa2, inference=mac)
print "Running time: ", time.clock() - start_time
print( result )

print( "\nMin-conflicts:" )
start_time = time.clock()
result = min_conflicts( usa3 )
print "Running time: ", time.clock() - start_time
print( result )

print("\n====FRANCE====")
print("\nFC-MRV:")
start_time = time.clock()
result = backtracking_search( france1, inference=forward_checking, select_unassigned_variable=mrv )
print "Running time: ", time.clock() - start_time
print( result )

print( "\nMAC:" )
start_time = time.clock()
result = backtracking_search( france2, inference=mac)
print "Running time: ", time.clock() - start_time
print( result )

print( "\nMin-conflicts:" )
start_time = time.clock()
result = min_conflicts( france3 )
print "Running time: ", time.clock() - start_time
print( result )