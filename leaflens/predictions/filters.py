import django_filters
from .models import Prediction

class PredictionFilter(django_filters.FilterSet):

    # date range filtering (?created_at_after=YYYY-MM-DD&created_at_before=YYYY-MM-DD)
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Prediction
        fields = {
            'id': ['exact'],
            'predicted_disease': ['exact'],  # FK ID filtering ex: ?predicted_disease__name__icontains=rust
            'predicted_disease__name': ['icontains'],  # human-friendly search
        }