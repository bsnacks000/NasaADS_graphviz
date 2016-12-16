from baseORM import *

#------------High Energy Astrophysics-------------------#
class HighEnergyMainNodes(Base, BaseNodes):
    __tablename__ = 'high_energy_astrophysics_main_nodes'

class HighEnergyMainEdges(Base, BaseEdges):
    __tablename__ = 'high_energy_astrophysics_main_edges'

class HighEnergyAuthorLgCcNodes(Base, BaseNodes):
    __tablename__ = 'high_energy_astrophysics_a_lg_cc_nodes'

class HighEnergyAuthorLgCcEdges(Base, BaseEdgesSubgraph):
    __tablename__ = 'high_energy_astrophysics_a_lg_cc_edges'

class HighEnergyJournalLgCcNodes(Base, BaseNodes):
    __tablename__ = 'high_energy_astrophysics_j_lg_cc_nodes'

class HighEnergyJournalLgCcEdges(Base, BaseEdgesSubgraph):
    __tablename__ = 'high_energy_astrophysics_j_lg_cc_edges'

class HighEnergyIslandsNodes(Base, BaseNodes):
    __tablename__ = 'high_energy_astrophysics_islands_nodes'

class HighEnergyIslandsEdges(Base, BaseEdgesSubgraph):
    __tablename__ = 'high_energy_astrophysics_islands_edges'
