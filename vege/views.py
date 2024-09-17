from django.shortcuts import render, redirect
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Recipe page - requires login
@login_required(login_url="/login/")
def recipes(request):
    # Handle blog submission (POST request)
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        # Save new recipe to the database
        Recipe.objects.create(
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            recipe_image=recipe_image
        )
        return redirect('/recipes/')

    # Retrieve all recipes or filter by search term
    queryset = Recipe.objects.all()
    if request.GET.get('search'):
        search_term = request.GET.get('search')
        queryset = queryset.filter(recipe_name__icontains=search_term)

    context = {'recipes': queryset}
    return render(request, 'recipe.html', context)

# Delete a specific recipe by ID - requires login
@login_required(login_url="/login/")
def delete_recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    recipe.delete()
    return redirect('/recipes/')

# Update a specific recipe by ID - requires login
@login_required(login_url="/login/")
def update_recipe(request, id):
    recipe = Recipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        # Update the recipe details
        recipe.recipe_name = recipe_name
        recipe.recipe_description = recipe_description

        if recipe_image:
            recipe.recipe_image = recipe_image

        recipe.save()
        return redirect('/recipes/')

    context = {'recipe': recipe}
    return render(request, 'update_recipe.html', context)

# Login page for user authentication
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid username")
            return redirect('/login/')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid password or username")
            return redirect('/login/')
        else:
            # Log in the user
            login(request, user)
            return redirect('/recipes/')

    return render(request, 'login.html')

# Logout the user and redirect to the login page
def logout_page(request):
    logout(request)
    return redirect('/login/')

# User registration page
def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/register/')

        # Create new user
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )
        messages.success(request, "Account created successfully")
        return redirect('/login/')

    return render(request, 'register.html')
