# Transaction Fraud Detection System

A Machine Learning-powered **Transaction Fraud Detection System** built with **LightGBM**, **FastAPI**, **Streamlit**, and **Docker**. This project predicts whether a financial transaction is fraudulent and provides fraud probability scores through an interactive web interface. In this project data was very unbalanced (only 0.45% were frauds )so i did experiments with class weight and SMOTE and some other imbalancing technequesto handle the unblanced data .

## 🚀 Project Overview

Financial fraud causes billions of dollars in losses every year. This project uses machine learning techniques and feature engineering to identify suspicious transactions in real time.

The application consists of:

* **Machine Learning Model** (LightGBM)
* **FastAPI Backend API**
* **Streamlit Frontend**
* **Dockerized Deployment**
* **Pydantic Data Validation**

---

## 📊 Features

### Machine Learning

* Fraud transaction prediction
* Probability score generation
* LightGBM classification model
* Class imbalance handling
* Feature engineering pipeline

### Data Processing

* Transaction time feature extraction
* Customer age calculation
* Merchant fraud rate encoding
* Category fraud rate encoding
* Distance calculation using geographical coordinates

### Backend

* FastAPI REST API
* Pydantic request validation
* Structured JSON responses
* Error handling

### Frontend

* User-friendly Streamlit interface
* Real-time predictions
* Fraud probability visualization
* Interactive transaction input form

### Deployment

* Docker support
* Portable deployment
* Environment-independent execution

---

## 🛠️ Tech Stack

| Category         | Technology             |
| ---------------- | ---------------------- |
| Language         | Python                 |
| Machine Learning | LightGBM, Scikit-Learn |
| Data Processing  | Pandas, NumPy          |
| API              | FastAPI                |
| Validation       | Pydantic               |
| Frontend         | Streamlit              |
| Visualization    | Matplotlib, Seaborn    |
| Deployment       | Docker                 |

---

## 📁 Project Structure

```text
Transaction-Fraud-Detection/
│
├── DATA/
│   └── fraud_dataset.csv
│
├── MODELS/
│   └── fraud_model.pkl
│
├── NOTEBOOKS/
│   └── experiments.ipynb
│
├── SRC/
│   ├── feature_engineering.py
│   ├── preprocessing.py
│   ├── train.py
│   └── utils.py
│
├── API/
│   ├── main.py
│   └── schema.py
│
├── GUI/
│   └── app.py
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

---

## ⚙️ Feature Engineering

The following features are generated before prediction:

### Time-Based Features

* Unix Timestamp
* Hour of Transaction

### Customer Features

* Age
* Gender

### Transaction Features

* Transaction Amount
* Merchant Risk Score
* Category Risk Score

### Location Features

* Distance from Customer Location

These engineered features significantly improve fraud detection performance.

---

## 📈 Model Performance

The model was trained on a highly imbalanced fraud dataset and optimized for fraud detection.

Evaluation Metrics:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC Score

Since fraud detection is an imbalanced classification problem, **Recall and F1 Score** were prioritized over raw accuracy.

---

## 🔌 API Usage

### Prediction Endpoint

```http
POST /predict
```

### Sample Request

```json
{
  "trans_date_trans_time": "2021-01-01 12:00:00",
  "merchant": "fraud_Abbott-Rogahn",
  "category": "health_fitness",
  "amt": 765,
  "gender": "M",
  "lat": 40.7128,
  "long": -74.0060
}
```

### Sample Response

```json
{
  "prediction": "Fraud",
  "fraud_probability": 96.65
}
```

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t fraud-detection .
```

### Run Docker Container

```bash
docker run -p 8501:8000 fraud-detection
```

After starting the container, open:

```text
http://localhost:8501
```

---

## 💻 Local Installation

### Clone Repository

```bash
git clone https://github.com/adnansaqib180-bit/Transaction-Fraud-Detection.git
```

### Move into Project Directory

```bash
cd Transaction-Fraud-Detection
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

### Start FastAPI Backend

```bash
uvicorn API.main:app --reload
```

### Start Streamlit Frontend

```bash
streamlit run GUI/app.py
```

---

## 🎯 Future Improvements

* Model monitoring
* Database integration
* User authentication
* Cloud deployment (AWS/Azure/GCP)
* Real-time transaction streaming
* Explainable AI (SHAP)

---

## 👨‍💻 Author

**Adnan Saqib**

Machine Learning Engineer

* GitHub: https://github.com/adnansaqib180-bit
* LinkedIn: http://www.linkedin.com/in/adnan-saqib-ml-engineer

---

## 📜 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute this project for educational and research purposes.
