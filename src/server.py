from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.schemas.schemas import Serie
from src.schemas import schemas
from src.infra.sqlalchemy.config.database import get_db, criar_bd
from src.infra.sqlalchemy.repositorios.series import RepositorioSerie

criar_bd()
app = FastAPI()

@app.post('/series')
def criar_serie(serie: schemas.Serie, db: Session = Depends (get_db)):
    serie_criada = RepositorioSerie(db).criar(serie)
    return serie_criada

@app.get('/series')
def listar_serie( db: Session = Depends(get_db)):
    lista_serie = RepositorioSerie(db).listar()
    return lista_serie

