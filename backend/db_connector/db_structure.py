from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Administrator(Base):
    __tablename__ = 'administrator'

    id = Column(Integer, primary_key=True, server_default=text("nextval('administrator_id_seq'::regclass)"))


class Przodownik(Base):
    __tablename__ = 'przodownik'

    id = Column(Integer, primary_key=True, server_default=text("nextval('przodownik_id_seq'::regclass)"))
    data_wygasniecia_legitymacji = Column(Date)


class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True, server_default=text("nextval('region_id_seq'::regclass)"))
    nazwa = Column(String(255))


class StatusTrasy(Base):
    __tablename__ = 'status_trasy'

    id = Column(Integer, primary_key=True, server_default=text("nextval('status_trasy_id_seq'::regclass)"))
    nazwa = Column(String(255))


class Turysta(Base):
    __tablename__ = 'turysta'

    id = Column(Integer, primary_key=True, server_default=text("nextval('turysta_id_seq'::regclass)"))
    data_urodzenia = Column(Date)
    punkty_z_poprzedniej_odznaki = Column(Integer)


class TypOdznaki(Base):
    __tablename__ = 'typ_odznaki'

    id = Column(Integer, primary_key=True, server_default=text("nextval('typ_odznaki_id_seq'::regclass)"))
    nazwa = Column(String(255))


class Wezel(Base):
    __tablename__ = 'wezel'

    id = Column(Integer, primary_key=True, server_default=text("nextval('wezel_id_seq'::regclass)"))
    nazwa = Column(String(255))
    wspolrzedna_x = Column(Float, nullable=False)
    wspolrzedna_y = Column(Float, nullable=False)


class Got(Base):
    __tablename__ = 'got'

    id = Column(Integer, primary_key=True, server_default=text("nextval('got_id_seq'::regclass)"))
    turysta_id = Column(ForeignKey('turysta.id'), nullable=False)
    typ_odznaki = Column(Integer, nullable=False)
    data_zdobycia = Column(Date)
    wartosc_punktowa_got = Column(Integer)

    turysta = relationship('Turysta')


class Odcinek(Base):
    __tablename__ = 'odcinek'

    id = Column(Integer, primary_key=True, server_default=text("nextval('odcinek_id_seq'::regclass)"))
    region_id = Column(ForeignKey('region.id'), nullable=False)
    wezel_id2 = Column(ForeignKey('wezel.id'), nullable=False)
    wezel_id = Column(ForeignKey('wezel.id'), nullable=False)
    punkty_got_w_kierunku = Column(Integer, nullable=False)
    punkty_got_w_przeciwnym_kierunku = Column(Integer)
    nazwa = Column(String(255))
    odleglosc = Column(Integer, nullable=False)
    suma_podejsc = Column(Integer, nullable=False)
    suma_zejsc = Column(Integer, nullable=False)

    region = relationship('Region')
    wezel = relationship('Wezel', primaryjoin='Odcinek.wezel_id == Wezel.id')
    wezel1 = relationship('Wezel', primaryjoin='Odcinek.wezel_id2 == Wezel.id')


class Uprawnienia(Base):
    __tablename__ = 'uprawnienia'

    id = Column(Integer, primary_key=True, server_default=text("nextval('uprawnienia_id_seq'::regclass)"))
    administrator_id = Column(ForeignKey('administrator.id'), nullable=False)
    region_id = Column(ForeignKey('region.id'), nullable=False)
    przodownik_id = Column(ForeignKey('przodownik.id'), nullable=False)

    administrator = relationship('Administrator')
    przodownik = relationship('Przodownik')
    region = relationship('Region')


class Trasa(Base):
    __tablename__ = 'trasa'

    id = Column(Integer, primary_key=True, server_default=text("nextval('trasa_id_seq'::regclass)"))
    nazwa = Column(String, nullable=False)
    turysta_id = Column(ForeignKey('turysta.id'), nullable=False)
    got_id = Column(ForeignKey('got.id'))
    punkty_got = Column(Integer, nullable=False)
    status = Column(ForeignKey('status_trasy.id'))
    data_zweryfikowania = Column(Date)

    got = relationship('Got')
    turysta = relationship('Turysta')
    status_trasy = relationship('StatusTrasy')


class Zamkniecie(Base):
    __tablename__ = 'zamkniecie'

    id = Column(Integer, primary_key=True, server_default=text("nextval('zamkniecie_id_seq'::regclass)"))
    odcinek_id = Column(ForeignKey('odcinek.id'), nullable=False)

    odcinek = relationship('Odcinek')


class DokumentacjaTrasy(Base):
    __tablename__ = 'dokumentacja_trasy'

    id = Column(Integer, primary_key=True, server_default=text("nextval('dokumentacja_trasy_id_seq'::regclass)"))
    trasa_id = Column(ForeignKey('trasa.id'), nullable=False)

    trasa = relationship('Trasa')


class OdcinekTrasy(Base):
    __tablename__ = 'odcinek_trasy'

    id = Column(Integer, primary_key=True, server_default=text("nextval('odcinek_trasy_id_seq'::regclass)"))
    odcinek_id = Column(ForeignKey('odcinek.id'), nullable=False)
    trasa_id = Column(ForeignKey('trasa.id'), nullable=False)
    punkty_got = Column(Integer)
    kierunek = Column(Boolean)

    odcinek = relationship('Odcinek')
    trasa = relationship('Trasa')
