import pytest

from django.utils import timezone
from django.contrib.auth import get_user_model
from lunch_menu.models import MealMenu, MenuUser

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        username='john_doe', name='John Doe', user_type='employee'
    )
    assert user.username == 'john_doe'
    assert user.name == 'John Doe'
    assert user.user_type == 'employee'
    assert not user.is_staff


@pytest.mark.django_db
def test_user_string_representation():
    user = User.objects.create_user(
        username='jane_doe', name='Jane Doe', user_type='employee'
    )
    assert str(user) == 'jane_doe'


@pytest.mark.django_db
def test_create_mealmenu():
    restaurant = MenuUser.objects.create_user(
        username='restaurant1', name='Restaurant 1', user_type='restaurant'
    )
    meal = MealMenu.objects.create(
        name='Cheese Pizza',
        description='Delicious cheese pizza',
        menu_content='Cheese, Tomato Sauce, Dough',
        price=9.99,
        restaurant=restaurant,
        upload_date=timezone.now()
    )
    assert meal.name == 'Cheese Pizza'
    assert meal.description == 'Delicious cheese pizza'
    assert meal.price == 9.99


@pytest.mark.django_db
def test_mealmenu_string_representation():
    restaurant = MenuUser.objects.create_user(
        username='restaurant2', name='Restaurant 2', user_type='restaurant'
    )
    meal = MealMenu.objects.create(
        name='Veggie Pizza',
        restaurant=restaurant,
        price=8.99,  # Provide a default or missing price here
        upload_date=timezone.now()
    )
    assert str(meal) == 'Veggie Pizza'