# By Marshall Saltz
import random
import json
import mutations as mutation
from addict import Dict
import main
import basic_load
import combination
import first_generation
import copy
import test as nt
import build_hand as bh
import plotting
import params


def crossover(p0, p1, gen, comb_mode, ind):
    """
    Calls combine to combine two files
    Parameters:
        p0 - parent 0
        p1 - parent 1
        gen - generation number
        comb_mode - a letter indicating which mode of combining
        ind - child index
    Returns:
        child_list - a list of two child dictionaries created
    """
    child_list = []
    d0 = Dict()
    d1 = Dict()
    c = combination.crossoverFunctions(p0, p1, comb_mode, ind, gen)                   
    d0, d1 = c.combo()
    child_list.append(copy.deepcopy(d0))
    child_list.append(copy.deepcopy(d1))
    return child_list


def carrier(genList, total_list, first, generation):    
    """
    Combines the fittest dictionary with a random collection of dictionaries.
    Parameters:
        genList - generational list of grippers
        total_list - total list of grippers
        first - gripper with highest fitness score
        generation - generation number
    Returns:
        child_list - list of created dictionaries
    """
    child_list = []
    fittest_dic = next((d for d in total_list if d['name'] == first), None)
    for i in range(params.carrier_num):
        recipient_dic = genList[random.randint(0,len(genList)-1)]
        child_list.extend(crossover(fittest_dic, recipient_dic, generation, "w", i))
    return child_list


def even_odd(genList, generation):
    """
    Combines random even dictionaries with random odd dictionaries.
    Parameters:
        genList - generational list of grippers
        generation - generation number
    Returns:
        child_list - list of created dictionaries
    """
    oddDics = []
    evenDics = []
    child_list = []
    for c in range(len(genList)):     
        if c%2 == 0:
            oddDics.append(copy.deepcopy(genList[c]))
        else:
            evenDics.append(copy.deepcopy(genList[c]))      
    for i in range(params.even_odd_num):
        child_list.extend(crossover(evenDics[random.randint(0, (len(evenDics) - 1))], oddDics[random.randint(0, (len(oddDics) - 1))], generation, "eo", i))
    return child_list


def mutate_files(to_mutate, file_to_mutate, gen, idx):
    """
    Mutates selected gripper.
    Parameters:
        to_mutate - list of gripper dictionaries to mutate
        file_to_mutate - name of selected gripper
        gen - generation number
        idx - if running multiple mutations, mutation number
    Returns:
        mutated_gripper - mutated version of selected gripper
    """
    for m in to_mutate:
        if str(m['name']) == str(file_to_mutate):
            mutate_dic = m
    m = mutation.Mutate(mutate_dic, gen, idx)
    mutated_gripper = m.build_hand()
    return mutated_gripper
 

def test(dicList, precision):
    """
    Runs test on grippers.
    Parameters:
        dicList - list of dictionaries to test
        precision - space in between points (mm)
    Returns:
        fitnesses - list of test results
    """
    fitnesses = []
    for l in dicList:    
        gripper_name = l['name']    
        w = nt.WorkSpace_Test(gripper_name, l, precision)     
        fit = w.main()
        fitnesses.append([fit, f"{gripper_name}.json"])
    
    return fitnesses
    
    
def get_top(sortedScoring):
    """
    Returns top grippers.
    Parameters:
        sortedScoring - list of grippers and their scores sorted by score in ascending order
    Returns:
        top - list of top grippers and their scores
        top_names - just the grippers' names
    """
    top = []
    count = 0
    for d in reversed(range(len(sortedScoring))):
        if sortedScoring[d] not in top:
            top.append(sortedScoring[d])
            count += 1
        if count > params.winner_count:
            break
    top_names = list(map(lambda x:x[1].split('.')[0], top))
    return top, top_names 


