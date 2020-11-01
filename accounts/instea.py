class MessageToUser(models.Model):
    message=models.TextField()
    from_teacher=models.ForeignKey(User,related_name='teacher_msg')
    to_student=models.ForeignKey(User,related_name='student_msg')
    sent_date=models.DateTimeField(auto_now_add=True)