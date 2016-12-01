from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Numeric, String

# Table Schema Base Classes

Base = declarative_base()

class BaseNodes(object):
    # fields for All Node tables
    id = Column(Integer, primary_key=True)
    label = Column(String(100))
    node_type = Column(String(10))
    zbetween_central = Column(Numeric())
    zdeg_central = Column(Numeric())
    zpagerank = Column(Numeric())

class BaseEdges(object):
    # fields for all Edge Tables
    id = Column(Integer, primary_key=True)
    source = Column(Integer())
    target = Column(Integer())

class BaseEdgesSubgraph(BaseEdges):
    # fields for subgraph edges
    weight = Column(Integer())
