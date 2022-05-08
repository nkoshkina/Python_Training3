from model.group import Group
import random


def test_modify_some_group_all_fields(app, db, check_ui, json_groups):
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name = "test group"))
    old_groups = db.get_group_list()
    group = random.choice(old_groups)
    #index = randrange(len(old_groups))
    group0 = json_groups
    group0.id = group.id
    app.group.modify_group_by_id(group.id, group0)
    #assert app.group.count() == len(old_groups)
    new_groups = db.get_group_list()
    old_groups.remove(group)
    old_groups.append(group0)
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
    if check_ui:
        print("CHECK_UI")
        assert sorted(new_groups, key=Group.id_or_max) == \
               sorted(app.group.get_groups_list(), key=Group.id_or_max)

