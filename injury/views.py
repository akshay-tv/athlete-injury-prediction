from django.shortcuts import render
from .models import Athlete, Prediction
# Create your views here.
import numpy as np
import joblib
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import time
from django.db.models import Q
from django.contrib import messages





# load model and encoders
model = joblib.load("ml_model/model.pkl")
le_gender = joblib.load("ml_model/le_gender.pkl")
le_sport = joblib.load("ml_model/le_sport.pkl")

def register_view(request):
    time.sleep(2)
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        # Check username exists
        if User.objects.filter(username=username).exists():

            return render(
                request,
                "injury/register.html",
                {
                    "error": "Username already exists. Please choose another."
                }
            )

        # Check email exists
        if User.objects.filter(email=email).exists():

            return render(
                request,
                "injury/register.html",
                {
                    "error": "Email already registered."
                }
            )

        # Create user (no try-except needed)
        User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        messages.success(
            request,
            "Registration successful! You can now login."
        )

        return redirect("login")

    return render(request, "injury/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("predict_injury")
        else:
            return render(request, "injury/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "injury/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def generate_ai_suggestion(
    age,
    sport,
    training,
    fatigue,
    sleep,
    bmi,
    hydration,
    previous,
    result
):

    suggestions = []

    # Fatigue check
    if fatigue >= 8:
        suggestions.append(
            "⚠️ High fatigue detected. Reduce training intensity and allow proper recovery."
        )

    # Sleep check
    if sleep < 6:
        suggestions.append(
            "😴 Sleep duration is low. Aim for at least 7–9 hours to support muscle recovery."
        )

    # Hydration check
    if hydration < 2:
        suggestions.append(
            "💧 Hydration level is low. Increase daily water intake to prevent muscle strain."
        )

    # BMI check
    if bmi > 25:
        suggestions.append(
            "⚖️ BMI is above recommended range. Consider weight control exercises."
        )

    # Previous injuries
    if previous >= 2:
        suggestions.append(
            "🩹 Multiple previous injuries detected. Focus on injury prevention exercises."
        )

    # Training overload
    if training > 4:
        suggestions.append(
            "🏋️ High training duration detected. Ensure proper warm-up and cool-down."
        )

    # Risk-level based suggestion
    if result == "HIGH INJURY RISK":

        suggestions.append(
            "🚨 High injury risk detected. Consider reducing workload and consult a physiotherapist."
        )

    elif result == "MEDIUM INJURY RISK":

        suggestions.append(
            "⚠️ Moderate risk detected. Monitor fatigue and recovery closely."
        )

    else:

        suggestions.append(
            "✅ Low injury risk. Maintain your current training and recovery routine."
        )

    # Final output
    return "\n• " + "\n• ".join(suggestions)


@login_required
def predict_injury(request):
    time.sleep(2)
    if request.method == "POST":
        name = request.POST["name"]
        age = float(request.POST["age"])
        gender = request.POST["gender"]
        sport = request.POST["sport"]
        training = float(request.POST["training"])
        previous = float(request.POST["previous"])
        fatigue = float(request.POST["fatigue"])
        sleep = float(request.POST["sleep"])
        bmi = float(request.POST["bmi"])
        hydration = float(request.POST["hydration"])

        # encode text to numbers
        gender_encoded = le_gender.transform([gender])[0]
        sport_encoded = le_sport.transform([sport])[0]

        # feature engineering (same as training)
        workload = training * fatigue
        recovery = sleep * hydration

        features = np.array([[ 
            age,
            gender_encoded,
            sport_encoded,
            training,
            previous,
            fatigue,
            sleep,
            bmi,
            hydration,
            workload,
            recovery
        ]])

        prediction = model.predict(features)[0]

        proba = model.predict_proba(features)[0]
        proba = [float(x) for x in proba]

        # 👉 ADD THIS (for UI)
        if prediction == 0:
            result = "LOW INJURY RISK"
            width = 30
            color = "green"
        elif prediction == 1:
            result = "MEDIUM INJURY RISK"
            width = 60
            color = "orange"
        else:
            result = "HIGH INJURY RISK"
            width = 90
            color = "red"
        # 🔥 AI SUGGESTION USING GEMINI
   
        ai_text = generate_ai_suggestion(
                age,
                sport,
                training,
                fatigue,
                sleep,
                bmi,
                hydration,
                previous,
                result
        )
        print("Form submitted")    
        
        
        athlete = Athlete.objects.create(
            user=request.user,
            name=name,  # you can add name field later in form
            age=age,
            gender=gender,
            sport=sport,
            training_hours=training,
            previous_injury=previous,
            fatigue_level=fatigue,
            sleep_hours=sleep,
            bmi=bmi,
            hydration_level=hydration
        )
        print("Athlete saved")
        Prediction.objects.create(
            athlete=athlete,
            risk_level=result,
            probability=float(max(proba)),
            ai_suggestion=ai_text
            
        )
        print("prediction saved")

        return render(request, "injury/result.html", {
            "result": result,
            "width": width,
            "color": color,
            "proba": list(proba),  # for charts
            "suggestion": ai_text   # 
        })


    return render(request, "injury/form.html")

@login_required
def dashboard(request):

    query = request.GET.get("q")

    athletes = Athlete.objects.filter(
        user=request.user
    )

    if query:
        athletes = athletes.filter(
            name__icontains=query
        )

    athletes = athletes.order_by("-created_at")

    return render(
        request,
        "injury/dashboard.html",
        {
            "athletes": athletes,
            "query": query
        }
    )
@login_required
def athlete_profile(request, athlete_id):

    athlete = Athlete.objects.get(
        athlete_id=athlete_id,
        user=request.user
    )

    predictions = Prediction.objects.filter(
        athlete=athlete
    ).order_by("-prediction_date")

    return render(
        request,
        "injury/athlete_profile.html",
        {
            "athlete": athlete,
            "predictions": predictions
        }
    )