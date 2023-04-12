from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy.orm import Session

from models import Fish, FishCreate, FishUpdate
from database import get_connection, Base, engine


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get('/fish', status_code=200)
async def list_all_fishes(connection: Session = Depends(get_connection)):
    """
    Devolve uma lista com todos os peixes

    :param connection:
    """

    fishes = connection.query(Fish).all()

    connection.close()

    return fishes


@app.post('/fish', status_code=201)
async def store_fish(fish_body: FishCreate, connection: Session = Depends(get_connection)):
    """
    Valida o body da request, cria um modelo fish e o adiciona a sessão.
    Depois, aplica isso no banco e adiciona o id ao objeto fish
    Por fim, retorna fish

    Caso ocorra algum erro, reverte todas as alterações feitas no banco e devolve uma Exception

    :param fish_body:
    :param connection:
    """

    fish = Fish(specie=fish_body.specie, size=fish_body.size)

    connection.add(fish)

    try:
        connection.commit()

        connection.refresh(fish)

    except HTTPException as e:
        connection.rollback()

        raise HTTPException(status_code=500, detail=str(e))

    finally:
        connection.close()

    return {
        'fish': fish,
        'status': True
    }


@app.get('/fish/{id}', status_code=200)
async def find_fish(id: int, connection: Session = Depends(get_connection)):
    """
    Retorna um peixe específico baseado no id passado por parãmetro da roat

    :param id:
    :param connection:
    """

    fish = connection.query(Fish).filter(Fish.id == id).first()

    if not fish:
        raise HTTPException(status_code=404, detail='Nenhum peixe foi encontrado')

    connection.close()

    return fish


@app.put('/fish/{id}', status_code=200)
async def update_fish(id: int, fish_body: FishUpdate, connection: Session = Depends(get_connection)):
    """
    Atualiza as informações de um peixe

    :param id:
    :param fish_body:
    :param connection:
    """

    fish = connection.query(Fish).filter(Fish.id == id).first()

    if not fish:
        raise HTTPException(status_code=404, detail='Nenhum peixe foi encontrado')

    if fish_body.specie:
        fish.specie = fish_body.specie

    if fish_body.size:
        fish.size = fish_body.size

    try:
        connection.commit()

        connection.refresh(fish)

    except HTTPException as e:
        connection.rollback()

        raise HTTPException(status_code=500, detail=str(e))

    finally:
        connection.close()

    return {
        'fish': fish,
        'status': True,
    }


@app.delete('/fish/{id}', status_code=200)
async def destroy_fish(id: int, connection: Session = Depends(get_connection)):
    """
    Deleta um peixe do banco

    :param id:
    :param connection:
    """

    fish = connection.query(Fish).filter(Fish.id == id).first()

    if not fish:
        raise HTTPException(status_code=404, detail='Nenhum peixe foi encontrado')

    try:
        connection.delete(fish)

        connection.commit()

    except HTTPException as e:
        connection.rollback()

        raise HTTPException(status_code=500, detail=str(e))

    finally:
        connection.close()

    return {
        'message': 'Peixe deletado com sucesso!',
        'status': True
    }
