# tsp


import time
import random
import numpy as np
import sys
import warnings


# # STDIN

euclidean = input().lower() == "euclidean"
num_cities = int(input())

coord_2d_org = np.zeros([num_cities,2])
adj_matx = np.zeros([num_cities,num_cities])

for i in range(num_cities):
    coord_2d_org[i] = np.fromstring(input().rstrip() , dtype=float, sep=' ')
num_cities
for i in range(num_cities):
    adj_matx[i] = np.fromstring(input().rstrip() , dtype=float, sep=' ')

# lsst = []
# for i in coord_2d_org:
#     lsst.append(list(i))
# print(lsst)
########################################################################

coord_2d = coord_2d_org.copy()
# coord_2d[:,0] = coord_2d[:,0] - np.min(coord_2d[:,0])
# coord_2d[:,1] = coord_2d[:,1] - np.min(coord_2d[:,1])
# coord_2d = 100* coord_2d/np.max(coord_2d)

if euclidean:
    for i in range(num_cities):
        for j in range(num_cities):
            if (i!=j):
                adj_matx[i,j] = np.sqrt( np.sum( ( coord_2d[i] - coord_2d[j]  )**2 ) )


########################################################################


def sigmoid(x):
    out = (-1)*x
    return  (1/(1+np.exp(out)))

def path_cost_adj(path):
    cost = 0
    for i in range(len(path)-1):
        cost +=  adj_matx[path[i], path[i+1]]
    cost+= adj_matx[path[0], path[-1]]
    return cost

def inverse(path, i, j):            # 2-edges are changed
    temp = path.copy()
    temp[i:j+1] = path[i:j+1][::-1]
    return temp     

def insert(path, i, j):             # 3-edges are changed
    temp = path.copy()
    tpr = path[j]
    if (i<j):
        temp[i+1:j+1] = path[i:j]
        temp[i] = tpr
    if (i>j):
        temp[j:i] = path[j+1:i+1]
        temp[i] = tpr
    return temp

def swap(path, i, j):               # 4-edges are changed
    temp = path.copy()
    temp[i] , temp[j] = path[j] , path[i]
    return temp



def list_bsd_sa(cities_indx, adj_matx):
    start_time = time.time()
    best_path = np.random.permutation(cities_indx)
    glob_best_path = best_path.copy()
    no_cities = len(cities_indx)
    E_best = path_cost_adj(best_path)
    E_glob_best = E_best
    L_max = 1000 #120 
    M = 3*no_cities
    p_o =  1e-10 #1e-15 # 1e-12 
    M = int(M)
    T_list = np.zeros(L_max)

    for i in range(L_max):       ##### CHECKED 
        # Random neighbour gen
        m_1 = random.randint(0,no_cities-1)
        m_2 = random.randint(0,no_cities-1)
        while(m_2 == m_1):
            m_2 = random.randint(0,no_cities-1)
        neighbour_lst = [ inverse(best_path, m_1, m_2), insert(best_path, m_1, m_2),  swap(best_path, m_1, m_2) ] 
        cost_arr = np.array([ path_cost_adj(neighbour_lst[0]),path_cost_adj(neighbour_lst[1]) , path_cost_adj(neighbour_lst[2]) ])
        idx = np.where(cost_arr == cost_arr.min() )[0][0]
        neighbour = neighbour_lst[idx]

        if (cost_arr[idx] < E_best):
            best_path = neighbour.copy() 
            E_best = path_cost_adj(best_path)
        
        T_list[i] = (-1)* abs( cost_arr[idx] - E_best)/np.log(p_o)

    # K = ?????
    # M = ?????
    # p_o = ????? 3 hyperparams to be tuned
    K = 100000
    # M = 2000 

    
    # while( time.time() - start_time <=290.0 ):
    while(1):
        t = 0
        c = 0
        T_list.sort()
        T_max = T_list[-1]  ### Checked
        for m in range(M):
            m_1 = random.randint(0,no_cities-1)
            m_2 = random.randint(0,no_cities-1)
            while(m_2 == m_1):
                m_2 = random.randint(0,no_cities-1)
            neighbour_lst = [ inverse(best_path, m_1, m_2), insert(best_path, m_1, m_2),  swap(best_path, m_1, m_2) ]
            cost_arr = np.array([ path_cost_adj(neighbour_lst[0]),path_cost_adj(neighbour_lst[1]) , path_cost_adj(neighbour_lst[2]) ])
            idx = np.where(cost_arr == cost_arr.min() )[0][0]
            neighbour = neighbour_lst[idx]

            if (cost_arr[idx] < E_best):
                best_path = neighbour.copy()
                E_best = path_cost_adj(best_path)
                if (E_glob_best > E_best):
                    glob_best_path = best_path.copy()
                    print(' '.join(map(str, glob_best_path)))
                    E_glob_best = path_cost_adj(glob_best_path)
                    # print(E_glob_best)
                # print(E_best) 
            elif(cost_arr[idx] > E_best): 
                uni_rand = 1
                while(uni_rand ==0 or uni_rand ==1):
                    uni_rand = random.uniform(0, 1)
                dff = E_best - cost_arr[idx]
                if ( uni_rand < np.exp(dff/T_max) ):
                    t = (t + dff)/np.log(uni_rand)
                    c = c+1
                    best_path = neighbour.copy()
                    E_best = path_cost_adj(best_path)
                    if (E_glob_best > E_best):
                        glob_best_path = best_path.copy()
                        print(' '.join(map(str, glob_best_path)))
                        E_glob_best = path_cost_adj(glob_best_path)
                        # print(E_glob_best)

                    # print(E_best)
        # print(f"Epochs: {k}  || T MAX : {T_max} || BEST SCORE: {E_glob_best} ")
        # if (k%120 == 0): 
        #     best_path = glob_best_path.copy()

        if c!=0:
            T_list[-1] = t/c
        # print(f"Epochs: {k}  || T MAX : {T_max} || BEST SCORE: {E_best} ")

    return glob_best_path

    



# start_time = time.time()
# cities_indx = np.arange(no_cities)

# sim_anneal_res = sim_anneal(cities_indx, adj_matx)
# best_path = sim_anneal_res[1]
cities_indx = np.arange(num_cities)
no_cities = num_cities
best_path = list_bsd_sa(cities_indx, adj_matx)
# best_path = Genetic(cities_indx) 

