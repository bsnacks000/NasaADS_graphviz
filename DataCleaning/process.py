#import ads.sandbox as ads
import ads
import pandas as pd
import numpy as np
import os

import networkx as nx
from networkx.algorithms import bipartite as bi


class ProcessADS(object):
    # query ADS and build initial graph edge_list and node_list
    # nodes and edges from this object go to ProcessGraph for networkx processing

    def __init__(self, q, key, max_pages):
        self.q = q  # query parameter string
        self.key = key # ADS dev key from outer scope
        self.max_pages = max_pages

        self.__nodes = None    # pandasDataFrames
        self.__edges = None

        self.__queryADS()

    def __queryADS(self):
        # queries ADS and builds initial node and edge lists for further processing
        ads.config.token = self.key
        papers = list(ads.SearchQuery(q=self.q, sort="citation_count",max_pages=self.max_pages))

        # <------ code dump from daina's ipython script ---->
        author_names = [i.author for i in papers]   # This code bottlenecks based on topic.. 5 - 60 secs
        journals = [i.pub for i in papers]

        # --added code here to limit author count by average authorship per query--
        author_names_limit, journals_limit = self.__limit_author_count(author_names,journals)
        # ------ end auth limit code -------#

        df = pd.DataFrame({'Author_Names' : author_names_limit,'Journal':journals_limit})   # changed to new limited lists
        s1 = df.apply(lambda x: pd.Series(x['Author_Names']),axis=1).stack().reset_index(level=1, drop=True)
        s1.name = 'Author_Name'

        self.__edges = df.drop('Author_Names', axis=1).join(s1).reset_index(level=1,drop=True)

        author_nodes = pd.DataFrame(self.__edges.Author_Name.unique(),columns=['label'])
        author_nodes['node_type'] = 'Author'
        journal_nodes = pd.DataFrame(self.__edges.Journal.unique(), columns=['label'])
        journal_nodes['node_type'] = 'Journal'

        # make nodes list: id, label, node_type
        self.__nodes = pd.concat([author_nodes, journal_nodes]).reset_index(drop=True)
        self.__nodes['id'] = self.__nodes.index

        # make source/target as ids on edge list data
        self.__edges = pd.merge(self.__edges,self.__nodes[(self.__nodes.node_type=='Journal')],
            how='left',left_on='Journal',right_on='label').drop(['node_type','label'],1).rename(columns={'id':'source'})
        self.__edges = pd.merge(self.__edges,self.__nodes[(self.__nodes.node_type=='Author')],
            how='left',left_on='Author_Name',right_on='label').drop(['node_type','label', 'Journal','Author_Name'],1).rename(columns={'id':'target'})
        self.__edges['id'] = self.__edges.index

        #< ---- end ipython code dump ---->

    def __average_author_count(self, author_names):
        lengths = [len(i) for i in author_names]
        return sum(lengths)/len(lengths)


    def __limit_author_count(self, author_names, journals):
        # replace code block above
        auth_limit = self.__average_author_count(author_names)

        author_names_limit = []
        journals_limit = []

        for i in range(len(author_names)):
            if len(author_names[i]) < auth_limit:
                author_names_limit.append(author_names[i])  # append to new lists if under limit
                journals_limit.append(journals[i])

        return author_names_limit, journals_limit

    # Public API

    @property
    def nodes(self):
        return self.__nodes

    @property
    def edges(self):
        return self.__edges



