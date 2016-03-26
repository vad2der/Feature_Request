from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
import json

Base = declarative_base()


class ClientName(enum.Enum):
    """
    class to declare enum on possible client names
    """
    CLIENT_A = 'Client A'
    CLIENT_B = 'Client B'
    CLIENT_C = 'Client C'


class ProductArea(enum.Enum):
    """
    class to declare enum in possible product areas
    """
    POLICIES = 'Policies'
    BILLING = 'Billing'
    CLAIM = 'Claims'
    REPORTS = 'Reports'


# Model classes to declare schema of the DB
class RequestTicket(Base):
    """
    Schema to declare table of requests

    """
    __tablename__ = 'request_ticket'
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    title = Column(String(50))
    description = Column(String(200))
    client = Column(Enum('Client A', 'Client B', 'Client C'))
    client_priority = Column(Integer)
    target_date = Column(DateTime)
    ticket_url = Column(String(100))
    product_area = Column(Enum('Policies', 'Billing', 'Claims', 'Reports'))

    def __init__(self, ind, title, description, client, client_priority, target_date, ticket_url, product_area):
        self.id = ind
        self.title = str(title)
        self.description = str(description)
        self.client = client
        self.client_priority = int(client_priority)
        self.target_date = target_date
        self.ticket_url = ticket_url     # to be updated right after getting an id
        self.product_area = product_area

    def __str__(self):
        return json.dumps(self.serialize, indent=4)

    def __repr__(self):
        return json.dumps(self.serialize)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {u"id": self.id,
                u"title": self.title,
                u"description": self.description,
                u"client": self.client,
                u"client_priority": self.client_priority,
                u"target_date": str(self.target_date),
                u"ticket_url": str(self.ticket_url),
                u"product_area": self.product_area}