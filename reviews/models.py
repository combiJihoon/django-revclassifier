from django.db import models
from .validators import validate_address, validate_symbols

# Create your models here.

# 검색할 것 : 지역명, 음식점명
# * 결과로 받을 것 *
# 1) 최종 평점,
# 2) 특정 리뷰에 대한 평점, 특정 리뷰 코멘트, 특정 리뷰 날짜
# 3) 이들에 대한 최고/최저 리뷰 내역


class Review(models.Model):
    restaurant = models.CharField(max_length=20, validators=[
                                  validate_symbols])  # max_length = 20 줄이기
    address = models.CharField(max_length=20, validators=[
                               validate_address])  # '동'까지
    website = models.CharField(max_length=10)  # 네이버, 카카오, 자사
    # 리뷰 크롤링 결과 파트
    final_rating = models.FloatField()
    rating = models.FloatField()
    comment = models.CharField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return self.restaurant
