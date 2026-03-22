
# 🏃 Athlete Injury Prediction System

## 📌 Project Overview

The **Athlete Injury Prediction System** is a Django-based web application that predicts the probability of injury risk in athletes using machine learning.
The system analyzes athlete details such as age, training intensity, fatigue level, and previous injuries to estimate the likelihood of injury.

This project helps coaches, trainers, and athletes take preventive measures to reduce injury risk and improve performance.

---

## 🎯 Features

* 👤 Athlete registration and login system
* 📊 Athlete profile management
* 🤖 Machine learning-based injury prediction
* 📈 Risk probability prediction output
* 🧾 Dashboard for viewing athlete details
* 🔐 Secure authentication system
* 🖥️ User-friendly web interface

---

## 🧠 Machine Learning Model

The injury prediction model is trained using athlete-related data and includes:

* Age
* Gender
* Sport Type
* Training Hours
* Previous Injuries
* Fatigue Level

The trained model is saved using:

* `model.pkl`
* Label encoders (`le_gender.pkl`, `le_sport.pkl`)

---

## 🛠️ Technologies Used

### Backend

* Python 🐍
* Django 🌐

### Frontend

* HTML
* CSS
* Bootstrap

### Machine Learning

* Scikit-learn
* Pandas
* NumPy

### Database

* SQLite

---

## 📂 Project Structure

```
Athlete_injury_system/
│
├── config/              # Django project settings
├── injury/              # Main application
├── ml_model/            # Machine learning model files
├── dataset/             # Training dataset
├── manage.py
├── db.sqlite3
└── README.md
```

---

## ⚙️ Installation Guide

Follow these steps to run the project locally:

### Step 1 — Clone Repository

```
git clone https://github.com/akshay-tv/athlete-injury-prediction.git
```

### Step 2 — Navigate to Project

```
cd Athlete_injury_system
```

### Step 3 — Create Virtual Environment

```
python -m venv venv
```

### Step 4 — Activate Virtual Environment

Windows:

```
venv\Scripts\activate
```

### Step 5 — Install Dependencies

```
pip install -r requirements.txt
```

### Step 6 — Run Server

```
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000/
```

---

## 📊 Prediction Workflow

1. User logs into the system
2. Athlete details are entered
3. Machine learning model processes the data
4. Injury probability is calculated
5. Risk result is displayed to the user

---

## 🚀 Future Improvements

* Improve model accuracy with larger datasets
* Add real-time injury monitoring
* Deploy system to cloud (Render / AWS)
* Add graphical analytics dashboard

---

## 👨‍💻 Author

**Akshay TV**
GitHub: https://github.com/akshay-tv

---


