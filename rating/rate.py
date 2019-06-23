from pymongo import MongoClient
# from config import config
import networkx as nx
from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np

class MaliciousVisualizer():
    def compute_graph(self):
        # Get graph from mongo
        self.mongo = MongoClient(config["MONGO_HOST"])
        # collection = mongo[config["MONGO_DATABASE"]][config["TEST_MONGO_COLLECTION"] + "_votes"]
        # votes = list(collection.find({}))
        # votes_df = pd.DataFrame(votes)
        graph = nx.DiGraph()
        # graph.add_weighted_edges_from([(
        #     vote["voter"],
        #     vote["votee"],
        #     vote["vote"]
        # ) for index, vote in votes_df.iterrows()])
        graph.add_weighted_edges_from([
            (1, 2, 1), (2, 1, 1), (3, 2, 1), (2, 3, 1), (1, 3, 1), (3, 1, 1), (4, 3, 1), (2, 4, 1), (5, 3, 1), (1, 5, 1), 
            (10, 1, 1), (10, 2, 1), (2, 10, 1), (11, 10, 1), (10, 3, 1), (3, 10, 1), (4, 11, 1), (10, 5, 1),
            (6, 7, 1), (7, 6, 1), (6, 8, 1), (8, 6, 1), # sybil 
            (2, 6, -1), (3, 6, -1), (1, 6, -1), (1, 7, -1),
        ])
        return graph
    
    def preprocess_graph_for_ranks(self):
        graph = self.graph
        plain_graph = nx.DiGraph()
        plain_graph.add_weighted_edges_from([(u, v, data["weight"]) for u, v, data in graph.edges(data=True)])
        edges = [(u, v, data["weight"]) for u, v, data in plain_graph.edges(data=True)]
        for u, v, w in edges:
            if w <= 0:
                plain_graph.remove_edge(u, v)
        return plain_graph
    
    def preprocess_graph_for_rates(self):
        graph = self.graph
        plain_graph = nx.DiGraph()
        plain_graph.add_weighted_edges_from([(u, v, 1) for u, v in graph.edges])
        return plain_graph
    
    def compute_ranks(self):
        graph = self.graph
        graph = self.preprocess_graph_for_ranks()
        return nx.pagerank(graph)
    
    def calculate_rates(self):
        graph = self.graph
        graph = self.preprocess_graph_for_rates()
        return {
            node: len(list(graph.predecessors(node)))
            for node in graph
        }

    def calculate_relative_ranks(self, rates, ranks):
        ranks_df = pd.DataFrame()
        ranks_df["rate"] = pd.Series(rates)
        ranks_df["rank"] = pd.Series(ranks)
        dataset = ranks_df.groupby("rate")["rank"].max()

        regression = LinearRegression()
        X = np.array(ranks_df.index).reshape(-1, 1)
        y = ranks_df["rank"]
        regression.fit(X, y)

        return (ranks_df["rank"] - regression.coef_[0]) / (regression.intercept_ * ranks_df["rate"])

    def save_ranks(self, ranks):
        collection = self.mongo[config["MONGO_DATABASE"]][config["TEST_MONGO_COLLECTION"]]
        for node, rank in ranks.iteritems():
            print(node, rank)
            collection.update_many({
                "author": node
            }, {
                "$set": {"author_rank": rank}
            })
    
    def compute(self):
        self.graph = self.compute_graph()
        ranks = self.compute_ranks()
        rates = self.calculate_rates()
        relative_ranks = self.calculate_relative_ranks(rates, ranks)
        self.save_ranks(relative_ranks)

if (__name__ == "__main__"):
    MaliciousVisualizer().compute()