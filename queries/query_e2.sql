
SELECT
    subjects.name AS subject_name,
    groups.name AS group_name,
    students.fullname AS student_name,
    grades.grade AS student_grade
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
JOIN groups ON students.group_id = groups.id
WHERE (subjects.id, grades.grade_date) IN (
    SELECT
        subjects.id AS subject_id,
        MAX(grades.grade_date) AS max_grade_date
    FROM students
    JOIN grades ON students.id = grades.student_id
    JOIN subjects ON grades.subject_id = subjects.id
    GROUP BY subjects.id
)
ORDER BY subject_name, group_name, student_name;