from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from .crawler import getDriver, kakao_checker, naver_checker
# Create your views here.


def user_input(request):
    context = dict()
    if request.method == 'POST':
        input_form = ReviewForm(request.POST)
        if input_form.is_valid():
            # 음식점 확인하는 코드 추가하기
            new_input = input_form.save()
            # getDriver()
            return redirect('user_input_kakao', review_id=new_input.id)
    else:
        input_form = ReviewForm()
        context['form'] = input_form
    return render(request, 'reviews/user_input.html', context=context)


def user_input_kakao(request, review_id):
    context = dict()

    review = Review.objects.get(id=review_id)
    context["review"] = review
    # restaurant = review.restaurant
    # address = review.address
    # queryInput = address + restaurant
    # restaurant_list, driver = kakao_checker(queryInput, driver)
    # context["restaurant_list"] = restaurant_list
    # return render(request, 'reviews/user_input_kakao.html', context=context)

    return render(request, 'reviews/user_input_kakao.html', context=context)


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
