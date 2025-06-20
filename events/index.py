import algoliasearch_django as algoliasearch
from algoliasearch_django.decorators import register
from .models import Event

# algolia
@register(Event)
class EventIndex(algoliasearch.AlgoliaIndex):
    # 1. Specify which fields from the Event model to index directly
    fields = (
        'title',
        'description',
        'location_name',
        'price',
        'seats',

        'get_photo',
        'get_category_name',
        'get_creator_name',
        'get_date',
        'get_time',
    )


    # 3. Configure Algolia index settings
    settings = {
        'searchableAttributes': [
            'title',
            'description',
            'location_name',
            'get_category_name',
            'get_creator_username',
        ],

        'attributesForFaceting': [
            'category.name', # Use dot notation if get_category_name makes 'category' an object
            'get_category_name', # For single string facet
            'get_creator_username',
            'filterOnly(price)', # Allows filtering by price range without making it searchable by text
            'filterOnly(get_event_datetime_iso)', # For date range filtering
            'filterOnly(get_available_seats)',
        ],

        'customRanking': [
            'asc(get_event_datetime_iso)', # Rank by closest upcoming event
            'desc(get_available_seats)', # Prioritize events with more seats
            'desc(price)', # Example: higher price first
        ],
        'numericAttributesForFiltering': [
            'price',
            'seats',
            'get_available_seats',
            # Algolia can automatically infer numbers for filtering if they are numeric fields,
            # but explicitly declaring them here can be good practice.
        ],
        'replicas': [
            'Event_by_price_asc',
            'Event_by_price_desc',
            'Event_by_date_desc',
            # You define replicas for different sorting options.
            # You'll then specify the "indexName" in your React Native InstantSearch
            # to target these replicas for different sorting.
        ]
    }

    # Optional: Customize the index name (defaults to model name 'Event')
    # This will be prefixed by your ALGOLIA['INDEX_PREFIX'] from settings.py
    index_name = 'events'

