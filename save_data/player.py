from sqlalchemy import Column, String, Integer, Float

from base import Base

class Player(Base):
	__tablename__ = 'players'

	id = Column(String, primary_key=True)
	peso = Column(Float)
	aniosE = Column(Float)
	aIMunieca = Column(String)
	aFMunieca = Column(Float)
	stdMunieca = Column(Float)
	aICodo = Column(Float)
	aFCodo = Column(Float)
	stdCodo = Column(Float)
	aIHombro = Column(Float)
	aFHombro = Column(Float)
	stdHombro = Column(Float)
	aICadera = Column(Float)
	aFCadera = Column(Float)
	stdCadera = Column(Float)
	aIRodilla = Column(Float)
	aFRodilla = Column(Float)
	stdRodilla = Column(Float)
	aITobillo = Column(Float)
	aFTobillo = Column(Float)
	stdTobillo = Column(Float)
	efectividad = Column(Float)

	def __init__(self,
        id,
        peso,
        aniosE,
        aIMunieca,
        aFMunieca,
        stdMunieca,
        aICodo,
        aFCodo,
        stdCodo,
        aIHombro,
        aFHombro,
        stdHombro,
        aICadera,
        aFCadera,
        stdCadera,
        aIRodilla,
        aFRodilla,
        stdRodilla,
        aITobillo,
        aFTobillo,
        stdTobillo,
        efectividad):
          self.id = id
          self.peso = peso
          self.aniosE = aniosE
          self.aIMunieca =  aIMunieca
          self.aFMunieca =  aFMunieca
          self.stdMunieca = stdMunieca
          self.aICodo = aICodo
          self.aFCodo = aFCodo
          self.stdCodo =  stdCodo
          self.aIHombro = aIHombro
          self.aFHombro = aFHombro
          self.stdHombro =  stdHombro
          self.aICadera = aICadera
          self.aFCadera = aFCadera
          self.stdCadera =  stdCadera
          self.aIRodilla =  aIRodilla
          self.aFRodilla =  aFRodilla
          self.stdRodilla = stdRodilla
          self.aITobillo =  aITobillo
          self.aFTobillo =  aFTobillo
          self.stdTobillo = stdTobillo
          self.efectividad = efectividad