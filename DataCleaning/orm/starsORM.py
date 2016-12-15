# each subject ORM imports the baseORM module
from baseORM import *

#------------Stars-------------------#
class StarsMainNodes(Base, BaseNodes):
    __tablename__ = 'stars_main_nodes'

class StarsMainEdges(Base, BaseEdges):
    __tablename__ = 'stars_main_edges'

class StarsAuthorLgCcNodes(Base, BaseNodes):
    __tablename__ = 'stars_a_lg_cc_nodes'

class StarsAuthorLgCcEdges(Base, BaseEdgesSubgraph):
    __tablename__ = 'stars_a_lg_cc_edges'

class StarsJournalLgCcNodes(Base, BaseNodes):
    __tablename__ = 'stars_j_lg_cc_nodes'

class StarsJournalLgCcEdges(Base, BaseEdgesSubgraph):
    __tablename__ = 'stars_j_lg_cc_edges'    

class StarsIslandsNodes(Base, BaseNodes):
    __tablename__ = 'stars_islands_nodes'

class StarsIslandsEdges(Base, BaseEdgesSubgraph):
    __tablename__ = 'stars_islands_edges'
