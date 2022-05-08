from model.contact import Contact
import random


def test_delete_some_contact(app, db, check_ui):
    if len(db.get_contact_list()) == 0:
        app.contact.add_new(Contact("1n", "2n", "3n", "", "Title", "Comp", "address",
                                    "", "", "+7900", "+723456789",
                                    "test@test.com", "t@t2.com", "t@t3.com", "localhost",
                                    "3", "May", "1998", "13", "April", "2020",
                                    "sec address", "//test", "here are notes"))
    old_contacts = db.get_contact_list()
    contact_del = random.choice(old_contacts)
    app.contact.delete_contact_by_id(contact_del.id)
    #assert app.contact.count() == len(old_contacts) - 1
    old_contacts.remove(contact_del)
    new_contacts = db.get_contact_list()
    assert new_contacts == old_contacts
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == \
               sorted(app.contact.get_contacts_list(), key=Contact.id_or_max)
