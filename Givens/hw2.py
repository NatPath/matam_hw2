def printCompetitor(competitor):
    '''
    Given the data of a competitor, the function prints it in a specific format.
    Arguments:
        competitor: {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition_name = competitor['competition name']
    competition_type = competitor['competition type']
    competitor_id = competitor['competitor id']
    competitor_country = competitor['competitor country']
    result = competitor['result']
    
    print(f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}')


def printCompetitionResults(competition_name, winning_gold_country, winning_silver_country, winning_bronze_country):
    '''
    Given a competition name and its champs countries, the function prints the winning countries 
        in that competition in a specific format.
    Arguments:
        competition_name: the competition name
        winning_gold_country, winning_silver_country, winning_bronze_country: the champs countries
    '''
    undef_country = 'undef_country'
    countries = [country for country in [winning_gold_country, winning_silver_country, winning_bronze_country] if country != undef_country]
    print(f'The winning competitors in {competition_name} are from: {countries}')


def key_sort_competitor(competitor):
    '''
    A helper function that creates a special key for sorting competitors.
    Arguments:
        competitor: a dictionary contains the data of a competitor in the following format: 
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition_name = competitor['competition name']
    result = competitor['result']
    return (competition_name, result)


def readParseData(file_name):
    '''
    Given a file name, the function returns a list of competitors.
    Arguments: 
        file_name: the input file name. Assume that the input file is in the directory of this script.
    Return value:
        A list of competitors, such that every record is a dictionary, in the following format:
            {'competition name': competition_name, 'competition type': competition_type,
                'competitor id': competitor_id, 'competitor country': competitor_country, 
                'result': result}
    '''
    competitors_in_competitions = []
    # TODO Part A, Task 3.4
    with open(file_name,'r') as f:
        lines=f.readlines()

    split_data=[line.split() for line in lines]

    competitors_data=[elem for elem in split_data if elem[0]=='competitor']
    competitions_data=[elem for elem in split_data if elem[0]=='competition']

    competitors={int(elem[1]):elem[2] for elem in competitors_data}

    competitions=[{"competition name":competition[1],
        "competition type":competition[3],
        "competitor id":int(competition[2]),
        "competitor country":competitors.get(int(competition[2])),
        "result":int(competition[-1])}
        for competition in competitions_data]


    competitors_in_competitions=competitions
    return competitors_in_competitions

def split_by_competition_name(competitors_in_competitions):
    list_of_competitions=[elem.get("competition name") for elem in competitors_in_competitions]
    list_of_competitions=list(dict.fromkeys(list_of_competitions))
    splited_list=[]
    for competition in list_of_competitions:
        competitors_in_specific=[elem for elem in competitors_in_competitions if elem.get("competition name")==competition]
        splited_list.append(competitors_in_specific)
    return splited_list

    
    
def calcCompetitionsResults(competitors_in_competitions):
    '''
    Given the data of the competitors, the function returns the champs countries for each competition.
    Arguments:
        competitors_in_competitions: A list that contains the data of the competitors
                                    (see readParseData return value for more info)
    Retuen value:
        A list of competitions and their champs (list of lists). 
        Every record in the list contains the competition name and the champs, in the following format:
        [competition_name, winning_gold_country, winning_silver_country, winning_bronze_country]
    '''
    competitions_champs = []
    # TODO Part A, Task 3.5
    splited_list=split_by_competition_name(competitors_in_competitions)
    
     
    no_repetitions = [strike_repetitions(single_competition) for single_competition in splited_list]
    
    for elem in no_repetitions:

        if not elem:
            continue
        sorted_=sorted(elem, key=key_sort_competitor) 
        
        

        if sorted_[0].get("competition type")=="untimed":
            sorted_.reverse()

        if len(sorted_) < 3:
            sorted_.extend([{"competitor country":"undef_country"}] * (3-len(sorted_)))

        competion_name=sorted_[0].get("competition name")
        first_place=sorted_[0].get("competitor country")
        second_place=sorted_[1].get("competitor country")
        third_place=sorted_[2].get("competitor country")
        competitions_champs.append([competion_name,first_place,second_place,third_place])
        

    return competitions_champs

def strike_repetitions(single_competition):
    existing_competitors = []
    repetitions = []
    for elem in single_competition:
        if elem.get("competitor id") in existing_competitors:
            repetitions.append(elem.get("competitor id"))
        else:
            existing_competitors.append(elem.get("competitor id"))
    
    no_repetitions = [elem for elem in single_competition if not(elem.get("competitor id") in repetitions)]
    return no_repetitions       
        
    

def partA(file_name = 'input.txt', allow_prints = True):
    # read and parse the input file
    competitors_in_competitions = readParseData(file_name)
    if allow_prints:
        for competitor in sorted(competitors_in_competitions, key=key_sort_competitor):
            printCompetitor(competitor)
    
    # calculate competition results
    competitions_results = calcCompetitionsResults(competitors_in_competitions)
    if allow_prints:
        for competition_result_single in sorted(competitions_results):
            printCompetitionResults(*competition_result_single)
    
    return competitions_results


def partB(file_name = 'input.txt'):
    competitions_results = partA(file_name, allow_prints = False)
    import Olympics

    o=Olympics.OlympicsCreate()
    for competition in competitions_results:
        Olympics.OlympicsUpdateCompetitionResults(o,str(competition[1]),str(competition[2]),str(competition[3]))
    Olympics.OlympicsWinningCountry(o)
    Olympics.OlympicsDestroy(o)

    # TODO Part B


if __name__ == "__main__":
    '''
    The main part of the script.
    __main__ is the name of the scope in which top-level code executes.
    
    To run only a single part, comment the line below which correspondes to the part you don't want to run.
    '''    
    file_name = 'input.txt'
    file_name_mine='tests/in/test2.txt'

    partA(file_name_mine)
    partB(file_name_mine)