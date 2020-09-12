from django.db.models import F, Max, Min

from rest_framework.utils.urls import replace_query_param
from rest_framework.views import APIView
from rest_framework.response import Response

from house.constants import (
    BUDGET_RELAXATION_PERCENTAGE, BUDGET_SCORE_CONTRIBUTION,
    MAX_SEARCH_RADIUS, MINIMUM_SCORE_FOR_MATCH, NUM_ROOMS_RELAXATION,
    RelaxationType, ROOM_SCORE_CONTRIBUTION,
)
from house.models import House
from house.utils import (
    get_distance_score_annotation,
    get_haversine_distance_annotation,
    get_min_max_score_annotation,
)
from house.serializers import HouseSearchParamSerializer


class HouseSearchView(APIView):

    page_size = 10

    def _get_pagination_info(self, request, count, page_number):
        absolute_uri = request.build_absolute_uri()
        previous_url = None
        if page_number > 1:
            previous_url = replace_query_param(
                absolute_uri, 'page_number', page_number - 1
            )
        next_url = None
        if count > page_number * self.page_size:
            next_url = replace_query_param(
                absolute_uri, 'page_number', page_number + 1
            )
        return {
            "previous": previous_url,
            "next": next_url,
            "count": count
        }

    def get(self, request):
        param_serializer = HouseSearchParamSerializer(
            data=request.GET.dict()
        )
        if not param_serializer.is_valid():
            return Response(param_serializer.errors)

        page_number = param_serializer.data.get("page_number")
        latitude = param_serializer.data.get("latitude")
        longitude = param_serializer.data.get("longitude")
        min_budget = param_serializer.data.get("min_budget")
        max_budget = param_serializer.data.get("max_budget")
        min_bedrooms = param_serializer.data.get("min_bedrooms")
        max_bedrooms = param_serializer.data.get("max_bedrooms")
        min_bathrooms = param_serializer.data.get("min_bathrooms")
        max_bathrooms = param_serializer.data.get("max_bathrooms")

        min_max_values = House.objects.aggregate(
            Max('bedrooms'), Min('bedrooms'),
            Max('bathrooms'), Min('bathrooms')
        )

        # If min budget is not specified, min budget is assumed to be
        # max budget - 10%
        min_budget = min_budget or max_budget * 0.9
        # If max budget is not specified, max budget is assumed to be
        # min budget + 10%
        max_budget = max_budget or min_budget * 1.1

        # If min bedrooms is not specified, min bathrooms is assumed to be 1
        min_bedrooms = min_bedrooms or 1
        # If max bedrooms is not specified, max bedrooms is assumed to be
        # max available bedrooms
        max_bedrooms = max_bedrooms or min_max_values['bedrooms__max']

        # If min bathrooms is not specified, min bathrooms is assumed to be 1
        min_bathrooms = min_bathrooms or 1
        # If max bathrooms is not specified, max bathrooms is assumed to be
        # max available bathrooms
        max_bathrooms = max_bathrooms or min_max_values['bathrooms__max']

        distance_annotation = get_haversine_distance_annotation(
            latitude, longitude
        )
        distance_score_annotation = get_distance_score_annotation()
        budget_score_annotation = get_min_max_score_annotation(
            'price', min_budget, max_budget, BUDGET_SCORE_CONTRIBUTION,
            RelaxationType.PERCENTAGE, BUDGET_RELAXATION_PERCENTAGE,
        )
        room_score_annotation = get_min_max_score_annotation(
            'bedrooms', min_bedrooms, max_bedrooms, ROOM_SCORE_CONTRIBUTION,
            RelaxationType.VALUE, NUM_ROOMS_RELAXATION,
        )
        bath_score_annotation = get_min_max_score_annotation(
            'bathrooms', min_bathrooms, max_bathrooms, ROOM_SCORE_CONTRIBUTION,
            RelaxationType.VALUE, NUM_ROOMS_RELAXATION,
        )
        houses = House.objects.filter(
            price__gte=min_budget,
            price__lte=max_budget,
            bathrooms__gte=min_bathrooms - NUM_ROOMS_RELAXATION,
            bathrooms__lte=max_bathrooms + NUM_ROOMS_RELAXATION,
            bedrooms__gte=min_bedrooms - NUM_ROOMS_RELAXATION,
            bedrooms__lte=max_bedrooms + NUM_ROOMS_RELAXATION,
        ).annotate(
            distance=distance_annotation,
            distance_score=distance_score_annotation,
            budget_score=budget_score_annotation,
            rooms_score=room_score_annotation,
            baths_score=bath_score_annotation,
            final_score=(
                F('distance_score') + F('budget_score') +
                F('rooms_score') + F('baths_score')
            )
        ).filter(
            final_score__gte=MINIMUM_SCORE_FOR_MATCH,
            distance__lte=MAX_SEARCH_RADIUS,
        ).order_by('-final_score')

        pagination_start_index = (page_number - 1) * self.page_size
        pagination_end_index = (page_number) * self.page_size
        pagination_info = self._get_pagination_info(
            request, houses.count(), page_number
        )

        return Response({
            **pagination_info,
            "data": houses[pagination_start_index:pagination_end_index].values(
                "name", "price", "bedrooms", "bathrooms", "distance",
                "distance_score", "budget_score", "rooms_score",
                "baths_score", "final_score",
            ),
        })
