# Item 37: Compose Classes Instead of Nesting Many Levels of Built-in Types

from collections import defaultdict
class BySubjectGradebook:
    def __init__(self):
        self._grades = {} # Outer dict
    def add_student(self, name):
        self._grades[name] = defaultdict(list) # Inner dict
    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append(grade)
    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count
book = BySubjectGradebook()
book.add_student('Albert Einstein')
book.report_grade('Albert Einstein', 'Math', 75)
book.report_grade('Albert Einstein', 'Math', 65)
book.report_grade('Albert Einstein', 'Gym', 90)
book.report_grade('Albert Einstein', 'Gym', 95)
print(book.average_grade('Albert Einstein'))
# 81.25

class WeightedGradebook:
    def __init__(self):
        self._grades = {}
    def add_student(self, name):
        self._grades[name] = defaultdict(list)
    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append((score, weight))
    def average_grade(self, name):
        by_subject = self._grades[name]
        score_sum, score_count = 0, 0
        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0
            for score, weight in scores:
                subject_avg += score * weight
                total_weight += weight
            score_sum += subject_avg / total_weight
            score_count += 1
        return score_sum / score_count
book = WeightedGradebook()
book.add_student('Albert Einstein')
book.report_grade('Albert Einstein', 'Math', 75, 0.05)
book.report_grade('Albert Einstein', 'Math', 65, 0.15)
book.report_grade('Albert Einstein', 'Math', 70, 0.80)
book.report_grade('Albert Einstein', 'Gym', 100, 0.40)
book.report_grade('Albert Einstein', 'Gym', 85, 0.60)
print(book.average_grade('Albert Einstein'))
# 80.25

# Refactoring to Classes

from collections import namedtuple
Grade = namedtuple('Grade', ('score', 'weight'))

# Limitations of namedtuple
# Although namedtuple is useful in many circumstances, it’s important to understand
# when it can do more harm than good:
#  ■ You can’t specify default argument values for namedtuple
# classes. This makes them unwieldy when your data may have
# many optional properties. If you find yourself using more than
# a handful of attributes, using the built-in dataclasses module
# may be a better choice.
#  ■ The attribute values of namedtuple instances are still accessible using numerical
# indexes and iteration. Especially in externalized APIs, this can lead to unintentional usage that makes
# it harder to move to a real class later. If you’re not in control
# of all of the usage of your namedtuple instances, it’s better to
# explicitly define a new class.

class Subject:
    def __init__(self):
        self._grades = []
    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))
    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight

class Student:
    def __init__(self):
        self._subjects = defaultdict(Subject)
    def get_subject(self, name):
        return self._subjects[name]
    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count

class Gradebook:
    def __init__(self):
        self._students = defaultdict(Student)
    def get_student(self, name):
        return self._students[name]

book = Gradebook()
albert = book.get_student('Albert Einstein')
math = albert.get_subject('Math')
math.report_grade(75, 0.05)
math.report_grade(65, 0.15)
math.report_grade(70, 0.80)
gym = albert.get_subject('Gym')
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)
print(albert.average_grade())
# 80.25

# ✦ Avoid making dictionaries with values that are dictionaries, long
# tuples, or complex nestings of other built-in types.
# ✦ Use namedtuple for lightweight, immutable data containers before
# you need the flexibility of a full class.
# ✦ Move your bookkeeping code to using multiple classes when your
# internal state dictionaries get complicated.
