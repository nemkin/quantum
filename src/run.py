from tqdm import tqdm
import pydng
import time
import numpy as np


class Run:

  def make_name(self):
    time_part = time.strftime('%Y_%m_%d__%H_%M_%S')
    unique_part = pydng.generate_name()
    return f"{time_part}_{unique_part}"

  def mixing_time(counts):
    n = len(counts)
    diffarray = np.zeros(n-1)
    for i in range(n-1):
      diffarray[i] = np.linalg.norm(counts[i+1]-counts[i])
    return diffarray

  def hitting_time(counts):
    # https://stackoverflow.com/a/47269413
    mask = (counts != 0)
    axis = 0
    invalid_value = -1
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_value)

  def get_simulation(graph, simulator):
    counts = simulator.simulate(graph)
    mixing_time = Run.mixing_time(counts)
    hitting_time = Run.hitting_time(counts)
    return {
        "simulator": simulator,
        "counts": counts,
        "mixing_time": mixing_time,
        "hitting_time": hitting_time
    }

  def __init__(self, graph, simulators):
    self.name = self.make_name()
    self.N = graph.vertex_count()
    self.graph_adj = graph.adjacency_matrix()
    self.coin_faces = graph.coin_faces()
    self.sub_graphs = map(
        lambda sub_graph: {
            "describe": sub_graph.describe(),
            "adj": sub_graph.adjacency_matrix(self.N)
        },
        tqdm(graph.sub_graphs,
             desc=f"{graph.name} subgraph adjacency matrices", leave=False)
    )
    self.simulations = map(
        lambda s: Run.get_simulation(graph, s),
        tqdm(simulators, desc=f"{graph.name} simulations",
             leave=False)
    )
