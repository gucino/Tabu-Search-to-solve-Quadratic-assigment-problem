# -*- coding: utf-8 -*-
"""
Created on Sun May 17 15:31:59 2020

@author: Tisana
"""

import numpy as np
from matplotlib import pyplot as plt

#quadratic assignment problem
distance_matrix=np.array([[0,1,2,3,1,2,3,4],[1,0,1,2,2,1,2,3],[2,1,0,1,3,2,1,2],
                      [3,2,1,0,4,3,2,1],[1,2,3,4,0,1,2,3],[2,1,2,3,1,0,1,2],
                      [3,2,1,2,2,1,0,1],[4,3,2,1,3,2,1,0]])
flow_matrix=np.array([[0,5,2,4,1,0,0,6],[5,0,3,0,2,2,2,0],[2,3,0,0,0,0,0,5],
                      [4,0,0,0,5,2,2,10],[1,2,0,5,0,10,0,0],[0,2,0,2,10,0,5,1],
                      [0,2,0,2,0,5,0,10],[6,0,5,10,0,1,10,0]])

#cost function
def cost_function(distance,flow_matrix):
    cost=(distance*flow_matrix).sum()
    return cost


#dict btw  index and department name
convert={"A":0,
         "B":1,
         "C":2,
         "D":3,
         "E":4,
         "F":5,
         "G":6,
         "H":7}
#transform list of depeartment into distance matrix
def solution_function(solution):
    index_list=[]
    for each_letter in solution:
        index_list.append(convert[each_letter])
    new_solution= np.copy(distance_matrix)
    new_solution=new_solution[index_list,:]
    new_solution=new_solution[:,index_list]
    return new_solution


#move operator : generate new solution
def move(letter1,letter2,current_solution):
    index_one=current_solution.index(letter1)
    index_two=current_solution.index(letter2)
    
    new_solution=np.copy(current_solution)
    new_solution[index_one]=current_solution[index_two]
    new_solution[index_two]=current_solution[index_one]
    return new_solution

#all posible move
all_letter=[]
for i in convert:
    all_letter.append(i) 
all_possible_move_list=[]
while True:
    letter_1=np.random.choice(all_letter)
    letter_2=np.random.choice(all_letter)
    while letter_1==letter_2:
        letter_2=np.random.choice(all_letter)
    if [letter_1,letter_2] not in all_possible_move_list and [letter_2,letter_1] not in all_possible_move_list:
        all_possible_move_list.append([letter_1,letter_2])
    
    #print(len(all_possible_move_list))
    if len(all_possible_move_list)==28:
        break
  
#parameter
M=100
L=10

    
############################start###########################################    
current_solution=np.array(["A","B","C","D","E","F","G","H"]).tolist()
current_distance=solution_function(current_solution)
current_cost=cost_function(current_distance,flow_matrix)
tabu_list=[]
loss_list=[]
for m in range(0,M):
    loss_list.append(current_cost)   
    print(current_cost)
    solution_list=[]
    obj_value_list=[]
    #get all obj value
    for n in range(0,len(all_possible_move_list)):
        
        new_solution=move(all_possible_move_list[n][0],all_possible_move_list[n][1],current_solution)
        new_distance=solution_function(new_solution)
        cost=cost_function(new_distance,flow_matrix)
        
        obj_value_list.append(cost)
        solution_list.append(new_solution)
        
    #sort ascending
    index_list=np.argsort(obj_value_list)
    solution_list=np.array(solution_list)[index_list].tolist()
    obj_value_list=np.array(obj_value_list)[index_list].tolist()
    
    #check in tabu
    for best_solution in solution_list:
        if best_solution not in tabu_list:
            #take this move
            current_solution=best_solution
            current_distance=solution_function(current_solution)
            current_cost=cost_function(current_distance,flow_matrix)
            
            #append to tabu
            tabu_list.append(current_solution)
            if len(tabu_list)>L:
                #remove oldest item
                tabu_list.pop(0)
            break

best_index=np.argmin(loss_list)
optimal_solution=solution_list[best_index]
optimal_lost=loss_list[best_index]
print("best solution : ",optimal_solution)
print("best loss : ",optimal_lost)       

#see result
plt.xlabel("m iteration")
plt.ylabel("loss")
plt.plot(np.arange(0,len(loss_list)),loss_list)
   
    
    