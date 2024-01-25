   

def gui_test(dicList, num, coords0, coords1):####
    tmpFitness = []
    
    for l in dicList:
        name = l['name']
        rt = f"../output/{name}/hand"
        sim_test = testing.sim_tester(name, rt, l, coords0, coords1, "t")
        tmpFitness.append(sim_test.gui_test())
        
    return tmpFitness

def final_test(dicList, num, coords0, coords1):####
    tmpFitness = []
    
    for l in dicList:
        name = l
        rt = f"../output/{name}/hand"
        sim_test = testing.sim_tester(name, rt, l, coords0, coords1, "f")
        tmpFitness.append(sim_test.gui_test())
        
    return tmpFitness    

"""
Sorts scores
Parameters:
    scoring: unsorted fitness list
"""    
def sort_scores(scoring):###
    sortedScoring = sorted(scoring, key = lambda x: float(x[0])) #Sorts array by fittness scores
    
    return sortedScoring

