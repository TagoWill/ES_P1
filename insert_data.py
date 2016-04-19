from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import User, Base, Car, Dealership

engine = create_engine('mysql+pymysql://esproject:esproject@esteste.clw9xldhi2rc.eu-west-1.rds.amazonaws.com:3306/esproject1')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Insert a User
new_client = User(name='Tiago', type='client', email='tiago@gmail.pt', password='123')
session.add(new_client)
session.commit()

# Insert a User
new_client2 = User(name='Joao', type='client', email='joao@gmail.pt', password='123')
session.add(new_client2)
session.commit()

# Insert a User
new_owner = User(name='Daniel', type='owner', email='dbastos@gmail.pt', password='123')
session.add(new_owner)
session.commit()

# Insert a User
new_owner2 = User(name='Pedro', type='owner', email='pedro@gmail.pt', password='123')
session.add(new_owner2)
session.commit()

# Insert a User
new_owner3 = User(name='Andreia', type='owner', email='andreia@gmail.pt', password='123')
session.add(new_owner3)
session.commit()

# Insert a User
new_owner4 = User(name='Fabio', type='owner', email='fabio@gmail.pt', password='123')
session.add(new_owner4)
session.commit()

# Insert a User
new_owner5 = User(name='Catia', type='owner', email='catia@gmail.pt', password='123')
session.add(new_owner5)
session.commit()

# Insert a Car
new_car = Car(brand='Audi', model='A3', fuel='Diesel', price=20000, kms=100000, year=2000,
              owner_id=new_owner4.userid)
session.add(new_car)
session.commit()

# Insert a Car
new_car2 = Car(brand='BMW', model='320i', fuel='Gasoline', price=25000, kms=250000, year=1999,
               owner_id=new_owner.userid)
session.add(new_car2)
session.commit()

# Insert a Car
new_car3 = Car(brand='BMW', model='M5', fuel='Gasoline', price=45000, kms=300000, year=2005,
               owner_id=new_owner.userid)
session.add(new_car3)
session.commit()

# Insert a Car
new_car4 = Car(brand='Ferrari', model='Enzo', fuel='Gasoline', price=50000, kms=110000, year=1990,
               owner_id=new_owner3.userid)
session.add(new_car4)
session.commit()

# Insert a Car
new_car5 = Car(brand='Ford', model='Fiesta', fuel='Diesel', price=5000, kms=150000, year=2007,
               owner_id=new_owner3.userid)
session.add(new_car5)
session.commit()

# Insert a Car
new_car6 = Car(brand='Opel', model='Insignia', fuel='Diesel', price=17000, kms=50000, year=2010,
               owner_id=new_owner5.userid)
session.add(new_car6)
session.commit()

# Insert a Car
new_car7 = Car(brand='Seat', model='Ibiza', fuel='Diesel', price=7000, kms=70000, year=2013,
               owner_id=new_owner2.userid)
session.add(new_car7)
session.commit()

# Insert a Car
new_car8 = Car(brand='Volkswagen', model='Astra', fuel='Diesel', price=13000, kms=160000, year=2009,
               owner_id=new_owner5.userid)
session.add(new_car8)
session.commit()

# Insert a Dealership
new_deal = Dealership(name='StandDaniel', contact=919999999, district='Aveiro', seller_id=new_owner.userid)
session.add(new_deal)
session.commit()

# Insert a Car
new_car2 = Car(brand='Mercedes', model='SLK200', fuel='Gasoline', price=30000, kms=220000, year=1989,
               owner_id=new_owner.userid)
new_car2.mydealership.append(new_deal)
session.add(new_car2)
session.commit()

# Insert a Dealership
new_deal2 = Dealership(name='StandPedro', contact=929999999, district='Lisboa', seller_id=new_owner2.userid)
session.add(new_deal2)
session.commit()

# Insert a Dealership
new_deal3 = Dealership(name='StandAndreia', contact=939999999, district='Coimbra', seller_id=new_owner3.userid)
session.add(new_deal3)
session.commit()

# Insert a Dealership
new_deal4 = Dealership(name='StandFabio', contact=949999999, district='Porto', seller_id=new_owner4.userid)
session.add(new_deal4)
session.commit()

# Insert a Dealership
new_deal5 = Dealership(name='StandCatia', contact=959999999, district='Aveiro', seller_id=new_owner5.userid)
session.add(new_deal5)
session.commit()

session.close()
