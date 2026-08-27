"""Модуль расчета суточной нормы сухого и влажного корма для собак."""

import math

print("=== КАЛЬКУЛЯТОР ПИТАНИЯ ДЛЯ СОБАК ===")

# --- 1. НАСТРОЙКИ КАЛОРИЙНОСТИ КОРМОВ (ккал / 100г) ---
DEFAULT_DRY_KCAL = 350.0
DEFAULT_WET_KCAL = 90.0

# --- 2. СБОР РАСШИРЕННЫХ ДАННЫХ ---
dog_name = input("Как зовут вашу собаку?: ").strip().capitalize()
dog_breed = input(f"Укажите породу {dog_name}: ").strip().capitalize()

# Выбор пола
while True:
    dog_gender = input(
        f"Укажите пол {dog_name} (кобель/сука): "
    ).strip().lower()
    if dog_gender in ["кобель", "сука"]:
        break
    print("Ошибка: введите строго 'кобель' или 'сука'.")

# Выбор особого статуса для сук
pregnancy_status = "1"
if dog_gender == "сука":
    print(f"\n--- Особое состояние {dog_name} ---")
    print("1. Обычное состояние")
    print("2. Беременность (вторая половина)")
    print("3. Кормление щенков (лактация)")
    while True:
        pregnancy_status = input("Выберите вариант (1, 2 или 3): ").strip()
        if pregnancy_status in ["1", "2", "3"]:
            break
        print("Ошибка: введите цифру 1, 2 или 3.")

# Проверка здоровья собаки
while True:
    has_illness = input(
        f"\nУ {dog_name} есть хронические болезни? (да/нет): "
    ).strip().lower()
    if has_illness in ["да", "нет"]:
        break
    print("Ошибка: введите строго 'да' или 'нет'.")

# Выбор статуса стерилизации/кастрации
is_castrated = "нет"
if pregnancy_status == "1":
    status_text = "стерилизована" if dog_gender == "сука" else "кастрирован"
    while True:
        is_castrated = input(
            f"{dog_name} {status_text}? (да/нет): "
        ).strip().lower()
        if is_castrated in ["да", "нет"]:
            break
        print("Ошибка: введите строго 'да' или 'нет'.")

# Выбор уровня активности
print(f"\n--- Уровень активности {dog_name} ---")
print("1. Низкая (диванный режим, короткие прогулки)")
print("2. Умеренная (стандартный выгул дважды в день)")
print("3. Высокая (активные игры, бег, тренировки)")
while True:
    activity_choice = input("Выберите вариант (1, 2 или 3): ").strip()
    if activity_choice in ["1", "2", "3"]:
        break
    print("Ошибка: введите цифру 1, 2 или 3.")

# Выбор типа шерсти
print(f"\n--- Тип шерсти {dog_name} ---")
print("1. Обычная шерсть (короткая или длинная)")
print("2. Голая собака (нет шерсти, повышенный метаболизм)")
while True:
    coat_choice = input("Выберите вариант (1 или 2): ").strip()
    if coat_choice in ["1", "2"]:
        break
    print("Ошибка: введите цифру 1 или 2.")

# Выбор времени года
print("\n--- Выберите текущее время года ---")
print("1. Зима / Холодная осень (нужен обогрев)")
print("2. Лето / Жара (сниженная активность)")
print("3. Весна / Межсезонье (норма)")
while True:
    season_choice = input("Выберите вариант (1, 2 или 3): ").strip()
    if season_choice in ["1", "2", "3"]:
        break
    print("Ошибка: введите цифру 1, 2 или 3.")

# Запрашиваем возраст
while True:
    try:
        dog_age = float(
            input(f"\nСколько лет {dog_name} (например, 2 или 0.5): ").strip()
        )
        if 0 < dog_age <= 30:
            break
        print("Ошибка: введите реальный возраст собаки (от 0.1 до 30)!")
    except ValueError:
        print("Ошибка: возраст должен быть числом. Пример: 3 или 0.5")

# Запрашиваем вес
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
    if is_castrated == "да":
        coef = 1.0 if dog_gender == "сука" else 1.1
    else:
        coef = 1.2 if dog_gender == "сука" else 1.4
    advice = "⚠️ Метаболизм замедлен. Порция снижена во избежание ожирения."
else:
    if is_castrated == "да":
        base_coef = 1.3 if dog_gender == "сука" else 1.4
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

