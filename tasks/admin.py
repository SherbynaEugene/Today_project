from django.contrib import admin

from django.contrib import admin
from .models import Category, Task, SubTask

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Відображаємо назву та колір у списку
    list_display = ('name', 'user', 'color')

    # Додаємо можливість редагувати колір прямо зі списку (опціонально)
    list_editable = ('color',)

# Також зареєструємо завдання, щоб їх було видно
admin.site.register(Task)
admin.site.register(SubTask)
