#Práctica 2: Métodos GET, PUT, POST, DELETE Y PATCH
#Equipo:
#Beltrán Saucedo Axel Alejandro
#Cerón Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham
#Lorenzo Silva Abad Rey

#Recuerden descargar al fastapi
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(
    title= "Gestion de paquetes",
    description= "API para almacenar, editar, actualizar y borrar la información de los paquetes (items) a ser enviados"
)


class ItemBase(BaseModel):
    ganancia: float
    peso: float

class Item(ItemBase):
    id: int

class ItemUpdate(BaseModel):
    peso: Optional[float] = None
    ganancia: Optional[float] = None

envio: List[Item] = []
current_id = 0


@app.get("/items/", response_model=list[Item], tags=["Items"])
def get_all_items():
    return envio

@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
def get_item_by_id(item_id: int):
    """Obtiene un item por su ID"""
    item = next((item for item in envio if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    return item

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"])
def create_item(item_data: ItemBase):
    """Crea un item nuevo"""
    global current_id
    current_id += 1

    new_item = Item(id=current_id, **item_data.model_dump())

    envio.append(new_item)
    return new_item

@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
def replace_item(item_id: int, item_data: ItemBase):
    """Actualiza un item por su id"""
    for i, item in enumerate(envio):
        if item.id == item_id:
            updated_item = Item(id=item_id, **item_data.model_dump())
            envio[i] = updated_item
            return updated_item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

@app.patch("/items/{item_id}", response_model=Item, tags=["Items"])
def update_item_partially(item_id: int, item_update: ItemUpdate):
    """Actualiza parcialmente un item por su id"""
    stored_item = next((item for item in envio if item.id == item_id), None)
    if not stored_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encntrado")

    update_data = item_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(stored_item, key, value)
    return stored_item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
def delete_item(item_id: int):
    """Borra un item por su id"""
    item_to_delete = next((item for item in envio if item.id == item_id), None)
    if not item_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    envio.remove(item_to_delete)
    return