def write_to_file(total_list, fittestFirst, top_ls, top_names, precision):
    """
    Writes results to a file.
    Parameters:
        total_list - list of all created dictionaries
        fittestFirst - the winner
        top_ls - list of top 20 scores
        top_names - list of top 20 names
        precision - coarse or fine
    """
    winning_file_names = []
    winning_ratios = []
    winning_file_names = top_names
    for x in range(len(total_list)):
        if total_list[x].name in winning_file_names:
              winning_ratios.append(total_list[x])    
    with open(f"../output/results_{params.flag}_{precision}.txt", mode="w") as resultsFile:
        resultsFile.write(f"The fittest of them all in {params.flag} test is: " + str(fittestFirst) + "\n")
        resultsFile.write("Overall top results are: \n" + str(top_ls) + "\n")
        for j in range(len(winning_ratios)):
            resultsFile.write(f"{winning_ratios[j]}\n")
    resultsFile.close()  


def generate_hands(ls, to_build):
    """
    Generates urdf files for grippers.
    Parameters:
        ls - total list of dictionaries
        to_build - gripper to build
    """
    for l in ls:
        if l.name == str(to_build.split('.')[0]):
            hand_data = l
            break
    b = bh.Build_Json(hand_data)
    b.build_hand()
    main.MainScript()
    

def open_file(gripper):
    """
    Opens gripper in pybullet.
    Parameters:
        gripper - file to open
    """
    name = gripper.split('.')[0]
    rt = f"../output/{name}/hand"
    fittest_file = f"{rt}/{name}.urdf"
    basic_load.load(fittest_file) 
    

def save_all_hands(data, filename):
    """
    Saves a file as a json.
    Parameters:
        ls - data to save
        filename - file to save to
    """
    with open(f"../output/{filename}.json", mode="w") as handsFile:
        new_j = json.dumps(data)
        handsFile.write(new_j)
        handsFile.close()   

def get_data(filename, gen):
    """
    Gets data from a json. Since it saves every interval, it uses that info to get the file.
    Parameters:
        filename - file from which to retreive data
        gen - generation number
    Returns:
        data - data from file (list form)
    """
    data = []
    for i in range(gen):
        if i % params.interval == 0 and i != 0:
            with open(f"../output/{filename}{i}.json", mode="r") as p:
                data.extend(json.load(p))
    return data    

                      
