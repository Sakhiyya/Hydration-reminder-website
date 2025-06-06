from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, ProfileUpdateForm
import joblib
import os

# Load the ML model once at the top
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml_model', 'water_intake_model.pkl')
model = joblib.load(MODEL_PATH)

def home(request):
    result_text = None

    if request.method == "POST":
        try:
            # Retrieve form data
            temperature = request.POST.get("temperature")
            activity = request.POST.get("activity")
            sleep = request.POST.get("sleep")
            weight = request.POST.get("weight")
            exercise = request.POST.get("exercise")
            height = request.POST.get("height")

            # Check for missing fields
            if not all([temperature, activity, sleep, weight, exercise, height]):
                raise ValueError("Please fill in all fields.")

            # Convert to proper types
            temperature = float(temperature)
            sleep = float(sleep)
            weight = float(weight)
            height = float(height)

            # Validate numeric values
            if weight <= 0:
                raise ValueError("Weight must be a positive number.")
            if sleep < 0 or sleep > 24:
                raise ValueError("Sleep duration must be between 0 and 24 hours.")
            if temperature < -50 or temperature > 60:
                raise ValueError("Please enter a valid temperature.")
            if height < 50 or height > 250:
                raise ValueError("Please enter a valid height in cm (between 50 and 250).")

            # Normalize input strings
            activity = activity.lower()
            exercise = exercise.lower()

            # Encode activity
            activity_level_map = {"low": 0, "medium": 1, "high": 2}
            if activity not in activity_level_map:
                raise ValueError("Invalid activity level. Choose low, medium, or high.")
            activity_level = activity_level_map[activity]

            # Encode exercise
            exercised = 1 if exercise == "yes" else 0

            # Prepare input for model
            model_input = [[temperature, activity_level, sleep, weight, exercised]]

            # Predict using the ML model
            predicted_liters = model.predict(model_input)[0]

            result_text = f"Your recommended daily water intake is approximately {predicted_liters:.2f} liters 💧"


        except ValueError as e:
            messages.error(request, f"⚠️ {e}")
        except Exception:
            messages.error(request, "⚠️ Unexpected error. Please try again.")

    return render(request, "ui/home.html", {"result": result_text})



# ---------- Authentication and Profile Views ----------

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created for {user.username}!")
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'ui/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'ui/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'ui/profile.html', {'p_form': p_form})
