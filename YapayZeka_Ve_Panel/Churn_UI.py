import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import os
from dotenv import load_dotenv
from Churn_DB import gercek_veritabanindan_getir

load_dotenv()
FASTAPI_URL = os.getenv("FASTAPI_URL")
LLM_API_URL = os.getenv("LLM_API_URL")

st.set_page_config(page_title="Gelişmiş KDS Dashboard", layout="wide")
st.title("📊 Yönetici Aksiyon Paneli")

if st.button("🔄 Verileri Yenile"):
    st.cache_data.clear()
    
@st.cache_data
def tum_riskleri_hesapla():
    df = gercek_veritabanindan_getir()
    
    if 'Musteri_ID' not in df.columns:
        df['Musteri_ID'] = [f"CUST-{i+1000}" for i in range(len(df))]
        
    riskler, durumlar = [], []
    
    for _, row in df.iterrows():
        veri = {
            "Yas": int(row['Yas']), 
            "Kullanim_Suresi_Ay": int(row['Kullanim_Suresi_Ay']),
            "Aylik_Harcama_TL": float(row['Aylik_Harcama_TL']), 
            "Destek_Talebi_Sayisi": int(row['Destek_Talebi_Sayisi']),
            "Son_Giris_Gunu": int(row['Son_Giris_Gunu'])
        }
        try:
            res = requests.post(FASTAPI_URL, json=veri).json()
            riskler.append(res["Risk_Yuzdesi"])
            durumlar.append(res["Durum"])
        except:
            riskler.append(0)
            durumlar.append("Hata")
            
    df['Risk_Yuzdesi'] = riskler
    df['Durum'] = durumlar
    return df

def ai_istek_at(prompt_metni):
    try:
        lm_response = requests.post(
            LLM_API_URL,
            json={
                "messages": [
                    {"role": "system", "content": "Sen profesyonel bir CRM stratejistisin. Sadece istenen maddeleri ver."},
                    {"role": "user", "content": prompt_metni}
                ],
                "temperature": 0.7, 
                "max_tokens": 300
            }, 
            timeout=15
        )
        if lm_response.status_code == 200:
            st.info(lm_response.json()["choices"][0]["message"]["content"])
        else:
            st.error(f"LM Studio API Hatası: {lm_response.status_code}")
    except:
        st.error("LM Studio bağlantı hatası. Local sunucunun açık olduğundan emin olun.")

with st.spinner("Tüm veritabanı taranıyor ve risk skorları hesaplanıyor..."):
    df_tamami = tum_riskleri_hesapla()

st.markdown("---")
st.subheader("📊 Sistem Genel Özeti")
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

col_kpi1.metric("Toplam Müşteri", f"{len(df_tamami)}")
col_kpi2.metric("Ortalama Risk", f"%{df_tamami['Risk_Yuzdesi'].mean():.1f}")
col_kpi3.metric("Ortalama Harcama", f"{df_tamami['Aylik_Harcama_TL'].mean():.0f} ₺")
col_kpi4.metric("Toplam Destek Talebi", f"{df_tamami['Destek_Talebi_Sayisi'].sum()}")

st.markdown("---")
st.subheader("📊 Karar Destek Sistemi Görsel Analizleri")

col_grafik1, col_grafik2 = st.columns(2)

with col_grafik1:
    fig_pie = px.pie(
        df_tamami, 
        names='Durum', 
        title='Müşteri Risk Dağılımı',
        hole=0.4, 
        color='Durum',
        color_discrete_map={
            "Yüksek Risk": "#ff4b4b", 
            "Orta Risk": "#ffa421",   
            "Müşteri Kayıp": "#1f1f1f",
            "Risk Yok": "#00CC11" 
        }
    )
    fig_pie.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    st.plotly_chart(fig_pie, use_container_width=True)
    
