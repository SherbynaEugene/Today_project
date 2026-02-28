from django.db import models
from django.conf import settings

class Item(models.Model):
    SLOT_CHOICES = [
        ('mouth', 'Рот'),
        ('eyes_l', 'Ліве око'),
        ('eyes_r', 'Праве око'),
        ('head_top', 'Верх голови (волосся/шапки)'),
        ('torso', 'Тіло'),
        ('legs_l', 'Ліва нога'),
        ('legs_r', 'Права нога'),
        ('arms_l', 'Ліва рука'),
        ('arms_r', 'Права рука'),
        ('feet', 'Взуття'),
        ('none', 'Без слота (аксесуари)'),
    ]

    name = models.CharField("Назва", max_length=100)
    slug = models.SlugField("ID для коду (slug)", unique=True) # Це має збігатися з твоїм HTML
    price = models.IntegerField("Ціна", default=10)
    slot = models.CharField("Слот", max_length=20, choices=SLOT_CHOICES, default='none')
    css_id = models.CharField("CSS ID", max_length=50, blank=True, null=True)
    icon = models.CharField("Іконка (emoji)", max_length=10, default="📦") # Щоб бачити, що купуємо

    def __str__(self):
        return f"{self.name} ({self.get_slot_display()})"


class UserInventory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inventory'
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_equipped = models.BooleanField("Одягнено зараз", default=False)
    # is_owned ми прибрали

    class Meta:
        unique_together = ('user', 'item')
        verbose_name = "Предмет користувача"
        verbose_name_plural = "Інвентар"

    def __str__(self):
        status = "Одягнено" if self.is_equipped else "У шафі"
        # Використовуємо username або email залежно від твоєї моделі User
        return f"{self.user.username} — {self.item.name} ({status})"
