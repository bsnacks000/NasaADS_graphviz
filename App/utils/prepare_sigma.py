import pandas as pd

from numpy import cos, sin, pi
from numpy.random import randint
# prepare object in flask for sigma... takes a table name, calls
# this module will sit on the server in a utils folder ... from utils.prepare_sigma import PrepareSigma
# PrepareSigma objects get stored in session after creation


class PrepareSigma(object):

    def __init__(self, graph_name, db_path):
        self.graph_name = graph_name  # string from query '<subject>_<type>'
        self.db_path = db_path  # string ... sqlite:///./data/graph.db  databae file location path

        self.nodes = None
        self.edges = None

        self.sigma_obj = {}   # json object dictionary for sigma --> load this into session dict at app level

        # init methods
        self.__load_tables()
        self.__node_add_extra()
        self.__edge_weights()
        self.__make_json_obj()

    def __load_tables(self):
        # loads node and edge lists
        self.nodes = pd.read_sql_table(self.graph_name+'_nodes',self.db_path)
        self.edges = pd.read_sql_table(self.graph_name+'_edges',self.db_path)


    def __make_json_obj(self):
        # sets and returns obj dictionary with node and edge list arrays(sigma compatible)
        self.sigma_obj['nodes'] = self.nodes.to_dict('records')
        self.sigma_obj['edges'] = self.edges.to_dict('records')
        return self.sigma_obj

    def __node_add_extra(self):
        # adds extra stuff to the nodes list needed for sigma
        node_len = len(self.nodes)

        # spreads nodes in a circle for forceAtlas2
        x = 10 * cos(2 * randint(0,node_len,node_len) * pi/node_len)
        y = 10 * sin(2 * randint(0,node_len,node_len) * pi/node_len)

        # stuff for sigma nodes
        self.nodes['x'] = x
        self.nodes['y'] = y
        self.nodes['color'] = self.nodes.apply (lambda row: self.__choose_color(row), axis=1)
        self.nodes['size'] = 0.25 + 15 * self.nodes['zdeg_central']  # set to degree central


    def __choose_color(self, row):
        # arbitrary color choose for the node types used for above
        if row['node_type'] == 'Author':
            return "#7795c4"
        else:
            return '#79a55c'

    def __edge_weights(self):
        # if edges have weight attribute change column name to size
        if 'weight' in self.edges.columns:
            self.edges['size'] = self.edges['weight']
