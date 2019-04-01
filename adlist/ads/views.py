from ads.models import Ad

from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


from ads.util import AdsListView, AdsDetailView, AdsCreateView, AdsUpdateView, AdsDeleteView


class AdListView(AdsListView):
    model = Ad
    template_name = "ad_list.html"

class AdDetailView(AdsDetailView):
    model = Ad
    template_name = "ad_detail.html"

class AdCreateView(AdsCreateView):
    model = Ad
    fields = ['title', 'price', 'text']
    template_name = "ad_form.html"

class AdUpdateView(AdsUpdateView):
    model = Ad
    fields = ['title', 'price', 'text']
    template_name = "ad_form.html"

class AdDeleteView(AdsDeleteView):
    model = Ad
    template_name = "ad_delete.html"