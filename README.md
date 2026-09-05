# 🚀 Müşteri Churn Karar Destek Sistemi (KDS)

Bu proje, şirketlerin operasyonel müşteri süreçlerini yönetirken aynı zamanda makine öğrenmesi algoritmalarıyla müşteri kayıp (churn) riskini tahmin etmelerini sağlayan **N-Katmanlı bir Karar Destek Sistemidir.** 

Proje, operasyonel veri yönetimi ile analitik zekayı (AI) izole ama entegre bir şekilde çalıştırarak tam bir kurumsal mimari yaklaşımı sunar.

## 🎯 Proje Vizyonu ve Mimari
Sistem iki ana omurgadan oluşmaktadır:
1. **Operasyonel CRM (C# / ASP.NET Core MVC):** Müşteri verilerinin sisteme girildiği, güncellendiği ve veritabanı bütünlüğünün (Entity Framework Core) sağlandığı operasyonel katmandır.
2. **Analitik KDS Paneli (Python / Streamlit & FastAPI):** Veritabanındaki güncel verileri okuyan, **K-Nearest Neighbors (KNN)** algoritması ile müşterilerin churn (terk etme) riskini % olarak hesaplayan ve **Büyük Dil Modelleri (LLM)** entegrasyonu ile risk grubuna özel otomatik kampanya/e-posta metinleri üreten zeki katmandır.

## ✨ Temel Özellikler
* **CRUD Operasyonları:** Kullanıcı dostu arayüz ile müşteri kayıtlarının yönetimi.
* **Otomatik ID Yönetimi:** Veritabanı kimlik (Identity) kısıtlamalarına takılmadan C# üzerinden akıllı ID atama algoritması.
* **Makine Öğrenmesi (ML) Entegrasyonu:** Müşteri hareketlerine göre anlık risk skorlaması.
* **AI Destekli Aksiyon Paneli:** LM Studio (LLM) API entegrasyonu sayesinde yüksek riskli müşteriler için saniyeler içinde "Geri Kazanım E-Postası" taslağı oluşturma.
* **Görsel Veri Analitiği:** Plotly ile oluşturulmuş, anlık veritabanı durumunu yansıtan interaktif gösterge panelleri (Dashboard).

## 🛠️ Kullanılan Teknolojiler
**Backend & Operasyonel Katman**
* C# & ASP.NET Core MVC (UI ve İş Mantığı)
* Entity Framework Core (ORM)
* MS SQL Server (Veritabanı)

**Yapay Zeka & Analitik Katman**
* Python (Veri Bilimi ve API)
* FastAPI & Uvicorn (Makine Öğrenmesi Modeli Sunumu)
* Streamlit (Yönetici Dashboard Arayüzü)
* Scikit-Learn (KNN Sınıflandırma Modeli)
* Pandas, NumPy, Plotly (Veri Manipülasyonu ve Görselleştirme)

## 📸 Ekran Görüntüleri

| Operasyonel CRM (MVC) | Analitik Dashboard (Streamlit) |
| :---: | :---: |
| ![CRM Ekranı](Buraya_CRM_Ekran_Goruntusunun_Linkini_Koyun.png) | ![Dashboard Ekranı](Buraya_Dashboard_Ekran_Goruntusunun_Linkini_Koyun.png) |

| AI Aksiyon Paneli | Risk Analiz Grafikleri |
| :---: | :---: |
| ![Aksiyon Ekranı](Buraya_Aksiyon_Ekran_Goruntusunun_Linkini_Koyun.png) | ![Grafik Ekranı](Buraya_Grafik_Ekran_Goruntusunun_Linkini_Koyun.png) |

## 🚀 Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

### 1. Veritabanı ve C# (MVC) Katmanının Ayağa Kaldırılması
1. `MVC_Operasyonel_CRM` klasöründeki `Churn.sln` dosyasını Visual Studio ile açın.
2. `appsettings.json` içerisindeki `DefaultConnection` SQL Server bağlantı dizenizi (Connection String) kendi veritabanı sunucunuza göre güncelleyin.
3. Package Manager Console (PMC) üzerinden veritabanını oluşturmak için `Update-Database` komutunu çalıştırın.
4. Projeyi çalıştırarak (IIS Express / Kestrel) operasyonel CRM panelini ayağa kaldırın.

### 2. Yapay Zeka Katmanının (FastAPI & Streamlit) Çalıştırılması
1. Yeni bir terminal açın ve `YapayZeka_Ve_Panel` klasörüne gidin.
2. Gerekli Python kütüphanelerini kurmak için `pip install -r requirements.txt` komutunu çalıştırın.
3. Klasör içindeki `.env.example` dosyasının adını `.env` olarak değiştirin ve içindeki API/Veritabanı linklerini sisteminize göre ayarlayın.
4. **FastAPI** makine öğrenmesi sunucusunu başlatmak için `uvicorn Churn_FastAPI:app --reload` komutunu kullanın.
5. Farklı bir terminal açıp **Streamlit** yönetici panelini başlatmak için `streamlit run Churn_UI.py` komutunu çalıştırın.
   ```bash
   Update-Database
