# -*- encoding: utf-8 -*-
from django.urls import path
from api.views import CheckServerHealth, Login, Logout, AmILogin
from api.views import GetRecipeTypes, GetRecipes, GetRecipeDoc, GetRecipeImg
from api.views import GetPrecautionTypes, GetPrecautions, GetPrecautionFile, GetPrecautionImg


urlpatterns = [
    path('CheckServerHealth', CheckServerHealth.as_view(), name='CheckServerHealth'),
    path('User/Login', Login.as_view(), name='api_login'),
    path('User/Logout', Logout.as_view(), name='api_logout'),
    path('User/AmILogin', AmILogin.as_view(), name='AmILogin'),

    path('Recipes/GetRecipeTypes', GetRecipeTypes.as_view(), name='api_GetRecipeTypes'),
    path('Recipes/GetRecipes/<str:recipe_type>', GetRecipes.as_view(), name='api_GetRecipe'),
    path('Recipes/GetRecipeDoc/<str:recipe_name>', GetRecipeDoc.as_view(), name='api_GetRecipeDoc'),
    path('Recipes/GetRecipeImg/<str:recipe_name>', GetRecipeImg.as_view(), name='api_GetRecipeImg'),

    path('Precautions/GetPrecautionTypes', GetPrecautionTypes.as_view(), name='api_GetPrecautionTypes'),
    path('Precautions/GetPrecautions/<str:precaution_type>', GetPrecautions.as_view(), name='api_GetPrecautions'),
    path('Precautions/GetPrecautionFile/<str:precaution_name>', GetPrecautionFile.as_view(), name='api_GetPrecautionFile'),
    path('Precautions/GetPrecautionImg/<str:precaution_name>', GetPrecautionImg.as_view(), name='api_GetPrecautionImg'),
]
