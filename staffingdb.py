import sqlite3           
import math
# Class definitions sqlite

class ProjectAdd:
    def __init__(self, 
                 name
                 #, address
                 , projectname
                 , projecttype
                 #, 
                 #cost
                 , complexity
                 , innovation
                 , time_to_market
                 , expertise
                 , laws
                 #, criticallity
                 , availability
                 , timezone
                 , nearshore_cb
                 , offshore_cb
                #, scalability
                ):
        self.name = name
        #self.address = address
        self.projectname = projectname
        self.projecttype = projecttype
        #self.cost = cost
        self.time_to_market = time_to_market
        #self.criticallity = criticallity
        self.timezone = timezone
        self.complexity = complexity
        self.expertise = expertise
        self.laws = laws
        self.availability = availability
        self.innovation = innovation
        self.nearshore_cb = nearshore_cb
        self.offshore_cb = offshore_cb
        #self.scalability = scalability

    def save(self):
        conn = sqlite3.connect('Staffing.db')
        c = conn.cursor()
        # Create tables if they don't exist
        c.execute('''CREATE TABLE IF NOT EXISTS projectdetail 
                    (name text, address text, projectname text, projecttype text, cost int, time_to_market text, timezone int, complexity int, expertise int, laws int
                , availability int, innovation int)''')
        c.execute('''INSERT INTO projectdetail (name, address, projectname, projecttype, cost, time_to_market, timezone, complexity, expertise, laws
                , availability, innovation) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                  (self.name
                   #, self.address
                   , self.projectname, self.projecttype, self.cost, self.time_to_market
                   #, self.criticallity
                   , self.timezone, self.complexity, self.expertise
                   , self.laws, self.availability, self.innovation
                   #, self.scalability
                   ))
        conn.commit()

    def getspread(self):
        on_shore_cost = 210
        near_shore_cost = 140
        off_shore_cost = 110
        on_shore_spread = ((((6-self.time_to_market) + self.timezone + self.complexity + self.expertise + self.laws + self.availability + self.innovation)/7)/6) + 0.05
        if self.timezone >=4 or self.availability >=4 :
            near_shore_spread = 1 - ((((6-self.time_to_market) + self.timezone + self.complexity + self.expertise + self.laws + self.availability + self.innovation)/7)/6) - 0.05
        else:
            near_shore_spread = ((1-(((6-self.time_to_market) + self.timezone + self.complexity + self.expertise + self.laws + self.availability + self.innovation)/7)/6)*.4) - 0.02
        if self.timezone >=4 or self.availability >=4:
            off_shore_spread = 0
        else:
            off_shore_spread = ((1-(((6-self.time_to_market) + self.timezone + self.complexity + self.expertise + self.laws + self.availability + self.innovation)/7)/6)*.6) - 0.03
        low_savings_calc = '{:.0%}'.format((1-(((on_shore_cost*on_shore_spread) + (off_shore_cost*off_shore_spread) + (near_shore_cost*near_shore_spread) )/ on_shore_cost))-0.05)
        high_savings_calc = '{:.0%}'.format((1-(((on_shore_cost*on_shore_spread) + (off_shore_cost*off_shore_spread) + (near_shore_cost*near_shore_spread) )/ on_shore_cost))+0.05) 
        return [[('On Shore',on_shore_spread), ('Off Shore',off_shore_spread) , ('Near Shore', near_shore_spread)],(low_savings_calc, high_savings_calc)]
       