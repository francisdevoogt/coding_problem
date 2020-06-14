#!/usr/bin/env python
# coding: utf-8

# # Problem

# The problem is set up as follows:
# 
# You are given a list of airports and you have to ensure a passenger can reach each of those airports, starting at 'lga', with as many interconnecting flights as you like. All connecting one-way flights that you already have available are also given in the list called routes, none of these depart from 'lga'. It is your job to fill in the necessary flights exlusively departing from 'lga' to any other airport in order to be able to reach all airports. 
# 
# The challenge is to use the minimal amount of flights departing from 'lga'.

# First we import the only library necessary, the airports and the routes.

# In[1]:


import numpy as np

airports = ['bgi','cdg','del','doh','dsm','ewr','eyw','hnd','icn','jfk','lga','lhr','ord','san','sfo','sin','tlv','bud']

a =    ['dsm','ord']
b =    ['ord','bgi']
c =    ['bgi','lga']
d =    ['sin','cdg']
e =    ['cdg','sin']
f =    ['del','doh']
g =    ['del','cdg']
h =    ['tlv','del']
i =    ['ewr','hnd']
j =    ['hnd','icn']
k =    ['hnd','jfk']
l =    ['icn','jfk']
m =    ['jfk','lga']
n =    ['eyw','lhr']
o =    ['lhr','sfo']
p =    ['sfo','san']
q =    ['sfo','dsm']
r =    ['san','eyw']
s =    ['cdg','bud']

routes = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s]


# # Requirements

# In order to solve this problem it needs to be broken down into pieces. These pieces can follow from the requirements. 
# 
# 1)  In this case one requirement is that you need to be able to reach each of the available airports.
# 
# 2)  Another requirement is that reaching these airports must be able by departing from 'lga' and taking potential connecting flights.
# 
# Drawing out a map of the given connecting flights is likely to help you understand how to solve the problem, it does help greatly with following the logic and calculations that you perform in python. It is in my opinion essential in verification and validation. However problems like these are intended to be representative of problems that scale to immense sizes that cannot be graphically represented at full scale, the problem will thus also be treated as such in the remainder of the code.

# ## Requirement 1: reach all airports

# Lets separate the routes into arrival and departure locations with two lists, arrive and depart. This will make it more convenient to call locations related to a route. Though each route initially was given a designated letter, we continue working with the indexes that python designates to lists. The first route has index 0, the second route has index 1, ...

# In[2]:


depart =[] # create empty lists
arrive =[]
for i in range(0,np.shape(routes)[0]): # we loop from the first route to the last one, shape of routes is (number of routes,2) we only want the number of routes
    depart.append(routes[i][0]) # for each iteration of i the departure location (index 0 of a route) is appended to the existing list
    arrive.append(routes[i][1])
    
print(depart) # show the list
print(arrive)


# If we have more airports than routes available, than we know we at least need some flights from 'lga' to those destinations that are currently missing.

# In[3]:


print('all airports:',np.shape(airports)[0])
print('all routes:',np.shape(routes)[0])


# We seem to have more routes than airports... However some of the routes arrive at the same airport and we are interested in the different airports we can reach, not how many flights reach an airport. Therefor we should check the unique airports that are currently available as a arrival point.

# In[4]:


print('unique arrival airports with initial given routes:',np.shape(np.unique(arrive))[0])


# Since we have 16 available destinations with the current routes, but we need to reach 18 airports, we know we need at least two flights from 'lga' to the missing destinations. We can write a simple loop to check which arrival airports are missing and add them to a list called connection1, these are arrival airports that need to have a departure from 'lga'.

# In[5]:


# destinations missing 
connection1 =[] # create an empty list for the required connections from 'lga' to other arrival airports
for i in airports: # check all required airports to be reached, i iterates over all airport strings
    if i in np.unique(arrive): # if the airport is in the list of unique arrival airports of the given routes, it satisfies requirement 1 and nothing needs to be done
        continue
    else: # else it needs to be part of a new route as a destinations, with a departure from 'lga'
        connection1.append(i) 

print(connection1)


# Thus at this point it is clear that in order to have each airport as an arrival destination, two routes need to be added. This satisfies requirement 1.

# ## Requirement 2: 'lga' as universal starting point for any destination

# ### Part 1

