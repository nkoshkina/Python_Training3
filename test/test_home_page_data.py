from model.contact import Contact
import re
import random

def test_data_on_home_page(app, db, check_ui):
    if len(db.get_contact_list()) == 0:
        app.contact.add_new(Contact(firstname="1n", middlename="2n", lastname="3n", address="Test address",
                                    home="+09875444", mobile="+79897896756", fax="+70008986756",
                                    email="t@test.com", email2="test2@t.com", email3="test@test3.com",
                                    snotes="here are notes"))
    db_contacts = db.get_contact_list()
    for element in db_contacts:
        element.all_emails_from_home_page = merge_emails_like_home_page(element)
        element.all_phones_from_home_page = merge_phones_like_home_page(element)
    contacts_from_home_page = app.contact.get_contacts_list()
    db_contacts = sorted(db_contacts, key=Contact.id_or_max)
    contacts_from_home_page = sorted(app.contact.get_contacts_list(), key=Contact.id_or_max)
    assert len(db_contacts) == len(contacts_from_home_page)
    assert db_contacts == contacts_from_home_page
    for i in range(len(db_contacts)):
        print(str(i))
        print(db_contacts[i])
        print(contacts_from_home_page[i])

    for i in range(len(db_contacts)):
        assert db_contacts[i].id == contacts_from_home_page[i].id
        assert db_contacts[i].firstname == contacts_from_home_page[i].firstname
        assert db_contacts[i].address == contacts_from_home_page[i].address
        assert db_contacts[i].all_phones_from_home_page == contacts_from_home_page[i].all_phones_from_home_page
        assert db_contacts[i].all_emails_from_home_page == contacts_from_home_page[i].all_emails_from_home_page


def clear_phones(s):
    return re.sub("[()/ -]", "", s)


def merge_phones_like_home_page(contact):
    return "\n".join(filter(lambda x: x!= "",
        map(lambda x: clear_phones(x), filter(lambda x: x is not None,
            [contact.home, contact.mobile, contact.work, contact.phone2]))))

def merge_emails_like_home_page(contact):
    return "\n".join(filter(lambda x: x!= "",
        map(lambda x: x, filter(lambda x: x is not None,
            [contact.email, contact.email2, contact.email3]))))
