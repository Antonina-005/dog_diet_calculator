"""Модуль расчета суточной нормы сухого и влажного корма для собак."""

import math

print("=== КАЛЬКУЛЯТОР ПИТАНИЯ ДЛЯ СОБАК ===")

# --- 1. ГЛОБАЛЬНЫЕ КОНСТАНТЫ И ВЕТЕРИНАРНЫЕ ЛИМИТЫ ---
DEFAULT_DRY_KCAL = 350.0
DEFAULT_WET_KCAL = 90.0
MAX_DOG_WEIGHT = 100.0       # Максимальный разумный вес собаки (в кг)
MIN_PORTION_RATIO = 0.9      # Минимально допустимый коэффициент порции
MAX_PORTION_RATIO = 2.0      # Безопасный потолок порции для взрослых собак


# --- 2. ФУНКЦИЯ-ГЕНЕРАТОР ЗАБОТЛИВОГО UX-ВЕРДИКТА ---
def generate_human_verdict(coef, base_coef, name, factors):
    """Генерирует честный человеческий вердикт на основе расчетов."""
    # 1. Считаем абсолютную разницу со стандартной собакой (база = 1.0)
    abs_diff = int((coef - 1.0) * 100)

    # 2. Автоматически вычисляем чистую сумму всех штрафов
    total_penalties = 0.0
    for val in factors.values():
        # Базовый коэффициент не является штрафом, отсекаем его
        if val < 0 and val != base_coef:
            total_penalties += val

    penalty_percent = abs(int(total_penalties * 100))

    # 3. Формируем текст в зависимости от ситуации
    if coef in [2.0, 3.5]:
        return (
            f"💝 Сейчас у {name} особый мамин статус! Порция увеличена "
            f"максимально, чтобы малыши росли здоровыми."
        )

    verdict = (
        f"✨ Относительно базовой потребности покоя {name} нужно на "
        f"{abs_diff}% больше еды, чем 'условной идеальной' собаке. "
    )
    if penalty_percent > 0:
        verdict += (
            f"При этом из-за лишнего веса, дивана или жары мы урезали "
            f"её норму на {penalty_percent}%, но особенности породы "
            f"и организма частично компенсировали это!"
        )
    return verdict


# --- 3. ВЕТЕРИНАРНЫЕ ТАБЛИЦЫ КОНФИГУРАЦИИ ---
BASE_DIETS = {
    "сука_пожилой_да": (1.0, "Пожилой возраст + стерилизация"),
    "сука_пожилой_нет": (1.2, "Пожилой возраст (сниженный метаболизм)"),
    "кобель_пожилой_да": (1.1, "Пожилой возраст + кастрация"),
    "кобель_пожилой_нет": (1.4, "Пожилой возраст (сниженный метаболизм)"),
    "сука_взрослый_да": (1.3, "Взрослая стерилизованная собака"),
    "сука_взрослый_нет": (1.5, "Взрослая стандартная собака"),
    "кобель_взрослый_да": (1.4, "Взрослый кастрированный кобель"),
    "кобель_взрослый_нет": (1.6, "Взрослый стандартный кобель"),
}

FACTOR_MODIFIERS = {
    "activity_1": (-0.15, "Низкая активность (диванный режим)"),
    "activity_3": (0.20, "Высокая активность (тренировки)"),
    "coat_2": (0.20, "Голая порода (постоянный термообогрев)"),
    "season_2": (-0.10, "Летняя жара (снижение порции)"),
}

SPECIAL_STATUSES = {
    "2": (2.0, "🍼 Вторая половина беременности"),
    "3": (3.5, "🍼 Период лактации (выкармливание)"),
}


# --- 4. СБОР ДАННЫХ ---
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

# Проверка здоровья
while True:
    has_illness = input(
        f"\nУ {dog_name} есть хронические болезни? (да/нет): "
    ).strip().lower()
    if has_illness in ["да", "нет"]:
        break
    print("Ошибка: введите строго 'да' или 'нет'.")

# Статус стерилизации
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

# Уровень активности
print(f"\n--- Уровень активности {dog_name} ---")
print("1. Низкая (диванный режим, короткие прогулки)")
print("2. Умеренная (standard-выгул дважды в день)")
print("3. Высокая (активные игры, бег, тренировки)")
while True:
    activity_choice = input("Выберите вариант (1, 2 или 3): ").strip()
    if activity_choice in ["1", "2", "3"]:
        break
    print("Ошибка: введите цифру 1, 2 или 3.")