# The second requirement is a bit more tricky. Since we are now going to try to map how a passenger can get from one place to another and impose restrictions on that by following one way routes while allowing to chain as many flights as you like. While it might seem difficult that infinite connections can be created, breaking down what the desired solution is will illustrate how the problem can be handled with simple bits of recurring code. For the purpose of keeping this accessible to someone with little python experience, I will reproduce the code each time that it is relevant. People with more python experience will recognize how this recurring code can easily be modified into a loop or a function, furthermore using a class for the routes could clean up the code into a few lines while keeping full functionality.
# 
# Each airport that was initially given is now also a arrival airport, now that we know we need two more routes to reach all airports. Additionally the two new routes that we just found are the only ones that depart from 'lga' so far. The two only airports that satisfy both requirement 1 and requirement two are 'ewr' and 'tlv'.
# 
# If we can reach 'ewr' and 'tlv' from 'lga', there might be more airports we can reach from 'ewr' and 'tlv'. Let's put those airports in a list called connection2, airports in this list can be reached through 'lga' and one of the airports in connection1. This gives extra information that is not required for the problem but illustrates the path that is taken. All the arrival airports combined, regardless of the amount of connecting flights, that can depart from 'lga' are stored in a list called all_airp.

# In[6]:


all_airp = np.unique(connection1+['lga']) # only airports in connection1 are known to be accessible through 'lga'

# accessible through ewr and tlv (from lga)
connection2 = []

indices = [i for i, x in enumerate(depart) if x == "ewr"] # check which flights depart from 'ewr' and save their index, this can also be done with the for loop and if statement such as before
for i in indices:
    connection2.append(arrive[int(i)]) # add the destinations of those corresponding routes to places you can reach from 'lga' 

indices = [i for i, x in enumerate(depart) if x == "tlv"]
for i in indices:
    connection2.append(arrive[int(i)])

connection2 = list(np.unique(connection2)) # it is possible that you reach the same arrival airport from different departure airports, but we only care about the unique airports we can reach

new_airp = np.setdiff1d(connection2,all_airp) # difference between known accessible airports from 'lga' and the ones now found, google 'Python find elements in one list that are not in the other'
all_airp = np.unique(list(all_airp)+list(new_airp)) # update the list of known accessible airports from 'lga'

print('arrival airports found:',connection2)
print('of which are new:      ',list(new_airp))
print('all airports satisfying req.1 and req.2:',all_airp)


# 2 more airports are found to be accessible through one connecting flight. With the same method as just before, we can check if these airports lead to any more unique destinations. Let's call the list now connection3, indicating that these destinations require 3 flights.
# 

# In[7]:


# accessible through del and hnd (from ewr and tlv)
connection3 = []
indices = np.array([i for i, x in enumerate(depart) if x == "hnd"])
for i in indices:
    connection3.append(arrive[int(i)])
indices = [i for i, x in enumerate(depart) if x == "del"]
for i in indices:
    connection3.append(arrive[int(i)])

connection3 = list(np.unique(connection3))

new_airp = np.setdiff1d(connection3,all_airp) # difference between known accessible airports from 'lga' and the ones now found
all_airp = np.unique(list(all_airp)+list(new_airp)) # update the list of known accessible airports from 'lga'

print('arrival airports found:',connection3)
print('of which are new:      ',list(new_airp))
print('all airports satisfying req.1 and req.2:',all_airp)


# 4 more airports are found to be accessible through one connecting flight. We now have a total of 8 airports identified as satifying both requirements, plus 'lga' itself. With the same method as before, we can check if these new airports lead to any more unique destinations. Let's call the list now connection4, indicating that these destinations require 4 flights.
# 

# In[8]:


connection4 = []
indices = [i for i, x in enumerate(depart) if x == "cdg"]
for i in indices:
    connection4.append(arrive[int(i)])
indices = [i for i, x in enumerate(depart) if x == "doh"]
for i in indices:
    connection4.append(arrive[int(i)])
indices = [i for i, x in enumerate(depart) if x == "icn"]
for i in indices:
    connection4.append(arrive[int(i)])
indices = [i for i, x in enumerate(depart) if x == "jfk"]
for i in indices:
    connection4.append(arrive[int(i)])
    
connection4 = list(np.unique(connection4))

new_airp = np.setdiff1d(connection4,all_airp) # difference between known accessible airports from 'lga' and the ones now found
all_airp = np.unique(list(all_airp)+list(new_airp)) # update the list of known accessible airports from 'lga'

print('arrival airports found:',connection4)
print('of which are new:      ',list(new_airp))
print('all airports satisfying req.1 and req.2:',all_airp)


# Now it can be seen that two of the arrival destinations from connection4 are recurring, namely 'jfk' which also can be reached by a flight from connection3 and 'lga'. Let's see where the 2 new airports lead to.

