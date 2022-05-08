from model.contact import Contact
import random


def test_modify_some_contact_data(app, db, check_ui, json_contacts):
    if len(db.get_contact_list()) == 0:
        app.contact.add_new(Contact(firstname="1n", middlename="2n", lastname="3n",
                                    snotes="here are notes"))
    old_contacts = db.get_contact_list()
    contact_m = random.choice(old_contacts)
    contact0 = json_contacts
    contact0.id = contact_m.id
    app.contact.modify_contact_by_id(contact_m.id, contact0)
    new_contacts = db.get_contact_list()
    old_contacts.remove(contact_m)
    old_contacts.append(contact0)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == \
               sorted(app.contact.get_contacts_list(), key=Contact.id_or_max)

