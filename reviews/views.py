from django.shortcuts import render, redirect
from .models import UserInput, CrawlResult
from .forms import UserInputForm
from .crawler import *

import requests

from multiprocessing import Process
# Create your views here.


def index(request):
    return redirect('user-input')


def user_input(request):
    if request.method == 'POST':
        input_form = UserInputForm(request.POST)
        if input_form.is_valid():
            #     # 음식점 확인하는 코드 추가하기
            new_input = input_form.save()
            return redirect('temp-result', user_input_id=new_input.id)
    else:
        input_form = UserInputForm()
    return render(request, 'reviews/user_input.html', {'form': input_form})


def temp_result(request, user_input_id):
    context = dict()

    user_input = UserInput.objects.get(id=user_input_id)

    restaurant = user_input.restaurant
    address = user_input.address1 + ' ' + \
        user_input.address2 + ' ' + user_input.address3
    queryInput = address + ' ' + restaurant

    driver = getDriver()
    restaurant_list, driver = kakao_checker(queryInput, driver)
    context["restaurant"] = restaurant
    context["address"] = address
    context["restaurant_list"] = restaurant_list

    driver.quit()

    if request.method == 'POST':
        input_form = UserInputForm(request.POST, instance=user_input)
        if input_form.is_valid():
            input_form.save()
            return redirect('kakao-result', user_input_id=user_input.id)
    else:
        input_form = UserInputForm()

        context["form"] = input_form

    return render(request, 'reviews/temp_result.html', context=context)


def kakao_result(request, user_input_id):
    context = dict()

    user_input = UserInput.objects.get(id=user_input_id)

    # queryInput을 만들기 위한 코드
    restaurant = user_input.restaurant
    address = user_input.address1 + ' ' + \
        user_input.address2 + ' ' + user_input.address3
    queryInput = address + ' ' + restaurant
    # 'temp-list'에서 얻은 POST 결과
    restaurant_check = user_input.temp

    # 전체 크롤링 과정 다시 반복 후 restaurant_list, driver 리턴
    driver = getDriver()
    restaurant_list, driver = kakao_checker(queryInput, driver)

    # 멀티 프로세싱
    p1 = Process(target=kakao_crawler, args=(restaurant_list,
                                             restaurant_check, driver))
    p2 = Process(target=naver_crawler, args=(restaurant_list,
                                             restaurant_check, driver))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # final_rating, low_review_info, high_review_info = kakao_crawler(
    #    restaurant_list, restaurant_check, driver)

    # 카카오
    context["final_rating_kakao"] = final_rating_kakao
    context["low_review_info_kakao"] = low_review_info_kakao
    context["high_review_info_kakao"] = high_review_info_kakao
    # 네이버
    context["final_rating_naver"] = final_rating_naver
    context["low_review_info_naver"] = low_review_info_naver
    context["high_review_info_naver"] = high_review_info_naver

    return render(request, 'reviews/kakao_result.html', context=context)


# def result_kakao(request, review_id):
#     context = dict()
#     review = Info.objects.get(id=review_id)

#     queryInput = review.position1 + ' ' + review.position2 + \
#         ' ' + review.position3 + ' ' + review.name
#     restaurant_check = review.r_kakao

#     # 받은 정보를 이용해 처음부터 크롤링 스타트
#     driver = getDriver()
#     restaurant_list, driver = kakao_checker(queryInput, driver)
#     final_rating, low_review_info, high_review_info = kakao_crawler(
#         restaurant_list, restaurant_check, driver)

#     context["final_rating"] = final_rating
#     context["low_review_info"] = low_review_info
#     context["high_review_info"] = high_review_info

#     return render(request, 'reviews/result_kakao.html', context=context)

#     # def user_input_naver(request, review_id):
#     #     context = dict()

#     #     review = Review.objects.get(id=review_id)
#     #     restaurant = review.restaurant
#     #     address = review.address
#     #     queryInput = address + restaurant
#     #     restaurant_list, driver = naver_checker(queryInput, driver)
#     #     context["restaurant_list"] = restaurant_list

#     #     return render(request, 'reviews/user_input_naver.html', context=context)

#     # def review_comparison(request):
#     #     review = Review.objects.get(id=review_id)
