from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, UserInventory
from django.contrib import messages
from django.db.models import Sum
from tasks.models import Task, Category

# @login_required
# def profile_stats(request):
#     # Отримуємо ВСІ завдання користувача для тесту
#     user_tasks = Task.objects.filter(user=request.user)
#     print(f"DEBUG: Знайдено завдань: {user_tasks.count()}")

#     stats_query = user_tasks.values(
#         'category__name', 'category__color'
#     ).annotate(
#         total_hours=Sum('estimated_hours')
#     ).order_by('-total_hours')

#     chart_labels = []
#     chart_data = []
#     chart_colors = []

#     for entry in stats_query:
#         # Логіка для завдань без категорії
#         name = entry['category__name'] if entry['category__name'] else "Без категорії"
#         color = entry['category__color'] if entry['category__color'] else "#cccccc"
#         hours = float(entry['total_hours'] or 0)

#         if hours > 0: # Додаємо в графік тільки те, де є час
#             chart_labels.append(name)
#             chart_data.append(hours)
#             chart_colors.append(color)

#     print(f"DEBUG: Дані для графіка: {chart_labels} - {chart_data}")

#     context = {
#         'user': request.user,
#         'chart_labels': chart_labels,
#         'chart_data': chart_data,
#         'chart_colors': chart_colors,
#         'stats_summary': zip(chart_labels, chart_data, chart_colors)
#     }
#     return render(request, 'profile_app/profile.html', context)



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

    # --- ДОДАЄМО БЛОК СТАТИСТИКИ ---
    stats_query = Task.objects.filter(user=request.user).values(
        'category__name', 'category__color'
    ).annotate(
        total_hours=Sum('estimated_hours')
    ).order_by('-total_hours')

    chart_labels = []
    chart_data = []
    chart_colors = []

    for entry in stats_query:
        name = entry['category__name']
        color = entry['category__color']
        hours = float(entry['total_hours'] or 0)

        if hours > 0:
            # Якщо ім'я порожнє (завдання без категорії)
            if not name:
                chart_labels.append("Інше")
                chart_colors.append("#f0f0f0") # Світло-сірий для "Іншого"
            else:
                chart_labels.append(name)
                # Якщо колір в базі чорний або відсутній, дамо випадковий або стандартний
                if not color or color == "#000000":
                    chart_colors.append("#1f4d2b") # Наприклад, ваш зелений за замовчуванням
                else:
                    chart_colors.append(color)

            chart_data.append(hours)

    user = request.user
    user_rating = None
    # Перевіримо, чи є рейтинг у користувача
    if hasattr(user, "rating"):
        user_rating = user.rating
    # --- ФОРМУЄМО КОНТЕКСТ ---
    context = {
        'all_items': all_items,
        'owned_slugs': owned_slugs,
        'equipped_slugs': equipped_slugs,
        'user': user, # тут будуть монети: {{ user.coins }}
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'chart_colors': chart_colors,
        'stats_summary': list(zip(chart_labels, chart_data, chart_colors)),
        "user_rating": user_rating,
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
        messages.error(request, f'Недостатньо монет! У тебе лише {user.coins}!')
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
