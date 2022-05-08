# -*- coding: utf-8 -*-
from model.group import Group
import random

def test_delete_some_group(app, db, check_ui):
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="test group"))
    old_groups = db.get_group_list()
    group = random.choice(old_groups)
    app.group.delete_group_by_id(group.id)
    #assert app.group.count() == len(old_groups) - 1
    new_groups = db.get_group_list()
    old_groups.remove(group)
    assert new_groups == old_groups
    if check_ui:
        print("CHECK_UI")
        assert sorted(new_groups, key=Group.id_or_max) == \
               sorted(app.group.get_groups_list(), key=Group.id_or_max)