# In[9]:


connection5 = []
indices = [i for i, x in enumerate(depart) if x == "bud"]
for i in indices:
    connection5.append(arrive[int(i)])
indices = [i for i, x in enumerate(depart) if x == "sin"]
for i in indices:
    connection5.append(arrive[int(i)])
    
connection5 = list(np.unique(connection5))

new_airp = np.setdiff1d(connection5,all_airp) # difference between known accessible airports from 'lga' and the ones now found
all_airp = np.unique(list(all_airp)+list(new_airp)) # update the list of known accessible airports from 'lga'

print('arrival airports found:',connection5)
print('of which are new:      ',list(new_airp))
print('all airports satisfying req.1 and req.2:',all_airp)


# The list of new airports comes up emty! We have reached the end of the line after 4 flights, starting at 'lga'. Clearly we have not yet reached every airport starting from 'lga', which means that at least one or more flights starting at 'lga' will be required.

# ### Part 2

# When starting on Part 1 to start solving the second requirement it might have not been clear why there was a part 1 without a title. In the breakdown of a problem it is impossible to identify all the smallest problems you will encounter from the start. So far the problem solving structure has been following the principle of using the minimal amount of flights starting at 'lga' and encountered an end to the top level approach two times. The first time when the two flights in connection1 were found to be necessary to have each airport as an arrival point, and the second time when all the connecting flights of connection2 do not lead to full cover of all airports. In both cases we have focused on adding the minimal routes and checking on how far it gets us in terms of the requirements.
# 
# In order to provide full coverage of all airports it makes sense to check which airports we can't reach from 'lga' yet.

# In[10]:


missing = np.setdiff1d(airports,all_airp)


# In[11]:


print('missing airports from the required destinations:',missing)


# Now again there are multiple approaches to solving this problem. Keep in mind we want the minimal amount of flights departing from 'lga'. As such we can fall back on the approach from Part 1, where we checked which airports we can reach if the departure airport is known. We know that the remaining route(s) have to start at 'lga' and go to one of the missing airports. As such we can check the missing airports and where they lead to. Let's call the list with the airports we can reach by adding another route starting at 'lga' connections_possible this time. 
# 
# As the approach we take has been explained in detail before, the coding can be cleaned up a bit. Although the code below can be automated further, it now allows you to adjust the 'guessed' route that you want to investigate from the missing airports list. The code spits out all the airports you can reach when making this 1 extra route available starting at 'lga'. 

# In[12]:


# for new_route_departure in missing:

new_route_departure = 'dsm' # try replacing "dsm" with any of the other missing airports and see which final airports you can reach

connections_possible = [new_route_departure]

indexes = [i for i, x in enumerate(depart) if x == new_route_departure] # which of the flights departs from your chosen airport?
for i in indexes:
    connections_possible.append(arrive[int(i)]) # where does your chosen airport lead to?

while True:    # let's now loop for eternity to find where all the connecting flights lead to
    indexes1 = [i for i, x in enumerate(depart) if x in connections_possible] # set up second index list to evaluate if new airports are being found
    if indexes1 == indexes: # if the old list of indexes is equal to the new one, no new departure airports are being found
        connections_possible = list(np.unique(connections_possible)) 
        break # if we don't find anything new, we should quit looping
    else:
        for i in indexes1: # if we find new departure airports
            connections_possible.append(arrive[int(i)]) # they will lead to new airports
        indexes = indexes1 # update the old index list to the new index list values
        connections_possible = list(np.unique(connections_possible))   

all_airp_potentially = np.unique(list(all_airp)+list(connections_possible)) # the list of accessible airports from 'lga'
still_missing = np.setdiff1d(airports,all_airp_potentially)
print('airports that can be reached with new route:',connections_possible)      
print('all airports satisfying req.1 and req.2:',all_airp_potentially)
print('missing airports from the required destinations:',still_missing)


# If you try some of the airports that were initially missing as new options for an added route starting at 'lga' you will find that some will not lead to you serving all airports. However multiple options will also lead to you serving all airports. 

# Now that it is found that adding one more route is enough, the problem is solved. However it might have been possible that one extra route is not enough. In that case a new iteration can be set up that checks the airports that can be reached with two additional routes. This principle can scale up to any number of required extra routes till all airports satisfy both requirement 1 and 2. This new iteration can be constructed similar as before, the only change required is checking if the accessible airports of two new routes together make up the missing airports.
