from baseORM import *

#-------exoplanet astronomy-------#
class ExoplanetMainNodes(Base, BaseNodes):
    __tablename__ = 'exoplanet_astronomy_main_nodes'

class ExoplanetMainEdges(Base, BaseEdges):
    __tablename__ = 'exoplanet_astronomy_main_edges'

class ExoplanetAuthorLgCcNodes(Base, BaseNodes):
    __tablename__ = 'exoplanet_astronomy_a_lg_cc_nodes'

class ExoplanetAuthorLgCcEdges(Base, BaseEdgesSubgraph):
    __tablename__ = 'exoplanet_astronomy_a_lg_cc_edges'

class ExoplanetJournalLgCcNodes(Base, BaseNodes):
    __tablename__ = 'exoplanet_astronomy_j_lg_cc_nodes'

class ExoplanetJournalLgCcEdges(Base, BaseEdgesSubgraph):
    __tablename__ = 'exoplanet_astronomy_j_lg_cc_edges'

class ExoplanetIslandsNodes(Base, BaseNodes):
    __tablename__ = 'exoplanet_astronomy_islands_nodes'

class ExoplanetIslandsEdges(Base, BaseEdgesSubgraph):
    __tablename__ = 'exoplanet_astronomy_islands_edges'
