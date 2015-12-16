from haystack import indexes
from main.models import Episode

class EpisodeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Episode

    def index_queryset(self, using=None):
        return self.get_model().objects.all().order_by('-created_date')
