import os
import matplotlib.pyplot as plt
import multiprocessing as mp
from datetime import datetime
import json

def bins_calc(lst: list, use: str) -> list:
    """
    Returns a list of bins to avoid gaps in histogram plotting
    for Max score or Game Score
    
    Parameters
    ----------
    lst : list
    use : str
        Choices of 'max' or 'game'
    """
    lst = sorted(list(set(lst)))
    largest = None
    if use == "max":
        largest = 2058
    elif use == "game":
        largest = int(lst[-1]) + 10
    else:
        raise ValueError("use: expexted max or game")

    l = [n for n in range(int(lst[0]))]
    r = [n for n in range(int(lst[-1]), largest)]
    return l + lst + r

def get_name(agent) -> str:
    """"
    Takes an agent object and returns the agents name.
    """
    agent_name, agent_str = "", str(agent)
    for i in range(agent_str.find("Agent") + 5, len(agent_str)):
        if ord(agent_str[i]) == ord(' '): break
        agent_name += agent_str[i]
    return agent_name

class Plotter():
    def __init__(self, game_scores=None, max_scores=None, num_steps=None, agent=None) -> None:
        self.game_scores = game_scores
        self.max_scores = max_scores
        self.num_steps = num_steps
        self.num_episodes = sum(num_steps.values())
        self.agent_name = get_name(agent)
        self.my_path = os.path.dirname(os.path.dirname(__file__))
    
    def plt_max_score(self, plt_type:str) -> None:
        """
        Plots graph of Max Score:
        
        Parameters
        ----------
        plt_type: str
            The parameters of choice are 'histo', 'bar'.
        """
        plt.clf()
        plt.title(f'Agent {self.agent_name} Max Game scores over {self.num_episodes} episodes')
        plt.xlabel("Max scores") 
        plt.ylabel("Frequency")

        if plt_type == "histo":
            max_scores = [key for key, val in self.max_scores.items() for _ in range(val)]
            plt.hist(max_scores, bins=bins_calc(lst=max_scores, use="max"), 
                    color="green")
        elif plt_type == "bar":
            plt.bar(list(self.max_scores.keys()), self.max_scores.values(),
                     color="green")
            
        time = ''.join(c for c in str(datetime.now()) if c not in '.:')
        outfile = self.my_path + f'/data/plots/{self.agent_name} MaxScore ' + time + '.jpg'
        plt.savefig(outfile)

    def plt_game_score(self, plt_type:str) -> None:
        """
        Plots graph of Max Score:
        
        Parameters
        ----------
        plt_type: str
            The parameters of choice are 'histo', 'bar'.
        """
        plt.clf()
        plt.title(f'Agent {self.agent_name} Overall Game scores over {self.num_episodes} episodes')
        plt.xlabel("Game scores") 
        plt.ylabel("Frequency")

        if plt_type == "histo":
            game_scores = [key for key, val in self.game_scores.items() for _ in range(val)]
            plt.hist(game_scores, bins=bins_calc(game_scores, use="game"), 
                    color="green")
        elif plt_type == "bar":
            plt.bar(list(self.game_scores.keys()), self.game_scores.values(), 
                    color="green")
        
        time = ''.join(c for c in str(datetime.now()) if c not in '.:')
        outfile = self.my_path + f'/data/plots/{self.agent_name} GameScore' + time + '.jpg'
        plt.savefig(outfile)

    def save_info(self) -> None:
        """
        Saves all info to a JSON file.
        """
        time = ''.join(c for c in str(datetime.now()) if c not in '.:')
        JSON_val = {
            "Agent Name" : f'{self.agent_name}',
            "# Episodes" : f'{self.num_episodes}',
            "Max Scores" : dict(sorted(self.max_scores.items())),
            "Game Scores": dict(sorted(self.game_scores.items())),
            "# of steps" : dict(sorted(self.num_steps.items()))
        }
        
        with open(self.my_path + f'\data\json\{self.agent_name} plot_info' + time + '.json', "w") as f:
            json.dump(JSON_val, f, indent=4)
    