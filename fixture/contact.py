from selenium.webdriver.support.ui import Select
from model.contact import Contact


class ContactHelper:
    def __init__(self, app):
        self.app = app

    def add_new(self, contact):
        wd = self.app.wd
        # Add new contact
        wd.find_element_by_link_text("add new").click()
        self.fill_all_fields(contact)
        wd.find_element_by_xpath("//div[@id='content']/form/input[21]").click()
        self.contact_cache = None

    def fill_all_fields(self, contact):
        wd = self.app.wd
        self.fill_text_field("firstname", contact.firstname)
        self.fill_text_field("middlename", contact.middlename)
        self.fill_text_field("lastname", contact.lastname)
        self.fill_text_field("nickname", contact.nickname)
        self.fill_text_field("title", contact.title)
        self.fill_text_field("company", contact.company)
        self.fill_text_field("address", contact.address)
        self.fill_text_field("home", contact.home)
        self.fill_text_field("mobile", contact.mobile)
        self.fill_text_field("work", contact.work)
        self.fill_text_field("fax", contact.fax)
        self.fill_text_field("email", contact.email)
        self.fill_text_field("email2", contact.email2)
        self.fill_text_field("email3", contact.email3)
        self.fill_text_field("homepage", contact.homepage)
        self.selected_field("bday", contact.dbirthday)
        self.selected_field("bmonth", contact.mbirthday)
        self.fill_text_field("byear", contact.ybirthday)
        self.selected_field("aday", contact.danniversary)
        self.selected_field("amonth", contact.manniversary)
        self.fill_text_field("ayear", contact.yanniversary)
        self.fill_text_field("address2", contact.saddress)
        self.fill_text_field("phone2", contact.phone2)
        self.fill_text_field("notes", contact.snotes)

    def fill_text_field(self, field, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field).click()
            wd.find_element_by_name(field).clear()
            wd.find_element_by_name(field).send_keys(text)

    def selected_field(self, field, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field).click()
            Select(wd.find_element_by_name(field)).select_by_visible_text(text)

    def modify_first_contact(self, contact):
        self.modify_contact_by_index(0, contact)

    def modify_contact_by_index(self, index, contact):
        wd = self.app.wd
        self.click_home_link()
        wd.find_elements_by_xpath("//img[@title='Edit']")[index].click()
        # Fill fields
        self.fill_all_fields(contact)
        wd.find_element_by_name("update").click()
        self.contact_cache = None

    def modify_contact_by_id(self, id, contact):
        wd = self.app.wd
        self.click_home_link()
        #element = wd.find_element_by_css_selector("input[value='%s']" % id)
        #element.find_element_by_xpath("//../../img[@title='Edit']").click()
        wd.find_element_by_xpath('//a[@href="edit.php?id=%s"]/img' % id).click()
        # Fill fields
        self.fill_all_fields(contact)
        wd.find_element_by_name("update").click()
        self.contact_cache = None

    def delete_first_contact(self):
        self.delete_contact_by_index(0)

    def delete_contact_by_index(self, index):
        wd = self.app.wd
        self.click_home_link()
        self.select_contact_by_index(index)
        self.click_delete_button()
        self.alert_accept()
        self.contact_cache = None

    def delete_contact_by_id(self, id):
        wd = self.app.wd
        self.click_home_link()
        self.select_contact_by_id(id)
        self.click_delete_button()
        self.alert_accept()
        wd.find_element_by_css_selector("div.msgbox")
        self.contact_cache = None

    def add_contact_to_group_by_id(self, cid, gid):
        wd = self.app.wd
        self.click_home_link()
        self.select_contact_by_id(cid)
        wd.find_element_by_xpath("//select[@name='to_group']/option[@value='" + str(gid)+"']").click()
        wd.find_element_by_css_selector("input[value='Add to']").click()

    def delete_contact_from_group_by_id(self, cid, gid):
        wd = self.app.wd
        self.click_home_link()
        wd.find_element_by_xpath("//select[@name='group']/option[@value='" + str(gid)+"']").click()
        self.select_contact_by_id(cid)
        wd.find_element_by_name("remove").click()

    def select_group_by_name(self, grName):
        wd = self.app.wd
        self.selected_field("group", grName)

    def select_contact_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_name("selected[]")[index].click()

    def select_contact_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_css_selector("input[value='%s']" % id).click()

    def alert_accept(self):
        wd = self.app.wd
        # Confirm deleting
        wd.switch_to.alert.accept()

    def click_delete_button(self):
        wd = self.app.wd
        # Click Delete button
        wd.find_element_by_xpath("//input[@value='Delete']").click()

    def click_home_link(self):
        wd = self.app.wd
        if wd.current_url.endswith("/addressbook") and len(wd.find_elements_by_xpath("//[@value='Send e-Mail']")) > 0:
            return
        wd.find_element_by_link_text("home").click()

    def count(self):
        wd = self.app.wd
        self.click_home_link()
        return len(wd.find_elements_by_name("selected[]"))

    contact_cache = None

    def get_contacts_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.click_home_link()
            self.contact_cache = []
            for element in wd.find_elements_by_xpath("//tbody/tr[@name='entry']"):
                id = element.find_element_by_name("selected[]").get_attribute("value")
                lastname = element.find_element_by_xpath("td[2]").text
                firstname = element.find_element_by_xpath("td[3]").text
                address = element.find_element_by_xpath("td[4]").text
                all_phones = element.find_element_by_xpath("td[6]").text
                all_emails = element.find_element_by_xpath("td[5]").text
                self.contact_cache.append(Contact(firstname=firstname, lastname=lastname, id=id,
                                                  address=address,
                                                  all_phones_from_home_page=all_phones,
                                                  all_emails_from_home_page=all_emails))
        return list(self.contact_cache)


    def open_contact_to_edit_by_index(self, index):
        wd = self.app.wd
        self.click_home_link()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[7]
        cell.find_element_by_tag_name("a").click()

    def open_contact_view_by_index(self, index):
        wd = self.app.wd
        self.click_home_link()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[6]
        cell.find_element_by_tag_name("a").click()

    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.open_contact_to_edit_by_index(index)
        id = wd.find_element_by_name("id").get_attribute("value")
        firstname = wd.find_element_by_name("firstname").get_attribute("value")
        lastname = wd.find_element_by_name("lastname").get_attribute("value")
        address = wd.find_element_by_name("address").get_attribute("value")
        home = wd.find_element_by_name("home").get_attribute("value")
        work = wd.find_element_by_name("work").get_attribute("value")
        mobile = wd.find_element_by_name("mobile").get_attribute("value")
        phone2 = wd.find_element_by_name("phone2").get_attribute("value")
        email = wd.find_element_by_name("email").get_attribute("value")
        email2 = wd.find_element_by_name("email2").get_attribute("value")
        email3 = wd.find_element_by_name("email3").get_attribute("value")
        return Contact(firstname = firstname, lastname = lastname, address=address,
                id = id, home = home, mobile = mobile,
                work = work, phone2=phone2,
                email=email, email2=email2, email3=email3)


