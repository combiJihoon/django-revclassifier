from django.db import models
from .validators import validate_address1, validate_address2, validate_address3, validate_symbols
# Create your models here.

# 검색할 것 : 지역명, 음식점명
# * 결과로 받을 것 *
# 1) 최종 평점,
# 2) 특정 리뷰에 대한 평점, 특정 리뷰 코멘트, 특정 리뷰 날짜
# 3) 이들에 대한 최고/최저 리뷰 내역


class UserInput(models.Model):
    restaurant = models.CharField(
        max_length=20, default='', blank=True)  # max_length = 20 줄이기
    address1 = models.CharField(
        max_length=10, default='', validators=[validate_address1], blank=True)  # '동'까지
    address2 = models.CharField(max_length=10, default='', validators=[
                                validate_address2], blank=True)  # '동'까지
    address3 = models.CharField(max_length=10, default='', validators=[
                                validate_address3], blank=True)  # '동'까지
    temp = models.CharField(
        max_length=20, default='', validators=[validate_symbols], blank=True)

    # 리뷰 크롤링 결과 파트

    def __str__(self):
        return self.restaurant


class CrawlResult(models.Model):
    user_input_id = models.ForeignKey(UserInput, on_delete=models.CASCADE)
    final_rating = models.FloatField(null=True)
    rating = models.FloatField(null=True)
    comment = models.CharField(max_length=500, default='')
    date = models.DateField(null=True)
