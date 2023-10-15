import json
import math

from statistics import mean



class SimpleDataTool:

    AGENTS_FILEPATH = 'data/sfcc_2023_agents.json'
    CLAIM_HANDLERS_FILEPATH = 'data/sfcc_2023_claim_handlers.json'
    CLAIMS_FILEPATH = 'data/sfcc_2023_claims.json'
    DISASTERS_FILEPATH = 'data/sfcc_2023_disasters.json'

    REGION_MAP = {
        'west': 'Alaska,Hawaii,Washington,Oregon,California,Montana,Idaho,Wyoming,Nevada,Utah,Colorado,Arizona,New Mexico',
        'midwest': 'North Dakota,South Dakota,Minnesota,Wisconsin,Michigan,Nebraska,Iowa,Illinois,Indiana,Ohio,Missouri,Kansas',
        'south': 'Oklahoma,Texas,Arkansas,Louisiana,Kentucky,Tennessee,Mississippi,Alabama,West Virginia,Virginia,North Carolina,South Carolina,Georgia,Florida',
        'northeast': 'Maryland,Delaware,District of Columbia,Pennsylvania,New York,New Jersey,Connecticut,Massachusetts,Vermont,New Hampshire,Rhode Island,Maine'
    }

    def __init__(self):
        self.__agent_data = self.load_json_from_file(self.AGENTS_FILEPATH)
        self.__claim_handler_data = self.load_json_from_file(
            self.CLAIM_HANDLERS_FILEPATH)
        self.__claim_data = self.load_json_from_file(self.CLAIMS_FILEPATH)
        self.__disaster_data = self.load_json_from_file(
            self.DISASTERS_FILEPATH)
        

    # Helper Methods

    def load_json_from_file(self, filename):
        data = None

        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data

    def get_agent_data(self):
        return self.__agent_data

    def get_claim_handler_data(self):
        return self.__claim_handler_data

    def get_disaster_data(self):
        return self.__disaster_data

    def get_claim_data(self):
        return self.__claim_data

    # Unit Test Methods

    # region Test Set One

    def get_num_closed_claims(self):
        """Calculates the number of claims where that status is "Closed"

        Returns:
            int: number of closed claims
        """
        data = self.get_claim_data()

        num_closed_claims = 0
        for claim in data:
            if claim['status'] == 'Closed':
                num_closed_claims += 1

        return num_closed_claims
        

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        data = self.get_claim_data()
        #Group claims by handler id - 'Fill the buckets'
        claims_by_handler_dict = {}

        for claim in data:
            claim_handler_id = claim["claim_handler_assigned_id"]
            claims_by_handler_dict[claim_handler_id] = claims_by_handler_dict.get(claim_handler_id, 0) + 1

        return claims_by_handler_dict[claim_handler_id]

       

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        data = self.get_disaster_data()
        #Group disasters by state - 'Fill the buckets'
        num_disasters_by_state_dict = {}

        for disaster in data:
            st = disaster["state"]
            num_disasters_by_state_dict[st] = num_disasters_by_state_dict.get(st, 0) + 1

        return num_disasters_by_state_dict[state]


    # endregion

    # region Test Set Two

    def get_total_claim_cost_for_disaster(self, disaster_id):
        """Sums the estimated cost of a specific disaster by its claims

        Args:
            disaster_id (int): id of disaster

        Returns:
            float | None: estimate cost of disaster, rounded to the nearest hundredths place
                          returns None if no claims are found
        """
        data = self.get_claim_data()
        for claim in data:
            if claim['disaster_id'] == disaster_id:
                return claim['estimate_cost']
        return None
    

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        data = self.get_claim_data()
        #Group claims by handler id - 'Fill the buckets'
        claims_by_handler_dict = {}

        average_claim_cost = 0
        for claim in data:
            claim_handler_id = claim["claim_handler_assigned_id"]
            #For each claim, have a two-item list for each claim representing the total cost of claims and the number of claims, respectively, by claim handler id
            claims_by_handler_dict.get(claim_handler_id, [0, 0])[0] += claim["estimate_cost"]
            claims_by_handler_dict.get(claim_handler_id, [0, 0])[1] += 1
        
        average_claim_cost = claims_by_handler_dict[claim_handler_id][0]/claims_by_handler_dict[claim_handler_id][1]
        
        return average_claim_cost
    

    def get_state_with_most_disasters(self):
        """Returns the name of the state with the most disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Jersey and Delaware both have the highest number of disasters at
                 12 disasters each. Then, this method would return "Delaware" since "D"
                 comes before "N" in the alphabet. 

        Returns:
            string: single name of state
        """
        import heapq

        data = self.get_disaster_data()
        #Group disasters by state - 'Fill the buckets'
        num_disasters_by_state_dict = {}
        state_set = set()
        for disaster in data:
            st = disaster["state"]
            num_disasters_by_state_dict[st] = num_disasters_by_state_dict.get(st, 0) + 1
            state_set.add(st)
        
        states = list(state_set)
        total_cost_by_state_tuple_list = []
        for state in states:
            heapq.heappush(total_cost_by_state_tuple_list, (-num_disasters_by_state_dict[state], state))

        return heapq.heappop()[1]
        

    def get_state_with_least_disasters(self):
        """Returns the name of the state with the least disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Mexico and West Virginia both have the least number of disasters at
                 1 disaster each. Then, this method would return "New Mexico" since "N"
                 comes before "W" in the alphabet. 

        Returns:
            string: single name of state
        """
        import heapq

        data = self.get_disaster_data()
        #Group disasters by state - 'Fill the buckets'
        num_disasters_by_state_dict = {}
        state_set = set()
        for disaster in data:
            st = disaster["state"]
            num_disasters_by_state_dict[st] = num_disasters_by_state_dict.get(st, 0) + 1
            state_set.add(st)
        
        states = list(state_set)
        total_cost_by_state_tuple_list = []
        for state in states:
            heapq.heappush(total_cost_by_state_tuple_list, (num_disasters_by_state_dict[state], state))

        return heapq.heappop()[1]
        
    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        import heapq
        data = self.get_agent_data()
        agent_languages_by_state_dict = {}
        for agent in data:
            st = agent["state"]
            lang = agent["secondary_language"]
            #Store a dictionary of languages spoken by agents as a value for the state key in outer dictionary
            language_dict = agent_languages_by_state_dict.get(st, {})
            #Update dictionary of spoken languages by agents in this state            
            language_dict[lang] = language_dict.get(lang, (0, lang))[0]+1

        lang_dict_by_state = agent_languages_by_state_dict[state]
        #Iterate through enumeration of number-language tuples from inner dict corresponding to state
        spoken_languages = []
        for num, language in list(lang_dict_by_state.values()):
            heapq.heappush(spoken_languages, (-num, language))
        
        return heapq.heappop()[1]

    def get_num_of_open_claims_for_agent_and_severity(self, agent_id, min_severity_rating):
        """Returns the number of open claims for a specific agent and for a minimum severity level and higher

        Note: Severity rating scale for claims is 1 to 10, inclusive.
        
        Args:
            agent_id (int): ID of the agent
            min_severity_rating (int): minimum claim severity rating

        Returns:
            int | None: number of claims that are not closed and have minimum severity rating or greater
                        -1 if severity rating out of bounds
                        None if agent does not exist, or agent has no claims (open or not)
        """
        data = self.get_claim_data()
        #Group claims by handler id - 'Fill the buckets'
        open_claims_for_agent_and_severity = {}

        for claim in data:
            a_id = claim['agent_assigned_id']
            if claim['status'] != 'Closed' and claim['severity_rating'] >= min_severity_rating:
                open_claims_for_agent_and_severity[a_id] = open_claims_for_agent_and_severity.get(a_id, 0) + 1

        return open_claims_for_agent_and_severity[agent_id]


    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        import time

        data = self.get_disaster_data()
        num_disasters_declared_after_end_date = 0
        for disaster in data:
            end_date = disaster['end_date']
            declared_date = disaster['declared_date']
            #convert both date strings to compare
            end_date = time.strptime(end_date, "%Y-%m-%d")
            declared_date = time.strptime(declared_date, "%Y-%m-%d")

            if declared_date > end_date:
                num_disasters_declared_after_end_date += 1
        
        return num_disasters_declared_after_end_date


    def build_map_of_agents_to_total_claim_cost(self):
        """Builds a map of agent and their total claim cost

        Hints:
            An agent with no claims should return 0
            Invalid agent id should have a value of None
            You should round your total_claim_cost to the nearest hundredths

        Returns:
            dict: key is agent id, value is total cost of claims associated to the agent
        """
        data = self.get_claim_data()
        map_of_agents_to_total_claim_cost = {}
        for claim in data:
            agent_id = claim['agent_assigned_id']
            map_of_agents_to_total_claim_cost[agent_id] = map_of_agents_to_total_claim_cost.get(agent_id, 0) + claim['estimate_cost']

        return map_of_agents_to_total_claim_cost

    def calculate_disaster_claim_density(self, disaster_id):
        """Calculates density of a diaster based on the number of claims and impact radius

        Hints:
            Assume uniform spacing between claims
            Assume disaster impact area is a circle

        Args:
            disaster_id (int): id of diaster

        Returns:
            float: density of claims to disaster area, rounded to the nearest thousandths place
                   None if disaster does not exist
        """
        claim_data = self.get_claim_data()
        disaster_data = self.get_disaster_data()
        disaster_id_to_radius_map = {}
        density_by_disaster_id_map = {}

        for disaster in disaster_data:
            d_id = disaster['id']
            radius = disaster['radius_miles']
            disaster_id_to_radius_map[d_id] = radius

        for claim in claim_data:
            d_id = claim['disaster_id']
            area = math.pi * (disaster_id_to_radius_map[d_id])^2
            #Create two-value list representing number of claims and disaster area to calculate density
            density_by_disaster_id_map.get(d_id, [0, area])[0] += 1
        
        total_claims = disaster_id_to_radius_map[disaster_id][0]
        disaster_area = disaster_id_to_radius_map[disaster_id][1]

        return total_claims/disaster_area


    # endregion

    # region TestSetFour

    def get_top_three_months_with_highest_num_of_claims_desc(self):
        """Gets the top three months with the highest total claim cost

        Hint:
            Month should be full name like 01 is January and 12 is December
            Year should be full four-digit year
            List should be in descending order

        Returns:
            list: three strings of month and year, descending order of highest claims
        """
        import heapq

        claim_data = self.get_claim_data()
        disaster_data = self.get_disaster_data()

        total_claim_cost_by_month = {}
        disaster_id_to_month = {}

        for disaster in disaster_data:
            id = disaster['id']
            declared_date = disaster['declared_date']
            #Parse substring from date to month integer
            month = int(declared_date[6])
            year = int(declared_date[0:4])
            #Format by 'month/year'
            disaster_id_to_month[id] = f'{month}/{year}'

        for claim in claim_data:
            d_id = claim['disaster_id']
            cost = claim['estimate_cost']
            month_year = disaster_id_to_month[d_id]
            total_claim_cost_by_month.get(month_year, (0, month_year))[0] += cost
        
        #Iterate on each month and build a list with max-heap structure
        sum_of_claims_by_month = []
        for month in list(total_claim_cost_by_month.keys()):
            tup = total_claim_cost_by_month[month]
            tup[0] *= -1
            heapq.heappush(sum_of_claims_by_month, tup)

        return sum_of_claims_by_month[0:3]


    # endregion
