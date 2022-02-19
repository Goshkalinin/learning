from math import pi, sqrt
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

start_time = datetime.now()

input_parameters = pd.read_csv('Input Parameters.csv', encoding='ISO-8859-1')  # импортируем в скрипт одс-ку
holes_list = input_parameters['Радиус отверстия'].values  # пилим список значений из колонки "Радиус отверстия"


hole_counter = 0  # счётчик для диаметров отверстий
counter = 0  # счётчик итераций, он же считает время

"""стартовые параметры"""
model_volume = 0.001  # объём модели в кубометрах
h = 0.1  # высота бункера в метрах
r = 0.05  # радиус бункера в метрах
r_hole = holes_list[hole_counter]  # радиус отверстия в метрах, берётся из таблички
vol = pi*h*r**2  # объём в кубометрах
remaining_volume = model_volume  # оставшийся объём до истечения объёма модели
cv = 0.5  # Coefficient of Velocity
g = 9.81  # ускорение свободного падения, м/с
t = 1  # дискретизация по времени, секунды
potlife = 120  # время жизни пластика в секундах


estimated_cast_time = []
OutputData = {'Радиус отверстия':[holes_list],'Время залива': [estimated_cast_time]}



def base_height():  # пока объём истечения превышает объём бункера
    global h
    global remaining_volume
    torricelli = sqrt(g*h*2)*cv
    outlet_volume = pi*torricelli*t*r_hole**2
    remaining_volume = remaining_volume - outlet_volume
    h = vol/(pi*r**2)


def new_height():  # когда объём истечения меньше объёма бункера
    global h
    global remaining_volume
    global vol
    torricelli = sqrt(g*h*2)*cv
    outlet_volume = pi*torricelli*t*r_hole**2
    vol = vol - outlet_volume
    remaining_volume = remaining_volume - outlet_volume
    h = vol/(pi*r**2)


print('parameters: ')

print('Model Volume: '+"{:.3f}".format(model_volume*1000000)+' cm cube')
print('Bunker Volume: '+"{:.3f}".format(vol*1000000)+' cm cube')

print('Bunker Height: '+"{:.3f}".format(h*1000)+' mm')
print('Bunker Radius: '+"{:.3f}".format(r*1000)+' mm')
print('Hole Radiuses: ' + str(holes_list[0]) +' - '+ str(holes_list[-1]) + ' m')

print('Gravitational Acceleration: '+"{:.3f}".format(g))
print('Time Discrimination: '+"{:.3f}".format(t)+' s')
print('Coefficient of Velocity: '+"{:.3f}".format(cv))
print('____________________________________________________')

while hole_counter != len(holes_list):
    while h > 0:

        if remaining_volume > vol:
            base_height()
            counter += 1
        else:
            new_height()
            counter += 1

    if potlife > counter * t:  # если время жизни пластика больше времени истечения
        print('Time Left: ' + str("{:.2f}".format(counter * t)) + ' s' + ' with ' + 'hole radius: ' + "{:.2f}".format(r_hole * 1000) + ' mm')
        estimated_cast_time.append(str("{:.2f}".format(counter * t)))
    else:
        print('Hole radius: ' + "{:.2f}".format(r_hole * 1000) + ' mm' + ' is not enough!')
        estimated_cast_time.append(str("{:.2f}".format(counter * t)))

    hole_counter += 1  # прыгаем на следующий диаметр
    if hole_counter == len(holes_list):  # ?!!! без этой строчки выдаёт ошипку!
        break
    r_hole = holes_list[hole_counter]  # обновляем диаметр отверстия
    counter = 0  # обнуляем счётчик итераций
    h = 0.1  # обнуляем высоту
    vol = pi * h * r ** 2  # обнуляем объём бункера
    remaining_volume = model_volume  # обнуляем объём истечения

for col in OutputData.keys():
  OutputData[col] = OutputData[col][0]


df = pd.DataFrame(OutputData)

print(df.dtypes)

# df['Время залива'].plot()
# plt.show()

df.head()
print("Lead Time: " + str(datetime.now() - start_time))
print(OutputData)
print(df)

df.to_csv('out.csv')