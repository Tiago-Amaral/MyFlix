# Projeto MyFlix - API para Gerenciamento de Séries
### (Ainda em construção)

## Descrição
Este projeto tem como objetivo criar uma API para gerenciamento de séries utilizando o framework **FastAPI** e o **SQLAlchemy** para interação com o banco de dados SQLite. A API permite cadastrar, listar e, futuramente, obter e remover séries.

## Tecnologias Utilizadas
- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**

## Estrutura do Projeto

### Configuração do Banco de Dados
A conexão com o banco de dados é configurada utilizando o SQLAlchemy:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./myflix.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def criar_bd():
    Base.metadata.create_all(bind=engine)

def get_db():
    bd = SessionLocal()
    try:
        yield bd
    finally:
        bd.close()
```

### Modelo de Dados
A classe `Serie` representa o modelo de dados no banco:
```python
from sqlalchemy import Column, Integer, String
from src.infra.sqlalchemy.config.database import Base

class Serie(Base):
    __tablename__ = 'serie'
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    ano = Column(Integer)
    genero = Column(String)
    qtd_temporadas = Column(Integer)
```

### Esquema com Pydantic
O esquema utilizado para validação de dados:
```python
from pydantic import BaseModel
from typing import Optional

class Serie(BaseModel):
    id: Optional[int] = None
    titulo: str
    ano: int
    genero: str
    qtd_temporadas: int

    class Config:
        orm_mode = True
```

### Repositório
O repositório é responsável pela lógica de persistência e consulta:
```python
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.models import models

class RepositorioSerie():
    def __init__(self, db: Session):
        self.db = db

    def criar(self, serie: schemas.Serie):
        db_serie = models.Serie(
            titulo=serie.titulo,
            ano=serie.ano,
            genero=serie.genero,
            qtd_temporadas=serie.qtd_temporadas
        )
        self.db.add(db_serie)
        self.db.commit()
        self.db.refresh(db_serie)
        return db_serie

    def listar(self):
        series = self.db.query(models.Serie).all()
        return series
```

### Rotas da API
As rotas foram definidas utilizando FastAPI:
```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.schemas.schemas import Serie
from src.infra.sqlalchemy.config.database import get_db, criar_bd
from src.infra.sqlalchemy.repositorios.series import RepositorioSerie

criar_bd()
app = FastAPI()

@app.post('/series')
def criar_serie(serie: Serie, db: Session = Depends(get_db)):
    serie_criada = RepositorioSerie(db).criar(serie)
    return serie_criada

@app.get('/series')
def listar_series(db: Session = Depends(get_db)):
    lista_series = RepositorioSerie(db).listar()
    return lista_series
```

## Funcionalidades Implementadas
1. **Cadastrar série:** Endpoint POST `/series` para criar uma nova série no banco de dados.
2. **Listar séries:** Endpoint GET `/series` para listar todas as séries cadastradas.

## Funcionalidades Futuras
- Obter detalhes de uma série por ID.
- Remover uma série do banco de dados.
- Atualizar informações de uma série existente.

## Como Executar o Projeto
1. Clone este repositório.
2. Certifique-se de ter o Python instalado.
3. Instale as dependências:
   ```bash
   pip install fastapi sqlalchemy pydantic uvicorn
   ```
4. Execute o servidor:
   ```bash
   uvicorn main:app --reload
   ```
5. Acesse a documentação interativa da API em:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Conclusão
Este projeto demonstra o uso do FastAPI para criar uma API funcional e escalável, abordando aspectos como modelagem de dados, integração com banco de dados e definição de rotas. Mais funcionalidades serão adicionadas no futuro para aprimorar o sistema.

