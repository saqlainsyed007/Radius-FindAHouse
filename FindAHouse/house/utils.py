from django.db.models.functions import (
    Radians, Power, Sin, Cos, ATan2, Sqrt, Least, Greatest, Abs, Cast,
)
from django.db.models import F, FloatField

from house.constants import (
    RelaxationType, BATH_SCORE_CONTRIBUTION, BUDGET_RELAXATION_PERCENTAGE,
    BUDGET_SCORE_CONTRIBUTION, DISTANCE_SCORE_CONTRIBUTION, MAX_SEARCH_RADIUS,
    MAX_SCORE_DISTANCE, NUM_ROOMS_RELAXATION, ROOM_SCORE_CONTRIBUTION,
)


def get_haversine_distance_annotation(current_lat, current_long):
    """
    This uses the ‘haversine’ formula to calculate the great-circle distance
    between two points – that is, the shortest distance over the earth’s
    surface – giving an ‘as-the-crow-flies’ distance between the points
    (ignoring any hills they fly over, of course!).
    Haversine formula:
    a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    c = 2 ⋅ atan2( √a, √(1−a) )
    d = R ⋅ c
    where φ is latitude, λ is longitude,
    R is earth’s radius (mean radius = 6,371km);
    note that angles need to be in radians to pass to trig functions!
    """
    R = 6371.0088
    dlat = Radians(F('latitude')) - Radians(current_lat)
    dlong = Radians(F('longitude')) - Radians(current_long)

    a = (
        Power(Sin(dlat/2), 2) + Cos(Radians(current_lat)) *
        Cos(Radians(F('latitude'))) * Power(Sin(dlong/2), 2)
    )

    c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
    d = R * c
    return d


def get_distance_score_annotation():
    unit_distance_depriciation_score = DISTANCE_SCORE_CONTRIBUTION / (
        MAX_SEARCH_RADIUS - MAX_SCORE_DISTANCE
    )

    distance_score_annotation = DISTANCE_SCORE_CONTRIBUTION - Greatest(
        (F('distance') - MAX_SCORE_DISTANCE) * unit_distance_depriciation_score,
        0
    )
    return distance_score_annotation


def get_min_max_score_annotation(
    field_name, min_value, max_value, score_contribution,
    relaxation_type=None, relaxation_value=None,
):

    spread = (max_value - min_value)
    if relaxation_type == RelaxationType.PERCENTAGE:
        spread = spread * (1 + relaxation_value / 100 * 2)
    if relaxation_type == RelaxationType.VALUE:
        spread = spread + relaxation_value * 2

    offset = Cast(
        Abs(Least(
            F(field_name) - min_value,
            max_value - F(field_name),
            0,
        )), output_field=FloatField()
    )

    score_annotation = (score_contribution * (1 - offset / spread))
    return score_annotation
