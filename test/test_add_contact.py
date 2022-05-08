# -*- coding: utf-8 -*-
from model.contact import Contact

def test_add_new_contact_full_data(app, db, check_ui, json_contacts):
    old_contacts = db.get_contact_list()
    contact0 = json_contacts
    app.contact.add_new(contact0)
    #assert app.contact.count() == len(old_contacts) + 1
    new_contacts = db.get_contact_list()
    old_contacts.append(contact0)
    assert sorted(new_contacts, key=Contact.id_or_max) == sorted(old_contacts, key=Contact.id_or_max)
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == \
               sorted(app.contact.get_contacts_list(), key=Contact.id_or_max)
