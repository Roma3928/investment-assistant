from django.db import models


class News(models.Model):
    title = models.CharField(max_length=150)
    url = models.CharField(max_length=500)
    date = models.CharField(max_length=20)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<News: {self.title}, url={self.url}>'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date']
