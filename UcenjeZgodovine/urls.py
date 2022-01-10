"""UcenjeZgodovine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from Users import views as user_views
from django.conf.urls.static import static

urlpatterns = [
                  path('', lambda request: redirect('prva_stran/')),
                  path('vprasanja/<int:level>', user_views.get_questions_and_answers),
                  path('knjiznjica/', user_views.get_libraby),
                  path('prva_stran/', user_views.prva_stran),
                  path('druga_stran/', user_views.druga_stran),
                  path('tretja_stran/', user_views.tretja_stran),
                  path('admin/', admin.site.urls),
                  path('prijava/', user_views.prijava),
                  path('registracija/', user_views.registracija),
                  path('odjava/', user_views.odjava),
                  path('dodaj_vprasanje/', user_views.create_new_question),
                  path('vprasanja_ucencov/<str:theme>/', user_views.students_questions)

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
