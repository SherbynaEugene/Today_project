from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, UserInventory

@login_required
def profile_view(request):
    user = request.user

    # Отримуємо все, що є в інвентарі цього юзера
    user_inventory = UserInventory.objects.filter(user=user)

    # Перетворюємо в прості списки ['head', 'hat', 'smile']
    owned_slugs = list(user_inventory.values_list('item__slug', flat=True))
    equipped_slugs = list(user_inventory.filter(is_equipped=True).values_list('item__slug', flat=True))

    # Твій ручний список для крамниці
    all_items = Item.objects.all()
    # all_items = [
    #     {'slug': 'head', 'name': 'ГОЛОВА', 'price': 200, 'icon': '○'},
    #     {'slug': 'arm-l', 'name': 'ЛІВА РУКА', 'price': 10, 'icon': '/'},
    #     {'slug': 'arm-r', 'name': 'ПРАВА РУКА', 'price': 10, 'icon': '\\'},
    #     {'slug': 'eye-l', 'name': 'ЛІВЕ ОКО', 'price': 10, 'icon': '👀'},
    #     {'slug': 'hat', 'name': 'КАПЕЛЮХ', 'price': 500, 'icon': '🎩'},
    #     {'slug': 'shirt-red-black', 'name': 'КОФТА', 'price': 10, 'icon': '👕'},

    #     # Додавай сюди інші предмети, головне щоб slug збігався з адмінкою
    # ]

    context = {
        'all_items': all_items,
        'owned_slugs': owned_slugs,
        'equipped_slugs': equipped_slugs,
        'user': user, # тут будуть монети: {{ user.coins }}
    }
    return render(request, 'myapp/profile.html', context)

@login_required
def buy_item(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    user = request.user

    if user.coins >= item.price:
        inventory_obj, created = UserInventory.objects.get_or_create(user=user, item=item)
        if created:
            user.coins -= item.price
            user.save()
            # Викликаємо toggle_item, щоб він одягнувся з урахуванням слотів
            return toggle_item(request, item_slug)
    else:
        pass

    return redirect('profile_app:main')

@login_required
def toggle_item(request, item_slug):
    # 1. Знаходимо предмет, який юзер хоче одягнути/зняти
    user_item = get_object_or_404(UserInventory, user=request.user, item__slug=item_slug)

    # 2. Якщо предмет зараз НЕ одягнений, ми хочемо його ОДЯГНУТИ
    if not user_item.is_equipped:
        # ЛОГІКА СЛОТІВ:
        # Шукаємо всі предмети В ТОМУ Ж СЛОТІ, які вже одягнені на юзера
        current_slot = user_item.item.slot

        # Якщо предмет має слот (не 'none'), знімаємо всі інші предмети цього слоту
        if current_slot != 'none':
            UserInventory.objects.filter(
                user=request.user,
                item__slot=current_slot,
                is_equipped=True
            ).update(is_equipped=False)

        # Тепер одягаємо наш предмет
        user_item.is_equipped = True
    else:
        # 3. Якщо предмет уже був одягнений — просто знімаємо його
        user_item.is_equipped = False

    user_item.save()
    return redirect('profile_app:main')
