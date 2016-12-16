from baseORM import *

#---------Cosmology----------#
class CosmologyMainNodes(Base, BaseNodes):
    __tablename__ = 'cosmology_main_nodes'

class CosmologyMainEdges(Base, BaseEdges):
    __tablename__ = 'cosmology_main_edges'

class CosmologyAuthorLgCcNodes(Base, BaseNodes):
    __tablename__ = 'cosmology_a_lg_cc_nodes'

class CosmologyAuthorLgCcEdges(Base, BaseEdgesSubgraph):
    __tablename__ = 'cosmology_a_lg_cc_edges'

class CosmologyJournalLgCcNodes(Base, BaseNodes):
    __tablename__ = 'cosmology_j_lg_cc_nodes'

class CosmologyJournalLgCcEdges(Base, BaseEdgesSubgraph):
    __tablename__ = 'cosmology_j_lg_cc_edges'

class CosmologyIslandsNodes(Base, BaseNodes):
    __tablename__ = 'cosmology_islands_nodes'

class CosmologyIslandsEdges(Base, BaseEdgesSubgraph):
    __tablename__ = 'cosmology_islands_edges'
