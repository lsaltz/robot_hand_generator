import plotting
import params
import json
import ea
from addict import Dict

"""
Set test you wish to run on output hands in params and run this file
as the main file. This will display the results of running any test 
you wish on existing winning grippers.
"""
if __name__ == "__main__":
    ls =[]
    sortedScoring = []
    dicsList = []
    gen = 5001  #specify generations + 1 tests were ran for here
    sortedScoring.extend(plotting.get_data("sortedScoring", gen))
    sortedScoring = sorted(sortedScoring, key = lambda x: float(x[0]))
    top_scores, top_names = plotting.get_top(sortedScoring)
    with open("../output/totallistfile.json") as f:
        ls.extend(json.load(f))
    for name in top_names:
        for element in ls:    
            if element['name'] == name:
                dicsList.append(Dict(element))
                break
    fitnesses = plotting.test(dicsList, params.precision2)
    first = max(fitnesses, key=lambda item:item[0])[1].split(".")[0]
    ea.write_to_file(dicsList, first, fitnesses, top_names, f"{params.flag}")
    for i in dicsList:
        p = plotting.Plot(i["name"], params.precision2)
        p.main()


