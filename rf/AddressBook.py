import pytest
import json
import os.path
import importlib
import fixture.application

#from fixture.application import Application
#from fixture.db import DbFixture
import jsonpickle


class AddressBook:

    ROBOT_LIBRARY_SCOPE = 'TEST SUIT'

    def __init__(self, config='target.json', browser='chrome'):
        self.browser = browser
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'...', config)
        with open(config_file) as f:
            target = json.load(f)

    def init_fixtures(self):
        web_config = self.target('web')
        self.fixture = Application(browser=self.browser, base_url=web_config['baseUrl'])
        self.fixture.session.ensure_login(username=web_config['username'], password=web_config['password'])
        db_config = self.target['db']
        self.dbfixture = DbFixture(host=db_config['host'], name=db_config['name'],
                          user=db_config['user'], password=db_config['password'])

    def destroy_fixtures(self):
        self.dbfixture.destroy()
        self.fixture.destroy()

    def create_group(self):
        self.fixture.group.create(Group(name=name, header=header, footer=footer))