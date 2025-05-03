from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Direction(models.Model):
    name = models.CharField(max_length=100)
    subject1 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject1')
    point1 = models.FloatField(default=3.1)
    count1 = models.IntegerField(default=2)
    subject2 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject2')
    point2 = models.FloatField(default=2.1)
    count2 = models.IntegerField(default=2)
    subject3 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject3')
    point3 = models.FloatField(default=1.1)
    count3 = models.IntegerField(default=2)
    maximum_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.maximum_score = round(((self.point1 * self.count1) + (self.point2 * self.count2) + (self.point3 * self.count3)), 2)
        super().save(*args, **kwargs)

class Student(BaseModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    result = models.FloatField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Question(BaseModel):
    text = models.CharField(max_length=255, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(BaseModel):
    text = models.CharField(max_length=255, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    

class StudentAnswer(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return f"{self.student} - {self.question} - {self.answer}"