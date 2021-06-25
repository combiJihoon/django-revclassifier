from django.shortcuts import render, redirect
from .models import UserInput, CrawlResult
from .forms import UserInputForm
from .crawler import Crawler

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
    crawler = Crawler()

    context = dict()

    user_input = UserInput.objects.get(id=user_input_id)

    restaurant = user_input.restaurant
    address = user_input.address1 + ' ' + \
        user_input.address2 + ' ' + user_input.address3
    queryInput = address + ' ' + restaurant

    crawler.kakao_checker(queryInput)
    restaurant_list_kakao = crawler.restaurant_list_kakao

    # crawler.kakao_crawler(restaurant_check)

    # driver = getDriver()
    # restaurant_list, driver = kakao_checker(queryInput, driver)
    context["restaurant"] = restaurant
    context["address"] = address
    context["restaurant_list"] = restaurant_list_kakao

    # driver.quit()

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

    # TODO 크롤러 잘 작동하는지 확인하기
    crawler = Crawler()
    crawler.kakao_checker(queryInput)  # naver_list 생성
    crawler.naver_checker(queryInput)  # kakao_list 생성
    # 크롤러 작동
    jobs = []
    kakao_crawler = crawler.kakao_crawler(restaurant_check)
    naver_crawler = crawler.naver_crawler(restaurant_check)

    q = crawler.q

    crawlers = [kakao_crawler, naver_crawler]

    for crawler in crawlers:
        p = Process(target=crawler)
        jobs.append(p)
        p.start()

    for p in jobs:
        p.join()
        p.close()

    result = [q.get() for j in jobs]
    kakao_result_dict = result[0]
    naver_result_dict = result[1]

    # 카카오
    context["final_rating_kakao"] = kakao_result_dict["final_rating_kakao"]
    context["low_review_info_kakao"] = kakao_result_dict["low_review_info_kakao"]
    context["high_review_info_kakao"] = kakao_result_dict["high_review_info_kakao"]
    # 네이버
    context["final_rating_naver"] = naver_result_dict["final_rating_naver"]
    context["low_review_info_naver"] = naver_result_dict["low_review_info_naver"]
    context["high_review_info_naver"] = naver_result_dict["high_review_info_naver"]

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