with col_grafik2:
    fig_box = px.box(
        df_tamami, 
        x='Durum', 
        y='Kullanim_Suresi_Ay', 
        color='Durum',
        title='Risk Gruplarına Göre Sistemde Kalma Süresi (Ay)',
        color_discrete_map={
            "Yüksek Risk": "#ff4b4b", 
            "Orta Risk": "#ffa421",   
            "Müşteri Kayıp": "#1f1f1f",
            "Risksiz / Güvende": "#00CC96" 
        }
    )
    fig_box.update_layout(margin=dict(t=40, b=0, l=0, r=0), showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

col_grafik3, col_grafik4 = st.columns(2)

with col_grafik3:
    fig_age = px.histogram(
        df_tamami, 
        x='Yas', 
        nbins=15, 
        title='Müşteri Yaş Dağılımı', 
        color_discrete_sequence=['#636EFA']
    )
    fig_age.update_layout(margin=dict(t=40, b=0, l=0, r=0), bargap=0.1)
    st.plotly_chart(fig_age, use_container_width=True)
    
with col_grafik4:
    fig_spend = px.histogram(
        df_tamami, 
        x='Aylik_Harcama_TL', 
        nbins=20, 
        title='Aylık Harcama Dağılımı (TL)', 
        color_discrete_sequence=['#00CC96']
    )
    fig_spend.update_layout(margin=dict(t=40, b=0, l=0, r=0), bargap=0.1)
    st.plotly_chart(fig_spend, use_container_width=True)
    
st.markdown("---")
st.subheader("📈 Genel Sistem ve Churn Analitiği")

df_kayip = df_tamami[df_tamami['Durum'] == "Müşteri Kayıp"] 
df_aktif = df_tamami[df_tamami['Durum'] != "Müşteri Kayıp"]

if not df_kayip.empty:
    kritik_gun = int(df_kayip['Son_Giris_Gunu'].median())
    kritik_talep = round(df_kayip['Destek_Talebi_Sayisi'].mean(), 1)
    medyan_sure = df_tamami['Kullanim_Suresi_Ay'].median()

    kisa_sureli_churn = len(df_kayip[df_kayip['Kullanim_Suresi_Ay'] <= medyan_sure]) / len(df_tamami[df_tamami['Kullanim_Suresi_Ay'] <= medyan_sure]) * 100
    uzun_sureli_churn = len(df_kayip[df_kayip['Kullanim_Suresi_Ay'] > medyan_sure]) / len(df_tamami[df_tamami['Kullanim_Suresi_Ay'] > medyan_sure]) * 100

    sadakat_durumu = "Yeni müşterilerde kayıp daha yüksek." if kisa_sureli_churn > uzun_sureli_churn else "Eski müşterilerde kayıp daha yüksek."
else:
    kritik_gun, kritik_talep, kisa_sureli_churn, uzun_sureli_churn = 0, 0, 0, 0
    sadakat_durumu = "Sistemde henüz kayıp müşteri yok."

col_analiz1, col_analiz2, col_analiz3 = st.columns(3)
col_analiz1.metric(label="Kritik İnaktiflik Eşiği", value=f"{kritik_gun} Gün", help="Kaybedilen müşterilerin büyük çoğunluğu bu süreden sonra geri dönmemiştir.")
col_analiz2.metric(label="Kritik Şikayet Eşiği", value=f"{kritik_talep} Talep", help="Müşteriler ortalama bu sayıda destek talebi açtıktan sonra sistemi terk ediyor.")
col_analiz3.metric(label="Sadakat / Kayıp Analizi", value=f"%{round(max(kisa_sureli_churn, uzun_sureli_churn), 1)}", delta=sadakat_durumu, delta_color="off")

st.markdown("---")
st.subheader("Müşteri Segmentleri ve Aksiyon Paneli")

def durum_renklendir(durum):
    if "Yüksek" in str(durum): return "🔴 " + str(durum)
    elif "Orta" in str(durum): return "🟡 " + str(durum)
    elif "Kayıp" in str(durum): return "⚫ " + str(durum)
    else: return "🟢 " + str(durum)

df_tamami['Gorsel_Durum'] = df_tamami['Durum'].apply(durum_renklendir)

with st.expander("🔍 Gelişmiş Müşteri Filtreleme (Görüntülemek İçin Tıklayın)", expanded=False):
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    with col_f1:
        risk_filtre = st.selectbox("Minimum Risk Seviyesi", ["Hepsi", "%40 ve Üzeri", "%60 ve Üzeri"])
    with col_f2:
        min_yas, max_yas = int(df_tamami['Yas'].min()), int(df_tamami['Yas'].max())
        secilen_yas = st.slider("Yaş Aralığı", min_yas, max_yas, (min_yas, max_yas))
    with col_f3:
        min_harcama, max_harcama = float(df_tamami['Aylik_Harcama_TL'].min()), float(df_tamami['Aylik_Harcama_TL'].max())
        secilen_harcama = st.slider("Aylık Harcama (TL)", min_harcama, max_harcama, (min_harcama, max_harcama))
    with col_f4:
        min_talep, max_talep = int(df_tamami['Destek_Talebi_Sayisi'].min()), int(df_tamami['Destek_Talebi_Sayisi'].max())
        secilen_talep = st.slider("Destek Talebi Sayısı", min_talep, max_talep, (min_talep, max_talep))

df_filtrelenmis = df_tamami[
    (df_tamami['Yas'] >= secilen_yas[0]) & (df_tamami['Yas'] <= secilen_yas[1]) &
    (df_tamami['Aylik_Harcama_TL'] >= secilen_harcama[0]) & (df_tamami['Aylik_Harcama_TL'] <= secilen_harcama[1]) &
    (df_tamami['Destek_Talebi_Sayisi'] >= secilen_talep[0]) & (df_tamami['Destek_Talebi_Sayisi'] <= secilen_talep[1])
]

if risk_filtre == "%40 ve Üzeri":
    df_filtrelenmis = df_filtrelenmis[df_filtrelenmis['Risk_Yuzdesi'] >= 40]
elif risk_filtre == "%60 ve Üzeri":
    df_filtrelenmis = df_filtrelenmis[df_filtrelenmis['Risk_Yuzdesi'] >= 60]

ortak_sutun_ayarlari = {
    "Aksiyon_Sec": st.column_config.CheckboxColumn("Aksiyon Seç", default=False),
    "Musteri_ID": st.column_config.TextColumn("Müşteri ID"),
    "Risk_Yuzdesi": st.column_config.ProgressColumn("Kayıp Riski", format="%%%d", min_value=0, max_value=100),
    "Aylik_Harcama_TL": st.column_config.NumberColumn("Aylık Harcama", format="₺%.2f"),
    "Gorsel_Durum": st.column_config.TextColumn("Risk Seviyesi"),
    "Durum": None, 
    "Churn": None
}
kilitli_sutunlar = ["Musteri_ID", "Yas", "Aylik_Harcama_TL", "Destek_Talebi_Sayisi", "Risk_Yuzdesi", "Durum", "Gorsel_Durum", "Kullanim_Suresi_Ay", "Son_Giris_Gunu"]

tab_dusuk, tab_orta, tab_yuksek = st.tabs(["🟢 Düşük / Risksiz Grubu", "🟡 Orta Risk Grubu", "🔴 Yüksek Risk Grubu"])

with tab_yuksek:
    df_yuksek = df_filtrelenmis[df_filtrelenmis['Durum'] == "Yüksek Risk"].copy()
    if not df_yuksek.empty:
        df_yuksek.insert(0, "Aksiyon_Sec", False) 
        st.markdown("### 🔴 Yüksek Riskli Müşteriler")
        
        edited_df_yuksek = st.data_editor(
            df_yuksek, key="tablo_yuksek", column_config=ortak_sutun_ayarlari, 
            hide_index=True, use_container_width=True, disabled=kilitli_sutunlar
        )

        secilen_yuksek = edited_df_yuksek[edited_df_yuksek["Aksiyon_Sec"] == True]
        if not secilen_yuksek.empty:
            st.markdown("---")
            st.subheader("🎯 VIP Aksiyon Paneli (Seçili Müşteriler)")
            for index, row in secilen_yuksek.iterrows():
                musteri_id, risk, harcama = row.get('Musteri_ID', f"ID-{index}"), row['Risk_Yuzdesi'], row['Aylik_Harcama_TL']
                with st.expander(f"Müşteri {musteri_id} İçin Hızlı Aksiyon", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Özel Teklif Üret", key=f"btn_teklif_yuksek_{index}"):
                            ai_istek_at(f"Aylık {harcama} TL harcayan, kayıp riski %{risk} olan müşteri için tek bir anlık özel teklif üret.")
                    with col2:
                        if st.button(f"VIP E-Posta Yaz", key=f"btn_mail_yuksek_{index}"):
                            ai_istek_at(f"Kayıp riski %{risk} olan müşterimize (ID: {musteri_id}), onu geri kazanmaya yönelik samimi bir e-posta taslağı yaz.")
        else:
            st.info("👆 Bireysel panelleri görmek için tablodan müşteri seçin.")
            
        st.markdown("---")
        st.markdown("### 📢 Toplu Kampanya Aksiyonu")
        st.write("Bu gruptaki tüm müşteriler için genel bir kurtarma stratejisi belirle.")
        if st.button("Tüm Yüksek Riskliler İçin Ortak Strateji Üret", key="btn_toplu_yuksek"):
            ort_harcama = df_yuksek['Aylik_Harcama_TL'].mean()
            ai_istek_at(f"Yüksek risk grubunda ortalama {ort_harcama:.2f} TL harcayan bir müşteri kitlemiz var. Bu kitleyi kaybetmemek için tümüne SMS ile gönderilecek çok çarpıcı, 2 cümlelik bir kampanya metni ve ekibe 2 maddelik aksiyon öner.")
    else:
        st.success("Bu filtrelere uygun yüksek riskli müşteriniz bulunmuyor.")

with tab_orta:
    df_orta = df_filtrelenmis[df_filtrelenmis['Durum'] == "Orta Risk"].copy()
    if not df_orta.empty:
        df_orta.insert(0, "Aksiyon_Sec", False) 
        st.markdown("### 🟡 Orta Riskli Müşteriler")
        
        edited_df_orta = st.data_editor(
            df_orta, key="tablo_orta", column_config=ortak_sutun_ayarlari, 
            hide_index=True, use_container_width=True, disabled=kilitli_sutunlar
        )

        secilen_orta = edited_df_orta[edited_df_orta["Aksiyon_Sec"] == True]
        if not secilen_orta.empty:
            st.markdown("---")
            st.subheader("🎯 Hızlı Aksiyon Paneli (Seçili Müşteriler)")
            for index, row in secilen_orta.iterrows():
                musteri_id, risk = row.get('Musteri_ID', f"ID-{index}"), row['Risk_Yuzdesi']
                with st.expander(f"Müşteri {musteri_id} İçin İletişim", expanded=True):
                    if st.button(f"Özel 'Sizi Özledik' E-Postası Yaz", key=f"btn_mail_orta_{index}"):
                        ai_istek_at(f"Kayıp riski %{risk} olan orta riskli müşterimize agresif olmayan, samimi bir 'Sizi Özledik' e-posta taslağı yaz.")
        else:
            st.info("👆 Bireysel panelleri görmek için tablodan müşteri seçin.")
            
        st.markdown("---")
        st.markdown("### 📢 Toplu Kampanya Aksiyonu")
        st.write("Bu gruba agresif indirimler yerine 'Sizi Özledik' temalı genel mailler gönderilebilir.")
        if st.button("Tüm Orta Riskliler İçin Standart E-Posta Şablonu Üret", key="btn_toplu_orta"):
            ai_istek_at("Orta derecede churn riski taşıyan müşterilere gönderilmek üzere, onları geri kazanmaya yönelik samimi bir 'Sizi Özledik' e-posta taslağı yaz.")
    else:
        st.success("Bu filtrelere uygun orta riskli müşteriniz bulunmuyor.")

with tab_dusuk:
    df_dusuk = df_filtrelenmis[~df_filtrelenmis['Durum'].isin(["Orta Risk", "Yüksek Risk", "Müşteri Kayıp"])].copy()
    if not df_dusuk.empty:
        st.markdown("### 🟢 Güvenli Müşteri Segmenti")
        st.write("Bu gruptaki müşterilerin kayıp riski düşüktür. Sistemin sağlığını izlemek için listelenmiştir.")
        
        st.dataframe(df_dusuk, column_config=ortak_sutun_ayarlari, hide_index=True, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🎁 Toplu Sadakat Kampanyası")
        st.write("Bu güvenli gruba çapraz satış veya sadakat/teşekkür mesajları kurgulayabilirsin.")
        if st.button("Düşük Riskliler İçin Sadakat/Teşekkür Mesajı Üret", key="btn_toplu_dusuk"):
            ai_istek_at("Kayıp riski olmayan, sadık ve düzenli müşterilerimize gönderilmek üzere, onlara değer verdiğimizi hissettirecek şık bir teşekkür ve sürpriz hediye e-postası taslağı yaz.")
    else:
        st.info("Bu filtrelere uygun güvenli kategoride listelenecek müşteri bulunmuyor.")