# --- КОРРЕКТИРОВКА НА ОСОБЫЕ ФАКТОРЫ ---
if pregnancy_status == "2":
    coef = 2.0
    weight_status = "беременность (особый статус)"
    advice = "🍼 Особый рацион для беременной суки (поддержка плодов)."
elif pregnancy_status == "3":
    coef = 3.5
    weight_status = "лактация (выкармливание)"
    advice = "🍼 Максимальный рацион для кормящей мамы. Еда без ограничений!"

# Корректировки только для небеременных взрослых/пожилых
if pregnancy_status == "1" and dog_age >= 1.0:
    # 1. Корректировка на активность
    if activity_choice == "1":
        coef -= 0.15
    elif activity_choice == "3":
        coef += 0.20

    # 2. Корректировка на отсутствие шерсти
    if coat_choice == "2":
        coef += 0.20
        advice += (
            " 🐕 Голая собака: добавлена энергия на "
            "постоянный термообогрев."
        )

    # 3. Корректировка на сезон
    if season_choice == "1":
        coef += 0.15
        advice += " ❄️ Учтена зимняя надбавка на обогрев."
    elif season_choice == "2":
        coef -= 0.10
        advice += " ☀️ Порция уменьшена из-за летней жары."


# --- 4. РАСЧЕТ СУТОЧНОЙ ПОРЦИИ, ВОДЫ И ГРАФИКА ---
# Защита от слишком сильного урезания коэффициента в минимуме
if coef < 0.9:
    coef = 0.9

rer = 70 * math.pow(current_weight, 0.75)
total_kcal_needed = rer * coef

kcal_per_meal = total_kcal_needed / 2
dry_grams = int(kcal_per_meal / (DEFAULT_DRY_KCAL / 100))
wet_grams = int(kcal_per_meal / (DEFAULT_WET_KCAL / 100))
water_ml = int(current_weight * 55)

# График кормления
if dog_age < 0.4 or pregnancy_status == "3":
    meals_count = 4
    schedule = "08:00 | 12:00 | 16:00 | 20:00 (дробное питание)"
elif dog_age < 1.0 or pregnancy_status == "2":
    meals_count = 3
    schedule = "08:00 | 14:00 | 20:00 (3 раза в день)"
else:
    meals_count = 2
    schedule = (
        "08:00 утром и 20:00 вечером "
        "(идеальный интервал 12 часов)"
    )


# --- 5. ВЫВОД КРАСИВОГО СУТОЧНОГО ОТЧЕТА ---
print("\n==========================================")
print(f" ВЕТЕРИНАРНЫЙ ОТЧЕТ ДЛЯ: {dog_name.upper()}")
print(f" Порода: {dog_breed} | Пол: {dog_gender}")
if is_castrated == "да":
    print(" Особый статус: СТЕРИЛИЗОВАНА/КАСТРИРОВАНА")
print(f" Статус состояния: {weight_status.upper()}")
print(f" Рекомендация: {advice}")
print("==========================================")

if has_illness == "да":
    print(" 🛑 ВНИМАНИЕ: У собаки есть хронические болезни.")
    print(" Расчет является базовым! При заболеваниях ЖКТ, почек")
    print(" или аллергиях обязательно проконсультируйтесь с")
    print(" ветеринарным врачом для подбора лечебного корма.")
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
    single_dry = int(dry_grams / (meals_count - 1))
    print(f" На заметку: делите сухой корм по {single_dry}г на первые приемы,")
    print(f" а влажный корм {wet_grams}г давайте в финальное вечернее время.")

print("==========================================")
print("💡 ДОПОЛНИТЕЛЬНЫЕ СОВЕТЫ ПО КОРМЛЕНИЮ:")
print(" 1. Не смешивайте сухой и влажный корм в один прием пищи.")

if has_illness == "да":
    print(" 2. Строго соблюдайте диету, назначенную вашим лечащим врачом.")
elif is_castrated == "да" and weight_status == "избыточный вес":
    print(
        " 2. После стерилизации метаболизм снижен. "
        "Строго взвешивайте порции на весах."
    )
elif activity_choice == "3":
    print(
        " 2. У собаки высокая активность. Увеличьте время "
        "отдыха после еды во избежание заворота кишок."
    )
elif coat_choice == "2" and season_choice == "1":
    print(
        " 2. Одевайте голую собаку на зимние прогулки, "
        "чтобы она не мерзла."
    )
elif season_choice == "2":
    print(
        " 2. В жару берите на прогулку дорожную поилку "
        "и чаще меняйте воду."
    )
else:
    print(" 2. Наливайте свежую фильтрованную воду дважды в день.")

print("==========================================\n")
