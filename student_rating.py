# Решение задачи "Рейтинг ученика"
# Считываем входные данные
line1 = input().split()
N, M, Q, cw, sw, hw, tw = map(int, line1)

# Проверка корректности входных данных
if N < 3 or M <= 0 or cw <= 0 or sw <= 0 or hw <= 0 or tw <= 0:
    print("Во введённых данных ошибка")
else:
    # Проверка, что максимальный рейтинг не превышает Q
    max_possible_rating = M * (cw + sw + hw + tw)
    if max_possible_rating > Q:
        print("Во введённых данных ошибка")
    else:
        # Список для хранения данных учеников
        students = []
        
        # Считываем данные для каждого ученика
        for _ in range(N):
            # Считываем фамилию ученика
            surname = input()
            
            # Инициализируем суммы оценок
            sum_cw = 0
            sum_sw = 0
            sum_hw = 0
            sum_tw = 0
            
            # Считываем оценки за M занятий
            for _ in range(M):
                grades = input().split(',')
                a, b, c, d = map(int, grades)
                sum_cw += a
                sum_sw += b
                sum_hw += c
                sum_tw += d
            
            # Рассчитываем текущий рейтинг
            current_rating = sum_cw * cw + sum_sw * sw + sum_hw * hw + sum_tw * tw
            
            # Рассчитываем процент от максимального рейтинга
            percentage = round((current_rating / Q) * 100)
            
            # Добавляем данные ученика в список
            students.append((surname, percentage, current_rating))
        
        # Определяем максимальное, среднее и минимальное значения рейтинга
        ratings = [student[2] for student in students]
        max_rating = max(ratings)
        min_rating = min(ratings)
        avg_rating = sum(ratings) / len(ratings)
        
        # Преобразуем в проценты
        max_percentage = round((max_rating / Q) * 100)
        min_percentage = round((min_rating / Q) * 100)
        avg_percentage = round((avg_rating / Q) * 100)
        
        # Выводим максимальное, среднее и минимальное значения
        print(f"{max_percentage} {avg_percentage} {min_percentage}")
        
        # Сортируем учеников по рейтингу (по убыванию), при равенстве сохраняем порядок ввода
        # Для этого добавим индекс при сортировке
        students_with_index = [(students[i][0], students[i][1], students[i][2], i) for i in range(len(students))]
        sorted_students = sorted(students_with_index, key=lambda x: (-x[2], x[3]))
        
        # Выводим топ-3 учеников
        for i in range(min(3, len(sorted_students))):
            print(f"{sorted_students[i][0]} {sorted_students[i][1]}%")
        
        # Определяем, как усваивается курс
        if avg_percentage <= 50:
            print("Курс усваивается плохо")
        else:
            print("Курс усваивается хорошо")