from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import services
from schemas import services_create, services_response

# Crear la tabla en Neon si todavía no existe
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicios")


# ====================================
# GET: Consultar todas los servicios
# ====================================
@app.get("/Servicios", response_model=list[services_response])
def get_Servicios(db: Session = Depends(get_db)):
    Servicios = db.query(services).all()
    return Servicios


# ====================================
# GET: Consultar un servicio
# ====================================
@app.get("/Servicios/{services_id}", response_model=services_response)
def get_services(
    services_id: int,
    db: Session = Depends(get_db)
):
    service = db.query(services).filter(
        services.id == services_id
    ).first()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    return service


# ====================================
# POST: Registrar un servicio
# ====================================
@app.post("/Servicios", response_model=services_response, status_code=201)
def create_services(
    data: services_create,
    db: Session = Depends(get_db)
):
    service = services(
        name=data.name,
        price=data.price,
        description=data.description
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    return service


# ====================================
# PUT: Actualizar un servicio
# ====================================
@app.put("/Servicios/{services_id}", response_model=services_response)
def update_services(
    services_id: int,
    data: services_create,
    db: Session = Depends(get_db)
):
    service = db.query(services).filter(
        services.id == services_id
    ).first()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    service.name = data.name
    service.price = data.price
    service.description = data.description

    db.commit()
    db.refresh(service)

    return service


# ====================================
# DELETE: Eliminar un servicio
# ====================================
@app.delete("/Servicios/{services_id}")
def delete_services(
    services_id: int,
    db: Session = Depends(get_db)
):
    service = db.query(services).filter(
        services.id == services_id
    ).first()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    db.delete(service)
    db.commit()

    return {
        "message": "Service deleted successfully"
    }