class ProcessGraph(object):
    # graph processing... can export 3 graphs as node/edgelist pair csvs

    def __init__(self, ads_obj):

        # ads_query object
        self.ads_obj = ads_obj

        # These are private... accessed with property
        # load raw node/edgelist from ads into nodes and edges
        self.__main_nodes = None
        self.__main_edges = None

        # initialize subgraph variables
        self.__lg_cc_nodes = None
        self.__lg_cc_edges = None

        self.__islands_nodes = None
        self.__islands_edges = None

        self.__g = None   # main networkx graph set in __make_graphs
        self.__lg_cc_subgraph = None    # copies of cc subgraph
        self.__islands_graph = None   # copies of islands_graph

        self.__init_nxgraph()
        self.__init_subgraphs()

        # add centrality here

    def __init_nxgraph(self):
        # get node attributes and attach to graph
        nd = self.ads_obj.nodes[['label','node_type','id']].to_dict('index')

        # transfer in initial attributes
        labels = {k:v['label'] for (k, v) in nd.iteritems()}
        ids = {k:v['id'] for (k,v) in nd.iteritems()}
        node_type = {k:v['node_type'] for (k,v) in nd.iteritems()}

        # networkx graph from edgelist
        self.__g = nx.from_pandas_dataframe(self.ads_obj.edges,'source','target')

        # set initial attributes from original node list
        nx.set_node_attributes(self.__g,'label',labels)
        nx.set_node_attributes(self.__g,'id',ids)
        nx.set_node_attributes(self.__g,'node_type',node_type)

        # <---- add centrality measures here as node attributes --->
        self.add_degree_centrality(self.__g)
        self.add_pagerank(self.__g)
        self.add_betweenness_centrality(self.__g)

        # set main dataframes
        self.__main_nodes, self.__main_edges = self.__to_pandas_df(self.__g)

    def __init_subgraphs(self):

        sg_largest = max(nx.connected_component_subgraphs(self.__g), key=len)  # wrap in error code?
        # split into bipartite on author and Journal

        Author, Journal = bi.sets(sg_largest)

        j_proj_sg_largest = bi.weighted_projected_graph(sg_largest, Journal)
        a_proj_sg_largest = bi.weighted_projected_graph(sg_largest, Author)

        a_sg_island =  self.__trim(a_proj_sg_largest)
        j_sg_island = self.__trim(j_proj_sg_largest)

        # merge subgraphs and islands into 2 seperate graphs
        self.__lg_cc_subgraph = self.__merge_graph(a_proj_sg_largest, j_proj_sg_largest)
        self.__islands_graph = self.__merge_graph(a_proj_sg_largest, j_proj_sg_largest)

        # <---- add centrality measures here as node attributes --->
        self.add_degree_centrality(self.__lg_cc_subgraph)
        self.add_pagerank(self.__lg_cc_subgraph)
        self.add_betweenness_centrality(self.__lg_cc_subgraph)

        self.add_degree_centrality(self.__islands_graph)
        self.add_pagerank(self.__islands_graph)
        self.add_betweenness_centrality(self.__islands_graph)

        # convert these to pandas dfs
        self.__lg_cc_nodes, self.__lg_cc_edges = self.__to_pandas_df(self.__lg_cc_subgraph)
        self.__islands_nodes, self.__islands_edges = self.__to_pandas_df(self.__islands_graph)

    def __trim(self, g, weight=1):
        # island method - trim weighted subgraphs on weight
        g_temp = nx.Graph()
        edge_bunch2 = [i for i in g.edges(data=True) if i[2]['weight'] > weight]
        g_temp.add_edges_from(edge_bunch2)
        return g_temp


    def __merge_graph(self, g, h):
        # merges graphs for export (islands and largest_cc)
        g = nx.compose(g,h)
        return g

    def __to_pandas_df(self,graph):
        # dumps graph data into pandas dfs... returns a node and edge dataframe
        # for nodes just need to dump attribute dictionary
        nodes = pd.DataFrame([graph.nodes(data=True)[i][1] for i in range(len(graph.nodes()))])

        # edges
        e = graph.edges(data=True)
        edgelist = [0 for i in xrange(len(graph.edges()))] # init for optimization (large edgelists)

        for i in range(len(edgelist)):
            edgelist[i] = {'id': i, 'source':e[i][0], 'target':e[i][1]}
            if (len(e[i][2]) != 0):   # if edge weight exists
                edgelist[i]['weight'] = e[i][2]['weight']

        edges = pd.DataFrame(edgelist)
        return nodes, edges

    # PUBLIC API

    # centrality processing
    def add_degree_centrality(self, graph):
        dc = nx.degree_centrality(graph)
        nx.set_node_attributes(graph, 'zdeg_central',dc)   # adding z to place at end of dataframe

    def add_betweenness_centrality(self,graph):
        bc = nx.betweenness_centrality(graph)
        nx.set_node_attributes(graph,'zbetween_central',bc)

    def add_pagerank(self, graph):
        pr = nx.pagerank(graph)
        nx.set_node_attributes(graph, 'zpagerank',pr)

    # getters for dataframes and graphs
    @property
    def main_nodes(self):
        return self.__main_nodes

    @property
    def main_edges(self):
        return self.__main_edges

    @property
    def lg_cc_nodes(self):
        return self.__lg_cc_nodes

    @property
    def lg_cc_edges(self):
        return self.__lg_cc_edges

    @property
    def island_nodes(self):
        return self.__islands_nodes

    @property
    def island_edges(self):
        return self.__islands_edges

    @property
    def g(self):
        return self.__g

    @property
    def lg_cc_subgraph(self):
        return self.__lg_cc_subgraph

    @property
    def islands_graph(self):
        return self.__islands_graph


    def export_main_to_csv(self):

        output_dir = os.getcwd() + '/csvs'  # make output sub-directory for csvs
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            self.__main_nodes.to_csv(
                os.path.join(output_dir +'/'+ self.ads_obj.q +"_main_nodes.csv"), encoding='utf-8', index=False)
            self.__main_edges.to_csv(
                os.path.join(output_dir +'/'+ self.ads_obj.q +"_main_edges.csv"), encoding='utf-8', index=False)

        except AttributeError as e:
            raise e('dataframes for main graph are not set')

    def export_subgraphs_to_csv(self):
        # same as above but exports subgraphs

        output_dir = os.getcwd() + '/csvs'  # make output sub-directory for csvs
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            self.__lg_cc_nodes.to_csv(
                os.path.join(output_dir +'/'+ self.ads_obj.q +"_lg_cc_nodes.csv"), encoding='utf-8', index=False)
            self.__lg_cc_edges.to_csv(
                os.path.join(output_dir +'/'+ self.ads_obj.q +"_lg_cc_edges.csv"), encoding='utf-8', index=False)
            self.__islands_nodes.to_csv(
                os.path.join(output_dir +'/'+ self.ads_obj.q +"_islands_nodes.csv"), encoding='utf-8', index=False)
            self.__islands_edges.to_csv(
                os.path.join(output_dir +'/'+ self.ads_obj.q +"_islands_edges.csv"), encoding='utf-8', index=False)

        except AttributeError as e:
            raise e('dataframes for subgraphs are not set')

if __name__ == '__main__':
    # need to test class here...
    pass
