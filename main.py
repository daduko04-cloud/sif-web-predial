from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

app = FastAPI(title="SIF WEB - Predial")

@app.get("/")
def root():
    return {"status": "SIF WEB funcionando", "base": "sif_web OK"}

@app.get("/predios")
def listar_predios():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM predios"))
        return [dict(row._mapping) for row in result]

@app.get("/liquidar/{codigo}/{vigencia}")
def liquidar(codigo: str, vigencia: int):
    with engine.connect() as conn:
        avaluo = 100000000
        tarifa = conn.execute(text("SELECT tarifa_mil FROM tarifas_predial WHERE :av BETWEEN desde AND hasta AND vigencia=:v"), {"av": avaluo, "v": vigencia}).fetchone()
        tarifa_val = float(tarifa[0]) if tarifa else 8.0
        impuesto = avaluo * tarifa_val / 1000
        return {"codigo": codigo, "vigencia": vigencia, "avaluo": avaluo, "tarifa_mil": tarifa_val, "impuesto": impuesto}