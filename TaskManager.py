# -- Autor : Oscar-Amacende Task Manager
import json
import os
#Import fecha y API
#pip install "fastapi[standard]"
#pip imstall sqlalchemy
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#Titulo

app = FastAPI(title="Oscar-Amacende Task Manager API")


# Funciones 
def limpiar_pantalla():
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')

def guardar_tareas(tareas):
    try:
        with open('tareas.json', 'w', encoding='utf-8') as archivo:
            json.dump(tareas, archivo, indent=4, ensure_ascii=False)
            print("Guardado en un archivo Json")
    except Exception as e:
        print(f'Error al guardar Json: {e}')


def iniciar(tareas):
    #Guarda arreglo de valores indivudual
    tarea={}

    tarea["Titulo"] = input("Titulo: ")
    tarea["Descripcion"] = input("Descripcion: ")
    tarea["Prioridad"] = input("Prioridad: ")
    tarea["Vencimiento"] = input("Fecha limite (DD/MM/AAAA): ")
    tarea["Completado"] = False 

    #print(tarea)

    #Guardando en el arreglo global
    tareas.append(tarea)
    print(tarea)

def listar_tareas(tareas):
    print("---   TAREAS:   ---")
    for tarea in tareas:
        print(tarea)
    
def completar_tareas(tareas):
    print("---   Tarea que desea completar    ---")
    for numero, tarea in enumerate(tareas, start=1):
        print(numero, tarea)

    print("Longitud de tareas: ",len(tareas))
    comp=int(input("Tarea que ha completado : "))
    if comp > len(tareas):
        print("Por favor elige una tarea de las que esten listadas")
    else :
        #print(comp)
        nvoi=comp-1
        #print(tareas[nvoi])
        #Llamamos el indice y el campo a actualizar
        tareas[nvoi]["Completado"] = True
        print("Actualizado : ",tareas[nvoi])

def eliminar_tareas(tareas):
    print("---   ELIMINAR TAREAS:   ---")
    for numero, tarea in enumerate(tareas, start=1):
        print(numero, tarea)
    
    print("Longitud de tareas: ",len(tareas))
    comp=int(input("Tarea que desea eliminar : "))
    if comp > len(tareas):
        print("Por favor elige una tarea de las que esten listadas")
    else :
        nvoi=comp-1
        tarea_eliminada = tareas.pop(nvoi)
        print(f"Eliminado : {tarea_eliminada['Titulo']}")

#Main
def main():
    #Guarda todas las tareas
    tareas=[]

    while True:
        print("===   TASK MANAGER   ===")
        print("1-. Agregar tarea")
        print("2-. Listar Tareas")
        print("3-. Completar tarea")
        print("4-. Eliminar tarea")
        print("5-. Salir")

        opcion = input("Elige una opcion:").strip()

        if opcion =="1":
            limpiar_pantalla()
            iniciar(tareas)
            guardar_tareas(tareas)
        elif opcion =="2":
            limpiar_pantalla()
            listar_tareas(tareas)
            guardar_tareas(tareas)
        elif opcion =="3":
            limpiar_pantalla()
            completar_tareas(tareas)
            guardar_tareas(tareas)
        elif opcion =="4":
            limpiar_pantalla()
            eliminar_tareas(tareas)
            guardar_tareas(tareas)
        elif opcion =="5":
            break


if __name__ == '__main__':
  main()