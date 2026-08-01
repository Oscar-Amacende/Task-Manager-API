import json
import os
from typing import List
from fastapi import FastAPI,Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

#Import fecha y API
#pip install "fastapi[standard]"
#pip install sqlalchemy
#python3-64.exe .\Taskito.py 
#http://127.0.0.1:8000/docs Para probar las funciones de nuestra API
app = FastAPI(title="Oscar-Amacende Task Manager API")

# Archivo donde se guardarán los datos
ARCHIVO_JSON = "tareas.json"

# ==========================================
# CONFIGURACIÓN DE LA BASE DE DATOS (SQLITE)
# ==========================================
# Creamos el archivo de la base de datos local
DATABASE_URL = "sqlite:///./tareas.db"

# El argumento 'check_same_thread' es necesario únicamente para SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ==========================================
# MODELO DE LA BASE DE DATOS (SQLAlchemy)
# ==========================================
# Esto define cómo se creará la tabla físicamente en SQLite
class TareaDB(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True) # ID único autoincremental
    titulo = Column(String, index=True)
    descripcion = Column(String)
    prioridad = Column(String)
    completado = Column(Boolean, default=False)

# Crea la tabla en la base de datos si aún no existe
Base.metadata.create_all(bind=engine)




# ==========================================
# MODELOS DE VALIDACIÓN DE DATOS (Pydantic)
# ==========================================
# 1. Definimos la estructura de una Tarea usando Pydantic
class TareaBase(BaseModel):
  Titulo: str
  Descripcion: str
  Prioridad: str
  Completado: bool = False

# Estructura que la API devuelve (incluye el ID que genera la base de datos)
class TareaResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    prioridad: str
    completado: bool

    class Config:
        from_attributes = True # Permite a Pydantic leer los modelos de SQLAlchemy


# ==========================================
# CONFIGURACIÓN DE FASTAPI Y DEPENDENCIAS
# ==========================================
app = FastAPI(title="Oscar-Amacende Task Manager con SQLite")

# Función crucial para abrir y cerrar la conexión a la DB de forma segura en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ==========================================
# RUTAS DE LA API (ENDPOINTS)
# ==========================================

#RUTA 1: Obtener todas las tareas (GET)
@app.get("/tareas", response_model=List[TareaResponse])
def listar_tareas(db: Session = Depends(get_db)):
    return db.query(TareaDB).all()

#RUTA 2: Crear una nueva tarea (POST)
@app.post("/tareas", response_model=TareaResponse, status_code=201)
def crear_tarea(tarea: TareaBase, db: Session = Depends(get_db)):
    nueva_tarea = TareaDB(
        titulo=tarea.Titulo,
        descripcion=tarea.Descripcion,
        prioridad=tarea.Prioridad,
        completado=tarea.Completado
    )
    db.add(nueva_tarea)     # Prepara la inserción
    db.commit()             # Guarda físicamente en la DB
    db.refresh(nueva_tarea) # Trae el ID recién generado
    return nueva_tarea

#RUTA 3: Completar una tarea por su índice (PUT)
@app.put("/tareas/{tarea_id}/completar", response_model=TareaResponse)
def completar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(TareaDB).filter(TareaDB.id == tarea_id).first()
    
    if not tarea:
        raise HTTPException(status_code=404, detail="La tarea con ese ID no existe.")
    
    tarea.completado = True
    db.commit()
    db.refresh(tarea)
    return tarea

#RUTA 4: Eliminar una tarea por su índice (DELETE)
@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(TareaDB).filter(TareaDB.id == tarea_id).first()
    
    if not tarea:
        raise HTTPException(status_code=404, detail="La tarea con ese ID no existe.")
    
    db.delete(tarea) # Borra el registro
    db.commit()
    return {"mensaje": f"Tarea '{tarea.titulo}' eliminada con éxito de la base de datos"}


#Arranca el servidor local si ejecutas el archivo directamente
if __name__ == "__main__":
  import uvicorn

  uvicorn.run("Taskito:app", host="127.0.0.1", port=8000, reload=True)