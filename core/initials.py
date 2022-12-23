from django.contrib.auth.models import Group
from employee.models import Department, BranchLocation
from precautions.models import PrecautionType
from yayoi_recipe.models import RecipeType


def add_default_data():
    try:
        Group.objects.get_or_create(name='manager')
        Group.objects.get_or_create(name='normal')

        Department.objects.get_or_create(name='其他')
        Department.objects.get_or_create(name='內場')
        Department.objects.get_or_create(name='外場')
        Department.objects.get_or_create(name='管理')
        BranchLocation.objects.get_or_create(name='其他')
        RecipeType.objects.get_or_create(name='不分類')
        PrecautionType.objects.get_or_create(name='一般')
    except Exception:
        print("ERROR add_default_data")


def add_test_data():
    # test customer data
    pass


def init_data_to_db\
                ():
    add_default_data()
    add_test_data()
