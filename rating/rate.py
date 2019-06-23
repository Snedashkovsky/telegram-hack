from pymongo import MongoClient
from config import config
import networkx as nx
from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np

class MaliciousVisualizer():
    def compute_graph(self):
        # Get graph from mongo
        self.mongo = MongoClient(config["MONGO_HOST"])
        collection = self.mongo[config["MONGO_DATABASE"]][config["TEST_MONGO_COLLECTION"] + "_votes"]
        votes = list(collection.find({}))
        votes_df = pd.DataFrame(votes)
        graph = nx.DiGraph()
        graph.add_weighted_edges_from([(
            vote["voter"],
            vote["votee"],
            vote["vote"]
        ) for index, vote in votes_df.iterrows()])
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
        X = np.array(dataset.index).reshape(-1, 1)
        y = dataset.tolist()
        regression.fit(X, y)
        print(X, y, regression.intercept_, regression.coef_[0])

        return (ranks_df["rank"] - regression.intercept_) / (regression.coef_[0] * ranks_df["rate"])

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

def rate():
    MaliciousVisualizer().compute()
