from pathlib import Path
from collections import namedtuple, Counter
import time
import random

start=time.time()
with open(Path(__file__).parent / "../inputs/day23.txt") as file:
    lines = file.read().splitlines()

# lines = """kh-tc
# qp-kh
# de-cg
# ka-co
# yn-aq
# qp-ub
# cg-tb
# vc-aq
# tb-ka
# wh-tc
# yn-cg
# kh-ub
# ta-co
# de-co
# tc-td
# tb-wq
# wh-td
# ta-ka
# td-qp
# aq-cg
# wq-ub
# ub-vc
# de-ta
# wq-aq
# wq-vc
# wh-yn
# ka-de
# kh-ta
# co-tc
# wh-qp
# tb-vc
# td-yn""".splitlines()

class Graph:
    def __init__(self,vertices = set(),neighbours = dict(),num_edges = -1,memoized_cliques = dict()):
        self.vertices = vertices
        self.neighbours = neighbours
        self.num_vertices = len(vertices)
        self.num_edges = num_edges
        if num_edges == -1:
            self.num_edges = 0
            for v in self.vertices:
                self.num_edges += len(self.neighbours[v])
            self.num_edges //= 2
        # print(self.vertices)
        # print(self.neighbours)
        # print(self.num_vertices)
        # print(self.num_edges)
        # input()
        self.memoized_cliques = memoized_cliques
    def add_edge(self,v1,v2):
        if v1 not in self.vertices:
            self.vertices.add(v1)
            self.num_vertices += 1
            self.neighbours[v1] = set()
        if v2 not in self.vertices:
            self.vertices.add(v2)
            self.num_vertices += 1
            self.neighbours[v2] = set()
        if v2 not in self.neighbours[v1]:
            self.neighbours[v1].add(v2)
            self.neighbours[v2].add(v1)
            self.num_edges += 1
    def is_complete(self):
        return (self.num_vertices*(self.num_vertices-1))//2 == self.num_edges
    def count_triangles(self):
        count = 0
        for v1 in self.vertices:
            n1 = self.neighbours[v1]
            for v2 in n1:
                n2 = self.neighbours[v2]
                # print(v1,v2)
                # print(n1,n2)
                count += len(n1.intersection(n2))
        return count//6
    def count_t_triangles(self):
        triangles = set()
        for v1 in self.vertices:
            n1 = self.neighbours[v1]
            for v2 in n1:
                n2 = self.neighbours[v2]
                # print(v1,v2)
                # print(n1,n2)
                for v3 in n1.intersection(n2):
                    if v3[0] == "t":
                        triangles.add(frozenset({v1,v2,v3}))
                
        return len(triangles)
    def removed_vertex(self,vertex):
        # print("removing vertex",vertex,"from graph")
        new_vertices = self.vertices.difference({vertex})
        new_nbrs = dict_level2_copy(self.neighbours) ### HAS TO BE A DEEP COPY
        vertex_nbrs = new_nbrs.pop(vertex)
        new_num_edges = self.num_edges - len(vertex_nbrs)
        for nbr in vertex_nbrs:
            new_nbrs[nbr].remove(vertex)
    
        return Graph(new_vertices,new_nbrs,new_num_edges,self.memoized_cliques)
    def subgraph(self,vertices):
        new_nbrs = {}
        for vertex in vertices:
            new_nbrs[vertex] = self.neighbours[vertex].intersection(vertices)
        return Graph(vertices,new_nbrs)
    def remove_vertex(self,vertex):
        # print("removing vertex",vertex,"from graph")
        new_vertices = self.vertices.difference({vertex})
        new_nbrs = dict_level2_copy(self.neighbours) ### HAS TO BE A DEEP COPY
        vertex_nbrs = new_nbrs.pop(vertex)
        new_num_edges = self.num_edges - len(vertex_nbrs)
        for nbr in vertex_nbrs:
            new_nbrs[nbr].remove(vertex)
        self.vertices = new_vertices
        self.neighbours = new_nbrs
        self.num_vertices -= 1
        self.num_edges = new_num_edges
    def find_maximal_clique(self):
        if len(self.memoized_cliques)%10 == 0:
            print(len(self.memoized_cliques))
        best_clique = 0
        frozen_vertices = frozenset(self.vertices)
        if frozen_vertices in self.memoized_cliques:
            # print("this clique is memoized!")
            return self.memoized_cliques[frozen_vertices],self.memoized_cliques
        if self.is_complete():
            self.memoized_cliques[frozen_vertices] = self.num_vertices
            # print("this graph is complete!")
            return self.num_vertices,self.memoized_cliques
        for vertex in self.vertices:
            # print("-- main graph --")
            # print("vertices:",self.vertices)
            # print("nbrs:",self.neighbours)
            # print("num vertices:",self.num_vertices)
            # print("num edges:",self.num_edges)
            subgraph = self.removed_vertex(vertex)
            # print("-- subgraph removing vertex",vertex,"--")
            # print("vertices:",subgraph.vertices)
            # print("nbrs:",subgraph.neighbours)
            # print("num vertices:",subgraph.num_vertices)
            # print("num edges:",subgraph.num_edges)
            result,self.memoized_cliques = subgraph.find_maximal_clique()
            if result > best_clique:
                best_clique = result
            self.remove_vertex(vertex)
            
        self.memoized_cliques[frozen_vertices] = best_clique
        return best_clique,self.memoized_cliques
    def find_maximal_clique2(self):
        
        if self.is_complete():
            # print("is complete")
            # print(self.vertices)
            return self.vertices
        for vertex in self.vertices:
            break
        
        # print("vertex",vertex)
        best_with_vertex = self.subgraph(self.neighbours[vertex]).find_maximal_clique2().union({vertex})
        # print(best_with_vertex)
        best_without_vertex = self.subgraph(self.vertices.difference({vertex})).find_maximal_clique2()
        # print(best_without_vertex)
        if len(best_with_vertex) > len(best_without_vertex):
            return best_with_vertex
        return best_without_vertex

def dict_level2_copy(dictionary):
    new_dict = {}
    keys = dictionary.keys()
    for key in keys:
        new_dict[key] = dictionary[key].copy()
    return new_dict

def random_graph(n,p):
    # vertices = set(range(n))
    graph = Graph()
    for i in range(n):
        for j in range(i+1,n):
            if random.random() < p:
                graph.add_edge(i,j)
    return graph

day23graph = Graph()
for line in lines:
    v1,v2 = line.split("-")
    day23graph.add_edge(v1,v2)

# day23graph = random_graph(17,0.5)
# day23graph.add_edge("1","4")
# day23graph.add_edge("2","4")

# print(day23graph.vertices)
# print(day23graph.neighbours)

# print(day23graph.num_vertices)
# print(day23graph.num_edges)
# print(day23graph.count_triangles())
result1 = day23graph.count_t_triangles()
print(result1)


best_clique = sorted(list(day23graph.find_maximal_clique2()))
result2 = ",".join(best_clique)
end = time.time()
print(result2)
print(end-start)