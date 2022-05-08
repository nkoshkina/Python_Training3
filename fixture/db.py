import pymysql.cursors
from model.group import Group
from model.contact import Contact

class DbFixture:

    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host="127.0.0.1", database="addressbook",
                            user="root", password="", autocommit=True)

    def get_group_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select group_id, group_name, group_footer,"
                       "group_header from group_list")
            for row in cursor:
                (id, name, header, footer) = row
                list.append(Group(id=str(id), name=name, header=header, footer=footer))
        finally:
            cursor.close()
        return list


    def get_contacts_in_group(self, group_id):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select addressbook.id,  addressbook.firstname, addressbook.lastname \
                            from  address_in_groups \
                            INNER JOIN addressbook\
                            ON addressbook.id = address_in_groups.id \
                            where addressbook.deprecated = '0000-00-00 00:00:00' \
                            AND address_in_groups.deprecated = '0000-00-00 00:00:00'\
                            AND address_in_groups.group_id = " + str(group_id))

            for row in cursor:
                (id, firstname, lastname) = row
                list.append(Contact(id=str(id), firstname=firstname, lastname=lastname))
        finally:
            cursor.close()
        return list

    def get_contacts_not_in_group(self, group_id):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select addressbook.id,  addressbook.firstname, addressbook.lastname \
                            from  addressbook where \
                            addressbook.id not in ( \
                           select addressbook.id \
                            from  address_in_groups \
                            INNER JOIN addressbook\
                            ON addressbook.id = address_in_groups.id \
                            where addressbook.deprecated = '0000-00-00 00:00:00' \
                            AND address_in_groups.deprecated = '0000-00-00 00:00:00'\
                            AND address_in_groups.group_id = " + str(group_id) + ")")

            for row in cursor:
                (id, firstname, lastname) = row
                list.append(Contact(id=str(id), firstname=firstname, lastname=lastname))
        finally:
            cursor.close()
        return list

    def get_contact_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select id, firstname, middlename, lastname, address,\
                        email, email2, email3, \
                        mobile, work, phone2, home \
                           from addressbook where deprecated = '0000-00-00 00:00:00'" \
                           )
            for row in cursor:
                (id, firstname, middlename, lastname, address, email, email2, email3, \
                 mobile, work, phone2, home) = row
                list.append(Contact(id=str(id), firstname=firstname, middlename=middlename, lastname=lastname, \
                                    address=address, email=email, email2=email2, email3=email3, home=home, \
                                    mobile=mobile, work=work, phone2=phone2))
        finally:
            cursor.close()
        return list

    def destroy(self):
        self.connection.close()