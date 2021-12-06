# tsp_gui

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.graphics import Ellipse
import numpy as np

point_collec = []

class DrawInput(Widget):
    def on_touch_down(self,touch):
        with self.canvas:
            # touch.ud["line"] = Line(points = (touch.x, touch.y))
            point_collec.append([touch.x, touch.y])
            # self.canvas.add(Ellipse(pos = (touch.x, touch.y), size =(20,20) ))
            touch.ud["Ellipse"] = Ellipse(pos = (touch.x, touch.y), size =(15,15) )

            
            # print(touch.ud["line"])

    # def on_touch_move(self,touch):
    #     print(touch)
    #     # touch.ud["line"].points += (touch.x, touch.y)

    # def on_touch_up(self,touch):
    #     # print("RELEASED!",touch)
    #     # print(touch.ud["line"].points)
    #     touch.ud["line"].points += (touch.x, touch.y)
        

class SimpleKivy4(App):
    def build(self):
        print("in build")
        return DrawInput()

# if __name__ == "__main__":
SimpleKivy4().run()

# print("out of the function")

# print("################################")

print(point_collec)

coord_2d = np.array(point_collec)
import os
no_cities = len(coord_2d)

file1 = open("stdin.txt", "w")
file1.write("Euclidean\n")
file1.write(f"{no_cities}\n")

# file1 = open

adj_matx = np.zeros([no_cities,no_cities])

for i in coord_2d:
    file1.write(f"{i[0]} {i[1]}\n")

for i in range(no_cities):
    for j in range(no_cities):
        if (i!=j):
            adj_matx[i,j] = np.sqrt( np.sum( ( coord_2d[i] - coord_2d[j]  )**2 ) )

for i in range(no_cities):
    for j in range(no_cities):
        file1.write(f"{adj_matx[i,j]} ")
    file1.write("\n")

file1.close()
print("Successfully created STDIN.TXT file..!")





# print(points)

