from django.shortcuts import render, redirect
from .models import UserInput, CrawlResult
from .forms import UserInputForm
from .crawler import Crawler, MultiProcessing

import requests

from multiprocessing import Process
# Create your views here.

# TODO view를 클래스로 바꾸어서 인자들이 재사용 가능하도록 바꿀 것


def index(request):
    return redirect('user-input')


def user_input(request):
    if request.method == 'POST':
        input_form = UserInputForm(request.POST)
        if input_form.is_valid():
            # 음식점 확인하는 코드 추가하기
            new_input = input_form.save()
            return redirect('temp-result', user_input_id=new_input.id)
    else:
        input_form = UserInputForm()
    return render(request, 'reviews/user_input.html', {'form': input_form})


def temp_result(request, user_input_id):
    context = dict()

    # 모델 정보 가져오기
    user_input = UserInput.objects.get(id=user_input_id)

    # 검색 정보
    restaurant = user_input.restaurant
    address = user_input.address1 + ' ' + \
        user_input.address2 + ' ' + user_input.address3
    queryInput = address + ' ' + restaurant

    # 크롤러 실행 : 맛집 리스트 가져오기
    crawler = Crawler()
    crawler.kakao_checker(queryInput)

    # 중간 결과
    context["restaurant"] = restaurant
    context["address"] = address
    context["restaurant_list"] = crawler.restaurant_list_kakao

    crawler.driver_kakao.quit()

    if request.method == 'POST':
        # form 수정 메소드와 동일
        input_form = UserInputForm(request.POST, instance=user_input)
        if input_form.is_valid():
            input_form.save()

            return redirect('kakao-result', user_input_id=user_input.id)

    else:
        input_form = UserInputForm()

        context["form"] = input_form

    return render(request, 'reviews/temp_result.html', context=context)


def result(request, user_input_id):
    context = dict()
    user_input = UserInput.objects.get(id=user_input_id)

    # queryInput을 만들기 위한 코드
    restaurant = user_input.restaurant
    address = user_input.address1 + ' ' + \
        user_input.address2 + ' ' + user_input.address3
    queryInput = address + ' ' + restaurant

    # 'temp-list'에서 얻은 POST 결과
    restaurant_check = user_input.temp

    crawler = Crawler()
    crawler.kakao_checker(queryInput)  # naver_list 생성
    crawler.naver_checker(queryInput)  # kakao_list 생성

    # Multiprocessing 시작
    jobs = []

    q = crawler.q

    crawlers = [
        crawler.kakao_crawler(
            restaurant_check), crawler.naver_crawler(restaurant_check)
    ]

    for crawler in crawlers:
        p = Process(target=crawler)
        jobs.append(p)
        p.start()

    for p in jobs:
        p.join()
        p.close()

    result = [q.get() for j in jobs]

    # mp = MultiProcessing()
    # result = mp.multiCrawler(crawler.kakao_crawler(user_input.temp),
    #                          crawler.naver_crawler(user_input.temp))
    # kakao_result_dict = result[0]
    # naver_result_dict = result[1]

    print(result)

    # 카카오
    context["final_rating_kakao"] = result[0]["final_rating_kakao"]
    context["low_review_info_kakao"] = result[0]["low_review_info_kakao"]
    context["high_review_info_kakao"] = result[0]["high_review_info_kakao"]
    # 네이버
    context["final_rating_naver"] = result[1]["final_rating_naver"]
    context["low_review_info_naver"] = result[1]["low_review_info_naver"]
    context["high_review_info_naver"] = result[1]["high_review_info_naver"]

    return render(request, 'reviews/kakao_result.html', context=context)


#####################################
