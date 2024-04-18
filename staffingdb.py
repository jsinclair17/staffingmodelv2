import sqlite3           
import math
# Class definitions sqlite

class ProjectAdd:
    def __init__(self, 
                 name
                 #, address
                 , projectname
                 , projecttype
                 , complexity
                 , innovation
                 , cost
                 , time_to_market
                 , expertise
                 #, laws
                 #, criticallity
                 , availability
                 #, timezone
                 , nearshore_cb
                 , offshore_cb
                #, scalability
                ):
        self.name = name
        #self.address = address
        self.projectname = projectname
        self.projecttype = projecttype
        self.cost = cost
        self.time_to_market = time_to_market
        #self.criticallity = criticallity
        #self.timezone = timezone
        self.complexity = complexity
        self.expertise = expertise
        #self.laws = laws
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
        on_shore_complex_wt = 0.22
        off_shore_complex_wt = 0.07
        near_shore_complex_wt = 0.07
        on_shore_innovate_wt = 0.22
        off_shore_innovate_wt = 0.07
        near_shore_innovate_wt = 0.07
        on_shore_speed_wt = 0.17
        off_shore_speed_wt = 0.11
        near_shore_speed_wt = 0.09
        on_shore_expertise_wt = 0.17
        off_shore_expertise_wt = 0.07
        near_shore_expertise_wt = 0.07
        on_shore_accessible_wt = 0.17
        off_shore_accessible_wt = 0.08
        near_shore_accessible_wt = 0.09
        on_shore_cost_wt = 0.2
        off_shore_cost_wt = 0.2
        near_shore_cost_wt = 0.2
        on_shore_score = on_shore_complex_wt*(self.complexity + 1) + on_shore_innovate_wt*(self.innovation) + on_shore_speed_wt*(7-self.time_to_market) + on_shore_expertise_wt*(self.expertise) + on_shore_accessible_wt*(self.availability) + on_shore_cost_wt*(7-self.cost)
        near_shore_score =  near_shore_complex_wt*(7-self.complexity) + near_shore_innovate_wt*(6-self.innovation) + near_shore_speed_wt*(self.time_to_market) + near_shore_expertise_wt*(6-self.expertise) + near_shore_accessible_wt*(self.availability) + near_shore_cost_wt*(self.cost)
        off_shore_score =  off_shore_complex_wt*(7-self.complexity) + off_shore_innovate_wt*(6-self.innovation) + off_shore_speed_wt*(self.time_to_market) + off_shore_expertise_wt*(6-self.expertise) + off_shore_accessible_wt*(6-self.availability) + off_shore_cost_wt*(self.cost)                                                                                                                                                                                                                           
        on_shore_spread = on_shore_score/(on_shore_score + near_shore_score + off_shore_score)
        near_shore_spread = near_shore_score/(on_shore_score + near_shore_score + off_shore_score)
        off_shore_spread = off_shore_score/(on_shore_score + near_shore_score + off_shore_score)
        if self.availability >=4:
            near_shore_spread = (near_shore_score + off_shore_score)/(on_shore_score + near_shore_score + off_shore_score)
            off_shore_spread = 0   
        if self.nearshore_cb == True and self.offshore_cb == True:
            on_shore_spread = on_shore_spread
            near_shore_spread = near_shore_spread
            off_shore_spread = off_shore_spread
        elif self.nearshore_cb == False and self.offshore_cb == True:
            on_shore_spread = on_shore_spread
            off_shore_spread = off_shore_spread + near_shore_spread
            near_shore_spread = 0
        elif self.nearshore_cb == True and self.offshore_cb == False:
            on_shore_spread = on_shore_spread
            near_shore_spread = off_shore_spread + near_shore_spread
            off_shore_spread = 0
        else:
            on_shore_spread = 1
            near_shore_spread = 0
            off_shore_spread = 0
        low_savings_calc = '{:.0%}'.format((1-(((on_shore_cost*on_shore_spread) + (off_shore_cost*off_shore_spread) + (near_shore_cost*near_shore_spread) )/ on_shore_cost))-0.05)
        high_savings_calc = '{:.0%}'.format((1-(((on_shore_cost*on_shore_spread) + (off_shore_cost*off_shore_spread) + (near_shore_cost*near_shore_spread) )/ on_shore_cost))+0.05) 
        return [[('On Shore',on_shore_spread), ('Off Shore',off_shore_spread), ('Near Shore', near_shore_spread)],(low_savings_calc, high_savings_calc)]
       