# Тип шерсти
print(f"\n--- Тип шерсти {dog_name} ---")
print("1. Обычная шерсть (короткая или длинная)")
print("2. Голая собака (нет шерсти, повышенный метаболизм)")
while True:
    coat_choice = input("Выберите вариант (1 или 2): ").strip()
    if coat_choice in ["1", "2"]:
        break
    print("Ошибка: введите цифру 1 или 2.")

# Время года
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

# Запрашиваем вес с валидацией границ
while True:
    try:
        current_weight = float(
            input(f"Введите ТЕКУЩИЙ вес {dog_name} (в кг): ").strip()
        )
        ideal_weight = float(
            input(f"Введите ИДЕАЛЬНЫЙ вес {dog_name} (в кг): ").strip()
        )
        if current_weight <= 0 or ideal_weight <= 0:
            print("Ошибка: вес должен быть больше нуля!")
            continue
        if current_weight > MAX_DOG_WEIGHT or ideal_weight > MAX_DOG_WEIGHT:
            print(f"Ошибка: вес превышает лимит {MAX_DOG_WEIGHT} кг. ")
            print("Пожалуйста, проверьте введённые данные.")
            continue
        break
    except ValueError:
        print("Ошибка: пожалуйста, вводите только числа через точку.")


# --- 5. ДВИЖОК АВТОМАТИЧЕСКОГО РАСЧЕТА ---
diff_percent = ((current_weight - ideal_weight) / ideal_weight) * 100

weight_warning = False
if abs(diff_percent) > 50.0:
    weight_warning = True

applied_factors = {}
age_group = "пожилой" if dog_age >= 7.0 else "взрослый"

if dog_age < 1.0:
    weight_status = "активный рост (щенок)"
    base_coef = 2.5
    applied_factors["Рост щенка (базовый коэффициент)"] = 2.5
else:
    diet_key = f"{dog_gender}_{age_group}_{is_castrated}"
    base_coef, description = BASE_DIETS[diet_key]
    applied_factors[description] = base_coef

    if pregnancy_status == "1":
        if diff_percent > 10.0:
            weight_status = "избыточный вес"
            coef_change = -0.2
            applied_factors["Избыточный вес (диета для похудения)"] = (
                coef_change
            )
        elif diff_percent < -10.0:
            weight_status = "дефицит веса"
            coef_change = 0.2
            applied_factors["Дефицит веса (диета для набора)"] = coef_change
        else:
            weight_status = "идеальный баланс"
            applied_factors["Идеальный баланс веса (норма)"] = 0.0
    else:
        weight_status = "особый репродуктивный статус"

coef = base_coef

# Корректировки только для небеременных взрослых
if pregnancy_status == "1" and dog_age >= 1.0:
    if diff_percent > 10.0:
        coef -= 0.2
    elif diff_percent < -10.0:
        coef += 0.2

    active_key = f"activity_{activity_choice}"
    coat_key = f"coat_{coat_choice}"
    season_key = f"season_{season_choice}"

    if active_key in FACTOR_MODIFIERS:
        val, desc = FACTOR_MODIFIERS[active_key]
        coef += val
        applied_factors[desc] = val

    if coat_key in FACTOR_MODIFIERS:
        val, desc = FACTOR_MODIFIERS[coat_key]
        coef += val
        applied_factors[desc] = val

    if season_choice == "1":
        winter_bonus = 0.07 if weight_status == "избыточный вес" else 0.15
        coef += winter_bonus
        applied_factors["Зимний период (надбавка на мороз)"] = winter_bonus
    elif season_key in FACTOR_MODIFIERS:
        val, desc = FACTOR_MODIFIERS[season_key]
        coef += val
        applied_factors[desc] = val

if pregnancy_status in SPECIAL_STATUSES:
    coef, description = SPECIAL_STATUSES[pregnancy_status]
    applied_factors = {description: coef}

limit_max = (
    3.5 if (dog_age < 1.0 or pregnancy_status == "3")
    else MAX_PORTION_RATIO
)

if coef < MIN_PORTION_RATIO:
    applied_factors["🔒 Ограничение: ветеринарный минимум"] = (
        MIN_PORTION_RATIO - coef
    )
elif coef > limit_max:
    applied_factors["🔒 Ограничение: безопасный потолок"] = (
        limit_max - coef
    )

coef = max(MIN_PORTION_RATIO, coef)
coef = min(limit_max, coef)

# Вызываем функцию-генератор заботливого вердикта
human_verdict = generate_human_verdict(
    coef, base_coef, dog_name, applied_factors
)


# --- 6. РАСЧЕТ СУТОЧНОЙ ПОРЦИИ, ВОДЫ И ГРАФИКА ---
rer = 70 * math.pow(current_weight, 0.75)
total_kcal_needed = rer * coef

