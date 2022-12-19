from typing import List, Optional, Sequence, Tuple, Type, Union

import numpy as np
import torch
from redkg.config import Config
from redkg.utils import pickle_load
from torch.utils.data import DataLoader, Dataset


class Simulator:
    """Custom Environment that follows gym interface"""

    def __init__(self, config, mode):
        self.rating_dict = pickle_load(f"{config.preprocess_results_dir}/{mode}_data_dict.pkl")
        self.user_ids = list(self.rating_dict.keys())
        self.num_users = len(self.user_ids)

    def __len__(self):
        return len(self.rating_dict)

    def get_data(self, user_idx: int):
        user_id = self.user_ids[user_idx % self.num_users]
        user_ratings = np.array(self.rating_dict[user_id])
        item_ids, rates = user_ratings[:, 0].astype(np.int), user_ratings[:, 1].astype(np.float)
        return user_id, item_ids, rates

    def step(self, user_id: int, recommended_item_id: int):
        """Executes a step in the environment by applying an action. Returns the new observation and reward.

        :param user_id: Current agent (user)
        :param recommended_item_id: Action (selected item)
        :return: reward (0 if not interaction, attribute otherwise)
        """
        user_ratings = np.array(self.rating_dict[user_id])
        item_ids, rates = user_ratings[:, 0].astype(np.int), user_ratings[:, 1].astype(np.float)
        try:
            t = np.where(item_ids == recommended_item_id)[0][0]
            return rates[t]
        except IndexError:  # User did not interacted with recommended item
            return 0


class Graph:
    """Class holding k-hop neighbor information for each vertex"""

    def __init__(self, config):
        self.n_hop_kg = pickle_load(f"{config.preprocess_results_dir}/n_hop_kg.pkl")

    def get_n_hop(self, entity_id: int):
        return self.n_hop_kg[entity_id]


if __name__ == "__main__":
    conf = Config()
    simulator = Simulator(conf, "train")
    print(len(simulator))
    exit()
    graph = Graph(conf)

    user_id, item_ids, rates = simulator.get_data(0)
    print(f"User {user_id} has {len(item_ids)} interactions")
    for i, (item_id, rate) in enumerate(zip(item_ids, rates)):
        print(f"User {user_id}'s {i}th rating record is '{item_id}: {rate}/5.0'")
        n_hop_dict = graph.get_n_hop(item_id)
        print(f"First hop of {item_id} is {n_hop_dict[1]}")
        print(f"Second hop of {item_id} is {n_hop_dict[2]}")
