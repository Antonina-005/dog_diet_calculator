"""Модуль расчета суточной нормы сухого и влажного корма для собак."""

import math

print("=== КАЛЬКУЛЯТОР ПИТАНИЯ ДЛЯ СОБАК ===")

# --- 1. НАСТРОЙКИ КАЛОРИЙНОСТИ КОРМОВ (ккал / 100г) ---
DEFAULT_DRY_KCAL = 350.0
DEFAULT_WET_KCAL = 90.0

# --- 2. СБОР РАСШИРЕННЫХ ДАННЫХ ---
dog_name = input("Как зовут вашу собаку?: ").strip().capitalize()
dog_breed = input(f"Укажите породу {dog_name}: ").strip().capitalize()

# Выбор пола с валидацией
while True:
    dog_gender = input(
        f"Укажите пол {dog_name} (кобель/сука): "
    ).strip().lower()
    if dog_gender in ["кобель", "сука"]:
        break
    print("Ошибка: please, введите строго 'кобель' или 'сука'.")

# Запрашиваем возраст
while True:
    try:
        dog_age = float(
            input(f"Сколько лет {dog_name} (например, 2 или 0.5): ").strip()
        )
        if 0 < dog_age <= 30:
            break
        print("Ошибка: введите реальный возраст собаки (от 0.1 до 30)!")
    except ValueError:
        print("Ошибка: возраст должен быть числом. Пример: 3 или 0.5")

# Запрашиваем текущий и идеальный вес
while True:
    try:
        current_weight = float(
            input(f"Введите ТЕКУЩИЙ вес {dog_name} (в кг): ").strip()
        )
        ideal_weight = float(
            input(f"Введите ИДЕАЛЬНЫЙ вес {dog_name} (в кг): ").strip()
        )
        if current_weight > 0 and ideal_weight > 0:
            break
        print("Ошибка: вес должен быть больше нуля!")
    except ValueError:
        print("Ошибка: пожалуйста, вводите только числа через точку.")


# --- 3. АНАЛИЗ СТАТУСА ВЕСА И СТАБИЛИЗАЦИЯ ---
diff_percent = ((current_weight - ideal_weight) / ideal_weight) * 100

if dog_age < 1.0:
    weight_status = "активный рост (щенок)"
    coef = 2.5
    advice = "✅ Повышенная калорийность для правильного развития щенка."
elif dog_age >= 7.0:
    weight_status = "пожилой возраст"
    coef = 1.2 if dog_gender == "сука" else 1.4
    advice = "⚠️ Метаболизм замедлен. Порция снижена во избежание ожирения."
else:
    base_coef = 1.5 if dog_gender == "сука" else 1.6
    if diff_percent > 10.0:
        weight_status = "избыточный вес"
        coef = base_coef - 0.2
        advice = "⚠️ Порция снижена для плавного похудения до идеального веса."
    elif diff_percent < -10.0:
        weight_status = "дефицит веса"
        coef = base_coef + 0.2
        advice = "⚠️ Порция увеличена для безопасного набора мышечной массы."
    else:
        weight_status = "идеальный баланс"
        coef = base_coef
        advice = "✅ Отличный вес! Нагрузка рассчитана на поддержание формы."


# --- 4. РАСЧЕТ СУТОЧНОЙ ПОРЦИИ, ВОДЫ И ГРАФИКА ---
rer = 70 * math.pow(current_weight, 0.75)
total_kcal_needed = rer * coef

# Делим калории строго пополам (50/50)
kcal_per_meal = total_kcal_needed / 2

dry_grams = int(kcal_per_meal / (DEFAULT_DRY_KCAL / 100))
wet_grams = int(kcal_per_meal / (DEFAULT_WET_KCAL / 100))

# Расчет нормы воды (55 мл на 1 кг)
water_ml = int(current_weight * 55)

# Настройка кратности кормления на основе возраста
if dog_age < 0.4:  # До 5 месяцев
    meals_count = 4
    schedule = "08:00 | 12:00 | 16:00 | 20:00 (интервал 4 часа)"
elif dog_age < 1.0:  # От 5 месяцев до года
    meals_count = 3
    schedule = "08:00 | 14:00 | 20:00 (интервал 6 часов)"
else:  # Взрослые и пожилые
    meals_count = 2
    schedule = (
        "08:00 утром и 20:00 вечером "
        "(идеальный интервал 12 часов)"
    )


# --- 5. ВЫВОД КРАСИВОГО СУТОЧНОГО ОТЧЕТА ---
print("\n==========================================")
print(f" ВЕТЕРИНАРНЫЙ ОТЧЕТ ДЛЯ: {dog_name.upper()}")
print(f" Порода: {dog_breed} | Пол: {dog_gender}")
print(f" Статус состояния: {weight_status.upper()}")
print(f" Рекомендация: {advice}")
print("==========================================")
print("📋 РЕКОМЕНДУЕМЫЙ СУТОЧНЫЙ РАЦИОН:")
print(f" ☀️ УТРО (Сухой корм): {dry_grams} грамм всего")
print(f" 🌙 ВЕЧЕР (Влажный корм): {wet_grams} грамм всего")
print(f" 💧 МИНИМУМ ВОДЫ В СУТКИ: {water_ml} мл")
print("==========================================")
print("⏱️ РЕЖИМ И ГРАФИК КОРМЛЕНИЯ:")
print(f" Количество кормлений в сутки: {meals_count}")
print(f" Рекомендуемые часы: {schedule}")

if meals_count > 2:
    # Считаем разовую порцию для щенков
    single_dry = int(dry_grams / (meals_count - 1))
    print(f" На заметку: делите сухой корм по {single_dry}г на первые приемы,")
    print(f" а влажный корм {wet_grams}г давайте в финальное вечернее время.")

print("==========================================")
print("💡 ДОПОЛНИТЕЛЬНЫЕ СОВЕТЫ ПО КОРМЛЕНИЮ:")
print(" 1. Не смешивайте сухой и влажный корм в один прием пищи.")

if dog_age < 1.0:
    print(" 2. Стабильный график защищает щенка от скачков глюкозы в крови.")
elif weight_status == "избыточный вес":
    print(" 2. Искуственные лакомства замените на кусочки свежего огурца.")
else:
    print(" 2. Наливайте свежую фильтрованную воду дважды в день.")

print("==========================================\n")