if __name__ == "__main__":
    print("Please input the integer number of generations you would like to run this for: ")
    gen = int(input())+1  # generations ea runs for
    
    ls = []    # total list of grippers
    cycle_fitness = []  # list of fitnesses for that generation
    genList = []    # list of that generation's grippers
    mutations = []  # results from mutating
    sortedScoring = []  # sorted scores paired with names
    tmpList = []    # a temporary list for storing grippers
    generational_fitness= []    # maximum fitness from each generation
    
    # gen 0 grippers - init_num amount of grippers
    for n in range(params.init_num): 
        g0 = first_generation.First_Generation(0, n)
        tmpList.append(g0.build_hand())
    genList.extend(tmpList)
    ls.extend(tmpList)
    
    # mutate grippers - mutations_num amount of grippers
    for i in range(params.mutations_num):
        genList.append(mutate_files(ls, ls[random.randint(0,len(ls)-1)].name, 0, i))
    
    # test grippers
    cycle_fitness.extend(test(genList, params.precision1))
    sortedScoring.extend(cycle_fitness)

    # add gripper dictionaries to total list
    ls.extend(genList)

    # get the top grippers
    first= max(cycle_fitness, key=lambda item:item[0])[1].split(".")[0]
    cycle_fitness = sorted(cycle_fitness, key = lambda x: float(x[0]))
    top_scores, top_names = get_top(cycle_fitness)

    # append maximum fitness of that generation
    generational_fitness.append(max(cycle_fitness, key=lambda item:item[0])[0])
    
    cycle_fitness.clear()   
    mutations.clear() 

    # copy gen 0 grippers
    # Gen 0: init_num + mutations_num amount of grippers
    tmpList = copy.deepcopy(genList)

    # begin generations loop
    for num in range(1, gen):
        
        genList = []    # list of grippers of current generation
        cycle_fitness = []  # list of fitnesses for generation
        mutations = []  # mutation list of grippers on top grippers
        mut_ran = []    # mutation list of randomly mutrated grippers

        # mutate on random grippers from previous generation - random_mutations_num amount of grippers
        for i in range(params.random_mutations_num):
            mutt = copy.deepcopy(tmpList[random.randint(0,len(tmpList)-1)])
            mut_ran.append(mutate_files(tmpList, mutt.name, num, i))
            genList.append(mutt)


        # mutate on top grippers from previous generation - winner_mutations_num amount of grippers
        for i in range(params.winner_count):
            mutations.append(mutate_files(tmpList, top_names[i], num, (i+5)))
            genList.extend(copy.deepcopy([j for j in tmpList if j.name == top_names[i] and j not in genList]))
            
        # append mutations to generation list
        genList.extend(mut_ran)
        genList.extend(mutations)
        
        # test grippers (coarse)
        cycle_fitness.extend(test(genList, params.precision1))
        
        # add generation to total list of grippers
        ls.extend(genList)

        # perform combination of winner with grippers - 2 * carrier_num amount of grippers
        carrierList = carrier(genList, ls, first, num)
        # test children
        cycle_fitness.extend(test(carrierList, params.precision1))

        # perform combination of even and odd grippers - 2 * even_odd_num amount of grippers
        eoList = even_odd(genList, num)
        # test children
        cycle_fitness.extend(test(eoList, params.precision1))

        # append to generational list
        genList.extend(carrierList)
        genList.extend(eoList)
        
        # append to total list
        ls.extend(genList)

        # append scores and associated names
        sortedScoring.extend(cycle_fitness)
        
        # append maximum generation score
        generational_fitness.append(max(cycle_fitness, key=lambda item:item[0])[0])

        # copy previous generation
        tmpList.clear()
        tmpList = copy.deepcopy(genList)        
        genList.clear()

        # get winner
        first = max(cycle_fitness, key=lambda item:item[0])[1].split(".")[0]
        cycle_fitness = sorted(cycle_fitness, key = lambda x: float(x[0]))
        top_scores, top_names = get_top(cycle_fitness) 
        cycle_fitness.clear()
        first_fittest_dic = copy.deepcopy([i for i in ls if i['name'] == first])

        # save hands at interval so as not to slow things down
        if (num % params.interval) == 0:
            save_all_hands(ls, f"totallist{num}")
            save_all_hands(sortedScoring,f"sortedScoring{num}")
            save_all_hands(generational_fitness, f"generationalfitness{num}")
            ls.clear()
            sortedScoring.clear()
            generational_fitness.clear()
            ls.extend(first_fittest_dic)     
        
    # get and sort scoring data
    sortedScoring = list(get_data("sortedScoring", gen))
    sortedScoring = sorted(sortedScoring, key = lambda x: float(x[0]))
    
    # get winners and all hands
    first = max(sortedScoring, key=lambda item:item[0])[1].split(".")[0]
    top_scores, top_names = get_top(sortedScoring)
    ls = list([Dict(i) for i in get_data("totallist", gen)])
    
    # save all data
    save_all_hands(ls, "totallistfile")
    write_to_file(ls, first, top_scores, top_names, "coarse")

    sortedScoring.clear()

    # plot generational scores
    generational_fitness = list(get_data("generationalfitness", gen))
    plotting.plot_fitness(generational_fitness, gen)
    
    # generate urdf files for winning grippers
    for name in top_names:
        generate_hands(ls, name)

    new_test = []   # fine test data

    # copy over dictionaries of top grippers
    for l in ls:
        if l.name in top_names and l not in new_test:
            new_test.append(copy.deepcopy(l))
    ls.clear()
    
    # plot coarse data
    for top in top_names:
        name = top
        
        p = plotting.Plot(name, params.precision1)
        p.main()

    # run fine test, save data, and plot
    new_fitness = test(new_test, params.precision2)
    write_to_file(new_test, first, new_fitness, top_names, "fine")
    for top in top_names:
        name = top
        p = plotting.Plot(name, params.precision2)
        p.main()