kcal_per_meal = total_kcal_needed / 2
dry_grams = int(kcal_per_meal / (DEFAULT_DRY_KCAL / 100))
wet_grams = int(kcal_per_meal / (DEFAULT_WET_KCAL / 100))
water_ml = int(current_weight * 55)

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
# --- 7. ВЫВОД СУТОЧНОГО ОТЧЕТА ---
print("\n==========================================")
print(f" ВЕТЕРИНАРНЫЙ ОТЧЕТ ДЛЯ: {dog_name.upper()}")
print(f" Порода: {dog_breed} | Пол: {dog_gender}")
if is_castrated == "да":
    print(" Особый статус: СТЕРИЛИЗОВАНА/КАСТРИРОВАНА")
print(f" Статус состояния: {weight_status.upper()}")
print(f" Итоговый коэффициент метаболизма (MER): {round(coef, 2)}")
print("==========================================")
print("💬 ЗАБОТЛИВЫЙ ВЕРДИКТ КАЛЬКУЛЯТОРА:")
print(human_verdict)
print("==========================================")
print("🔍 ПОЧЕМУ НАЗНАЧЕНА ИМЕННО ТАКАЯ ПОРЦИЯ:")

for factor_name, factor_value in applied_factors.items():
    if factor_value == 0.0:
        print(f" • {factor_name}")
    elif factor_value > 0 and not factor_name.startswith("🔒"):
        if (
            "базовый" in factor_name
            or "собака" in factor_name
            or "кобель" in factor_name
        ):
            print(f" • {factor_name}: {factor_value}")
        else:
            print(f" • {factor_name}: +{factor_value}")
    else:
        print(f" • {factor_name}: {round(factor_value, 2)}")

print("==========================================")

if weight_warning:
    print(" ⚠️ ВНИМАНИЕ: Разница между текущим и идеальным")
    print(f" весом составляет {abs(int(diff_percent))}%! Пожалуйста, ")
    print(" убедитесь, что вы правильно указали идеальный вес.")
    print("==========================================")

if has_illness == "да":
    print(" 🛑 ВНИМАНИЕ: У собаки есть хронические болезни.")
    print(" Расчет является базовым! При заболеваниях ЖКТ, почек")
    print(" или аллергиях обязательно проконсультируйтесь с")
    print(" ветеринарным врачом для подбора лечебного корма.")
    print("==========================================")

print("📋 РЕКОМЕНДУЕМЫЙ СУТОЧНЫЙ РАЦИОН:")
print(f" ☀️ УТРО (Сухой корм): {dry_grams} gramm всего")
print(f" 🌙 ВЕЧЕР (Влажный корм): {wet_grams} gramm всего")
print(f" 💧 МИНИМУМ ВОДЫ В СУТКИ: {water_ml} ml")
print("==========================================")
print("⏱️ РЕЖИМ И ГРАФИК КОРМЛЕНИЯ:")
print(f" Количество кормлений в сутки: {meals_count}")
print(f" Рекомендуемые часы: {schedule}")

if meals_count > 2:
    single_dry = int(dry_grams / (meals_count - 1))
    print(
        f" На заметку: делите сухой корм по {single_dry}г на первые приемы,"
    )
    print(
        f" а влажный корм {wet_grams}г давайте в финальное вечернее время."
    )

# --- ДИНАМИЧЕСКИЙ ФИЛЬТР СОВЕТОВ ПО КОРМЛЕНИЮ ---
applied_tips = ["Не смешивайте сухой и влажный корм в один прием пищи."]

if has_illness == "да":
    applied_tips.append(
        "Строго соблюдайте лечебную диету, назначенную ветеринаром."
    )
else:
    if is_castrated == "да" and weight_status == "избыточный вес":
        applied_tips.append(
            "После стерилизации метаболизм снижен. "
            "Строго взвешивайте порции на весах."
        )
    if activity_choice == "3":
        applied_tips.append(
            "У собаки высокая активность. Увеличьте время "
            "отдыха после еды во избежание заворота кишок."
        )
    if coat_choice == "2" and season_choice == "1":
        applied_tips.append(
            "Одевайте голую собаку на зимние прогулки, чтобы она не мерзла."
        )
    if season_choice == "2":
        applied_tips.append(
            "В жару берите на прогулку дорожную поилку и чаще меняйте воду."
        )
    if len(applied_tips) == 1:
        applied_tips.append(
            "Наливайте свежую фильтрованную "
            "воду дважды в день."
        )

print("==========================================")
print("💡 ПЕРСОНАЛЬНЫЕ СОВЕТЫ ПО КОРМЛЕНИЮ:")
for i, tip in enumerate(applied_tips, 1):
    print(f" {i}. {tip}")
print("==========================================\n")
