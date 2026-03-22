from django.db import models
from django.contrib.auth.models import User

class Coach(models.Model):
    coach_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    
class Athlete(models.Model):
    athlete_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    sport = models.CharField(max_length=50)
    training_hours = models.FloatField()
    previous_injury = models.IntegerField()
    fatigue_level = models.IntegerField()
    sleep_hours = models.FloatField()
    bmi = models.FloatField()
    hydration_level = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Prediction(models.Model):
    prediction_id = models.AutoField(primary_key=True)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)

    risk_level = models.CharField(max_length=20)
    probability = models.FloatField()

    # 🔥 AI suggestion (you wanted this)
    ai_suggestion = models.TextField(blank=True, null=True)

    prediction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.athlete.name} - {self.risk_level}"