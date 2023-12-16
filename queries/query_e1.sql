

SELECT
       students.fullname AS student_name,

       teachers.fullname AS teacher_name,
       ROUND(AVG(grades.grade), 2) AS average_grade
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
JOIN teachers ON subjects.teacher_id = teachers.id

GROUP BY students.fullname, teachers.fullname;