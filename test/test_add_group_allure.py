# -*- coding: utf-8 -*-
from model.group import Group
import pytest
import allure_pytest

def test_add_group(app, db, check_ui, json_groups):
    group0 = json_groups
    with pytest.allure.step("Given a group list"):
        old_groups = db.get_group_list()
    with pytest.allure.step("When I add a group %s to the list" % group0):
        app.group.create(group0)
    #assert app.group.count() == len(old_groups) + 1
    with pytest.allure.step("When the new groups list is equal old list with added group"):
        new_groups = db.get_group_list()
        old_groups.append(group0)
        assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
        if check_ui:
            print("CHECK_UI")
            assert sorted(new_groups, key=Group.id_or_max) == \
                sorted(app.group.get_groups_list(), key=Group.id_or_max)


