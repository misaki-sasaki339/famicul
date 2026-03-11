from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import hospital as hospital_model
from app.models import user as user_model
from app.schemas import user as user_schema
from app.models import child as child_model
from app.schemas import child as child_schema
from app.models import department as department_model
from app.schemas import department as department_schema
from app.core.security import get_password_hash

# appインスタンスを作成（サーバ本体）
app = FastAPI()

# ルートURLにアクセスしたときの処理
@app.get("/")
def read_root():
    return {"message": "Famicul API is running!"}

@app.post("/register")
def register_user(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    # 1. すでに同じメールアドレスが登録されていないかチェック
    db_user = db.query(user_model.User).filter(user_model.User.email == user_in.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. パスワードをハッシュ化してモデルを作成
    try:
        hashed_pw = get_password_hash(user_in.password)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error during password processing")
    
    # 3. モデルのインスタンスを作成
    new_user = user_model.User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hashed_pw
    )

    # 4. DBに保存
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "message": "User created successfully!"
    }

@app.post("/children")
def create_child(child_in: child_schema.ChildCreate, db: Session = Depends(get_db)):
    new_child = child_model.Child(
        name=child_in.name,
        gender=child_in.gender,
        birthday=child_in.birthday,
        weight= child_in.weight,
        chronic_disease=child_in.chronic_disease,
        allergy=child_in.allergy,
        user_id=1,
    )

    db.add(new_child)
    db.commit()
    db.refresh(new_child)

    return {
        "name": new_child.name,
        "gender": new_child.gender,
        "birthday": new_child.birthday,
        "chronic_disease": new_child.chronic_disease,
        "allergy": new_child.allergy,
        "message": "Child created successfully!"
    }

@app.post("/department")
def create_department(department_in: department_schema.DepartmentCreate, db: Session = Depends(get_db)):
    new_department = department_model.Department(
        name=department_in.name,
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return {
        "name": new_department.name,
        "message": "Child created successfully!"
    }