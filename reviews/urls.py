from django.urls import path, include
from . import views

urlpatterns = [
    path("input/", views.user_input, name='user_input'),
    path("input/k", views.user_input_kakao, name='user_input_kakao'),
    path("input/k/n", views.user_input_naver, name='user_input_naver'),
    #     path("input/pick/", views.user_pick, user-pick),
    # path("input/comprsn/", views.review_comparison, name='review-comparison'),
    #     path("input/pick/sector/", views.analysis_by_sector, analysis-by-sector),
    #     path("input/pick/comprsn/<int:comprsn_id>/",
    #          views.review_comprsn_detail, comparison-detail),
    #     path("input/pick/sector/<int:secotr_id>",
    #          views.review_sector_detail, sector-detail),
]
