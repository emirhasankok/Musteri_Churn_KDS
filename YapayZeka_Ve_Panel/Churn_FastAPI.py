from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import uvicorn
import os

app = FastAPI()

MODEL_PATH = "knn_churn_model.pkl"
SCALER_PATH = "scaler.pkl" 

if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    raise RuntimeError("KRİTİK HATA: Model veya Scaler dosyası bulunamadı! API başlatılamıyor.")

knn_model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

class MusteriVerisi(BaseModel):
    Yas: int
    Kullanim_Suresi_Ay: int
    Aylik_Harcama_TL: float
    Destek_Talebi_Sayisi: int
    Son_Giris_Gunu: int

@app.post("/predict")
def predict_churn(veri: MusteriVerisi):
    features = np.array([[veri.Yas, veri.Kullanim_Suresi_Ay, veri.Aylik_Harcama_TL, 
                          veri.Destek_Talebi_Sayisi, veri.Son_Giris_Gunu]])
    
    features_scaled = scaler.transform(features)
    
    churn_tahmini = int(knn_model.predict(features_scaled)[0])
    churn_olasiligi = float(knn_model.predict_proba(features_scaled)[0][1])
    risk_yuzdesi = round(churn_olasiligi * 100, 2)
    
    if risk_yuzdesi == 100: durum = "Müşteri Kayıp"
    elif risk_yuzdesi >= 70: durum = "Yüksek Risk"
    elif risk_yuzdesi >= 40: durum = "Orta Risk"
    elif risk_yuzdesi >= 20: durum = "Düşük Risk"
    else: durum = "Risk Yok"
    
    return {
        "Churn_Tahmini": churn_tahmini,
        "Risk_Yuzdesi": risk_yuzdesi,
        "Durum": durum
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)