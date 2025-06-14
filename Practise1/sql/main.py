from fastapi import FastAPI, Depends,status, Response,HTTPException
from .import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app = FastAPI()

models.Base.metadata.create_all(engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/', status_code= 201, tags=['Users'])

def create(request:schemas.User, db: Session = Depends(get_db)):

    new_user = models.User(id=request.id, name=request.name, age=request.age, country=request.country)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/',status_code=status.HTTP_200_OK, tags=['Users'])

def get_all(db: Session = Depends(get_db)):
    get_info = db.query(models.User).all()
    return get_info

@app.get('/{id}', status_code = status.HTTP_202_ACCEPTED, tags=['Users'])

def uni_info (id, response: Response, db: Session = Depends(get_db)):
    uni_data = db.query(models.User).filter(models.User.id == id).first()
    # uni_data = db.query(models.User).filter(models.User.age == age).first()
    if not uni_data:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'User with id {id} not found'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return uni_data

@app.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT, tags=['Users'])

def delete_info(id,db: Session = Depends(get_db)):
    delete_data = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    if not delete_data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id {id} not found')
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto'   )

@app.post('/login', status_code= status.HTTP_201_CREATED, tags=['Login'])

def create_login( request: schemas.Login, db: Session = Depends(get_db)):
    hashed_password = pwd_cxt.hash(request.password)
    new_login = models.Loginfo(username = request.username, password = hashed_password, email = request.email)
    if not request.username or not request.password or not request.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username, password, and email are required")
    db.add(new_login)
    db.commit()
    db.refresh(new_login)
    return new_login



@app.delete('/login/{id}', status_code= status.HTTP_204_NO_CONTENT, tags=['Login'])
def delete_login(id,db: Session = Depends(get_db)):
    delete_login = db.query(models.Loginfo).filter(models.Loginfo.id == id).delete(synchronize_session=False)
    if not delete_login:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id {id} not found')
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.put('/{id}', status_code=status.HTTP_202_ACCEPTED , tags=['Users'])

def update_info(id:int, request: schemas.User, db: Session = Depends(get_db)):

    update_data = db.query(models.User).filter(models.User.id == id)
    if not update_data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    
    update_data.update(request.dict())
    db.commit()
    return update_data.first()

# @app.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update_info(id: int, request: schemas.User, db: Session = Depends(get_db)):
#     update_data = db.query(models.User).filter(models.User.id == id)
#     if not update_data.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    
#     update_data.update(request.dict())
#     db.commit()
#     return update_data.first()