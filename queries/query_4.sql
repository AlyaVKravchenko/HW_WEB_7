--Знайти середній бал на потоці (по всій таблиці оцінок):


SELECT ROUND(AVG(grades.grade), 2) as average_grade FROM grades;