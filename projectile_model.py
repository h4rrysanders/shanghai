# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 13:51:30 2023

@author: harry sanders
"""

import math
from matplotlib import pyplot as plt

###############
#function: 
#description:    
#parameters:
#return:
###############


###############
#function: deg_to_rad
#description: converts degrees to radians
#parameters: deg; float
#return: radian conversion rounded to 7 decimal places
###############
def deg_to_rad(deg):
    return round(deg * (math.pi / 180), 7)

###############
#function: rad_to_deg
#description: converts radians to degrees   
#parameters: rad; float
#return: degrees conversion rounded to 1 decimal place
###############
def rad_to_deg(rad):
    return round(rad * (180/math.pi), 1)

# Projectile Class
class Projectile:
    ###############
    #function: Projectile constructor
    #description: initialises variables for Projectile
    #parameters: u; float, v; float, theta; float
    #return: None
    ###############
    def __init__(self, u, v, theta):
        self. u = float(u) # angular velocity
        self.v = float(v) # horizontal velocity
        self.theta = deg_to_rad(float(theta)) # angle of projection in radians
        
        self.range = None # maximum horizontal displacement of the projectile
        
        self.ivd = 1.7 # initial vertical displacement (head height of 1.7m)
        self.path = [] # a list of (x, y) co ordinates in the path of the projectile
        
        self.key = None
        
    ###############
    #function: calculate
    #description: calculates vertical displacement (s_y) at a given horizontal displacement (s_x), using 
    #               u, v and theta
    #parameters: s_x; float
    #return: vertical displacement given that the projectile is projected from head height (ivd)
    ###############
    def calculate(self, s_x):
        s_y = s_x *((self.u * self.v * math.sin(self.theta) - (4.9 * s_x)) / (self.v * self.v)) #y=x(uvsin(theta) - 4.9x)/v^2
        return s_y + self.ivd
    
    ###############
    #function: get_range
    #description: calculates the maximum horizontal displacement of the projectile using u, theta and g (9.8m/s^2)   
    #parameters: None
    #return: range (maximum horizontal displacement)
    ###############
    def get_range(self):
        self.range = (self.u*self.u*math.sin(2*self.theta))/9.8
        return self.range
    
    ###############
    #function: get_path
    #description: calls the get_range function, calculates 1000 (x,y) points on the path of the projectile
    #               using the calculate funtion. The points are stored in the path variable
    #parameters: None
    #return: path
    ###############
    def get_path(self):
        self.get_range()
        i = 0
        while i <= self.range:
            self.path.append([i, self.calculate(i)])
            i += self.range/1000
        return self.path
            
        
# Simulation Class
class Sim: 
    
    ###############
    #function: Sim constructor
    #description: initialises variables for Sim class 
    #parameters: d; float, w; float, wh; float, hh; float
    #return: None
    ###############
    def __init__(self, d, w, wh, hh, tag):
        
        self.d = d  #distance from house
        self.width = w #width of house
        self.wall_height = wh #height of walls
        self.house_height = hh #total height of house
        
        self.projectiles = {} #dictionary containing all generated projectile objects
        
        self.v_list = []
        self.theta_list = []
        
        self.clear = [] #list of projectiles that clear the house
        
        self.desc = "simulation name: {}\nvariables:\ninitial horizontal distance"\
            " of projection from house : {}m\nwidth of house: {}m\n"\
                "height of walls {}m\n height of roof peak: {}m\n"\
                    .format(tag, d, w, wh, hh)
        
        
    ###############
    #function: gen_v
    #description: generates a list of v values between 2 and 10 with an increment of 0.5
    #parameters: None
    #return: None
    ###############
    def gen_v(self):
        i = 2
        while i<=10:
            self.v_list.append(i)
            i+=0.5
    
    ###############
    #function: gen_theta
    #description: generates a list of theta values between 30 and 80 with an increment of 5
    #parameters: None
    #return: None
    ###############
    def gen_theta(self):
        for i in range(30, 81, 5):
            self.theta_list.append(i)
            
            
    ###############
    #function: gen_projectiles
    #description: iterates though the list of v and the list of theta to instantiate a Projectile. Each instantiation of 
    #               the Projectile class will have a unique combination of v and theta. The u variable is calculated using 
    #               v and theta. Each instantiation is stored in the 'projectiles' dictionary with an integer index (num)
    #parameters: None
    #return: None
    ###############
    def gen_projectiles(self):
        num = 1
        for ang in self.theta_list:
                
            for v_ in self.v_list:
                
                u_ = round(v_/math.cos(deg_to_rad(ang)), 3)
                if u_ <= 21:
                    self.projectiles[num] = Projectile(u_, v_, ang)
                    self.projectiles[num].key = num
                    num += 1
                
    ###############
    #function: gen
    #description: calls gen_v, gen_theta and gen_projectiles
    #parameters: None
    #return: None
    ###############
    def gen(self):
        self.gen_v()
        self.gen_theta()
        self.gen_projectiles()
        
    ###############
    #function: clear_proj
    #description: iterates through all projectiles and performs the calculate function at the 
    #               wall points and roof tip to check if the projectile has intercepted the house. 
    #               Checks if the range is greater than the width of the house.
    #               Any projectile that meets all conditions has cleared the house and is stored in the 'clear' list
    #parameters: None
    #return: None
    ###############
    def clear_proj(self):
        for p in self.projectiles:
            r = self.projectiles[p].get_range()
            
            y_w1 = self.projectiles[p].calculate(self.d) # y val of projectile at x val of the first wall
            y_w2 = self.projectiles[p].calculate(self.d + self.width/2) # y val of projectile at x val of the roof peak
            y_w3 = self.projectiles[p].calculate(self.d +self.width) # y val of projectile at x val of the second wall
            
            x = (2*self.d) + self.width # width of the house plus extra room on either side 
            if r >= x -1: #check that the proj clears the width of the house 
                if y_w1 > self.wall_height and y_w3 > self.wall_height: # check the proj clears the walls
                    if y_w2 > self.house_height: # check the proj clears the roof peak
                        self.clear.append(self.projectiles[p])
    
    ###############
    #function: plt_house
    #description: plots the points occupied by the border of the house   
    #parameters: None
    #return: None
    ###############
    def plt_house(self):
        y = 0
        while y < self.wall_height:
            plt.plot(self.d, y, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
            plt.plot(self.d + self.width, y, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
            y += 0.25
        
        a = 0.299776
        
        plt.plot(self.d + self.width/2, self.house_height, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        
        plt.plot(self.d + self.width/4, self.wall_height + 2.75*math.atan(a), marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        plt.plot(self.d + self.width/8, self.wall_height + 1.375*math.atan(a), marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        plt.plot(self.d + 3*self.width/8, self.wall_height + 4.125*math.atan(a), marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        
        plt.plot(self.d + 3*self.width/8 + 2*self.width/8, self.wall_height+ 4.125*math.atan(a), marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        plt.plot(self.d + 3*self.width/4, self.wall_height + 2.75*math.atan(a), marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        plt.plot(self.d +  7*self.width/8, self.wall_height + 1.375*math.atan(a), marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        
    ###############
    #function: draw_path
    #description: calls get_path on a projectile (obj) and plots the points of the projectile's path and the points
    #               of the house
    #parameters: obj; Object (Projectile)
    #return: None
    ###############
    def draw_path(self, obj, n):
        obj.get_path()
        self.plt_house()
        for point in obj.path:
            plt.plot(point[0], point[1], marker="o", markersize=5, markeredgecolor="black", markerfacecolor="black")
        plt.title("Mapped motion of projectile: {},\
                                  Image Number {}".format(obj.key, n), loc = 'left')
        plt.xlabel("Horizontal Displacement (m)")
        plt.ylabel("Vertical Displacement (m)")
        plt.show()
        
    ###############
    #function: draw_paths
    #description: calls the draw_path function for every projectile that clears the house
    #parameters: None
    #return: None
    ###############
    def draw_paths(self):
        self.set_plt()
        n = 1
        for obj in self.clear:
            self.draw_path(obj, n)
            n += 1
        
    ###############
    #function: set_plt
    #description: initialises the matplotlib canvas
    #parameters: None
    #return: None
    ###############
    def set_plt(self):
        plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True
        plt.xlim(-5, 30)
        plt.ylim(0, 25)
        plt.grid()

###############
#function: info
#description: prints information about an instantiation of the Sim class
#parameters: s; Object (Sim)
#return: None
###############
def info(s):
    
    print("\nInformation:")
    print(s.desc)
    print("number of projectiles generated: ", len(s.projectiles))
    print("via all possible permutations of the following lists:")
    print("\nv:\n", s.v_list)
    print("\ntheta:\n",s.theta_list)
    print("\nnumber of projectiles that clear the house: ", len(s.clear))
    
    print("\nInformation about cleared projectiles:")
    i = 0
    for c in s.clear:
        
        print("\nprojectile number: ", c.key)
        print("index in clear list: ", i)
        print("image number: ",  i)
        print("u: {}\nv: {}\ntheta: {}".format(c.u, c.v, rad_to_deg(c.theta)))
        print("--------------------")
        i += 1

###############
#function: main
#description: instantiates the Sim (simulation) class, generates projectiles
#               and draw the projectiles that clear the house
#parameters:
#return:
###############            
def main():
    
    # sim = Sim(distance from house, house width, wall height, total height, name)
    s = Sim(3.75, 11, 5, 6.7, "alpha")
    s.gen()
    s.clear_proj()
    s.draw_paths()
    
    info(s)
    
main()
