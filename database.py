import datetime
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

class Utilisateurs(Base):
    __tablename__ = 'utilisateurs'
    id = Column(String, primary_key=True)
    nom = Column(String(250),nullable=False)
    user_type = Column(String(250), nullable=False)
    mot_de_passe = Column(String(250))
    
class Clients(Base):
    __tablename__='clients'
    id_client = Column(Integer, primary_key=True, autoincrement=True)
    client_ssn_id = Column(Integer, unique=True)
    nom = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    age = Column(Integer)
    pays = Column(String(250), nullable=False)
    ville = Column(String(250), nullable=False)
    statut = Column(String(250), nullable=False)

class Carnet_client(Base):
    __tablename__='carnet_client'
    id_carnet = Column(Integer, primary_key=True, autoincrement=True)
    id_client = Column(Integer, ForeignKey('clients.id_client'))
    message_enregistrement = Column(String(250), nullable=False)
    heure_sortir = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)

class Comptes(Base):
    __tablename__='comptes'
    id_compte = Column(Integer,primary_key=True,autoincrement=True)
    type_de_compte = Column(String(250),nullable=False)
    balance = Column(Integer, nullable=False)
    id_client = Column(Integer, ForeignKey('clients.id_client'))
    clients = relationship(Clients)
    statut = Column(String(250), nullable=False)
    message =  Column(String(250))
    dernier_majour = Column(DateTime)

class Transactions(Base):
    __tablename__="transactions"
    trans_id = Column(Integer, primary_key=True, autoincrement=True)
    id_compte = Column(Integer, ForeignKey('comptes.id_compte'))
    trans_message = Column(String(250), nullable=False)
    montant = Column(Integer, nullable=False)
    heure_sortir = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)
    
engine = create_engine('sqlite:///mokobank.db')
Base.metadata.create_all(engine)