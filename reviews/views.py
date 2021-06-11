from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from .crawler import getDriver, kakao_checker, naver_checker, kakao_crawler

import requests
import time
import json
# Create your views here.


def user_input(request):
    if request.method == 'POST':
        input_form = ReviewForm(request.POST)
        if input_form.is_valid():
            # 음식점 확인하는 코드 추가하기
            new_input = input_form.save()

            return redirect('user_input_kakao', review_id=new_input.id)
    else:
        input_form = ReviewForm()
    return render(request, 'reviews/user_input.html', {'form': input_form})


# def user_input_kakao(request, review_id):
#     context = dict()

#     review = Review.objects.get(id=review_id)
#     restaurant = review.restaurant
#     address = review.address1 + ' ' + review.address2 + ' ' + review.address3
#     queryInput = address + ' ' + restaurant

#     driver = getDriver()
#     restaurant_list, driver = kakao_checker(queryInput, driver)
#     context["restaurant"] = restaurant
#     context["address"] = address
#     context["restaurant_list"] = restaurant_list

#     return render(request, 'reviews/user_input_kakao.html', context=context)

global_context = dict()


def user_input_kakao(request, review_id):
    global global_context
    context = dict()

    review = Review.objects.get(id=review_id)
    restaurant = review.restaurant
    address = review.address1 + ' ' + review.address2 + ' ' + review.address3
    queryInput = address + ' ' + restaurant

    driver = getDriver()
    restaurant_list, driver = kakao_checker(queryInput, driver)

    context["restaurant"] = restaurant
    context["address"] = address
    context["restaurant_list"] = restaurant_list

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            # 크롤러 작동
            time.sleep(3)
            return redirect('result_kakao', review_id=review.id)
    else:
        review_form = ReviewForm(instance=review)

        context["form"] = review_form

    return render(request, 'reviews/user_input_kakao.html', context=context)


def result_kakao(request, review_id):
    context = dict()
    review = Review.objects.get(id=review_id)

    queryInput = review.address1 + ' ' + review.address2 + \
        ' ' + review.address3 + ' ' + review.restaurant
    restaurant_check = review.r_kakao

    # 받은 정보를 이용해 처음부터 크롤링 스타트
    driver = getDriver()
    restaurant_list, driver = kakao_checker(queryInput, driver)
    final_rating, low_review_info, high_review_info = kakao_crawler(
        restaurant_list, restaurant_check, driver)

    context["final_rating"] = final_rating
    context["low_review_info"] = low_review_info
    context["high_review_info"] = high_review_info

    return render(request, 'reviews/result_kakao.html', context=context)

    # def user_input_naver(request, review_id):
    #     context = dict()

    #     review = Review.objects.get(id=review_id)
    #     restaurant = review.restaurant
    #     address = review.address
    #     queryInput = address + restaurant
    #     restaurant_list, driver = naver_checker(queryInput, driver)
    #     context["restaurant_list"] = restaurant_list

    #     return render(request, 'reviews/user_input_naver.html', context=context)

    # def review_comparison(request):
    #     review = Review.objects.get(id=review_id)
