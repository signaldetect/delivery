from django.db import models

class Page(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.name

class PublTextModel(models.Model):
    '''
    Published text and its publication date
    '''
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Publication date')
    #description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.frag_of_text()

    def frag_of_text(self):
        if len(self.text) > 100:
            frag = self.text.split('. ', 1)[0]
            if len(frag) > 100:
                return '{0}...'.format(frag[:100])
            return '{0}.'.format(frag)
        # Otherwise
        return self.text

    frag_of_text.admin_order_field = 'text'
    frag_of_text.short_description = 'Text'

    class Meta:
        abstract = True
        ordering = ['-created_at']

class News(PublTextModel):
    class Meta(PublTextModel.Meta):
        verbose_name_plural = 'news'

class SpecOffer(PublTextModel):
    finished = models.BooleanField(default=False)

    class Meta(PublTextModel.Meta):
        verbose_name = 'special offer'
