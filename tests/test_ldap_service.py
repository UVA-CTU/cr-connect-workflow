from unittest.mock import patch

from ldap3.core.exceptions import LDAPSocketOpenError
from tests.base_test import BaseTest

from crc import app
from crc.api.common import ApiError
from crc.services.ldap_service import LdapService


class TestLdapService(BaseTest):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_single_user(self):
        user_info = LdapService().user_info("lb3dp")
        self.assertIsNotNone(user_info)
        self.assertEqual("lb3dp", user_info.uid)
        self.assertEqual("Laura Barnes", user_info.display_name)
        self.assertEqual("Laura", user_info.given_name)
        self.assertEqual("lb3dp@virginia.edu", user_info.email_address)
        self.assertEqual("+1 (434) 924-1723", user_info.telephone_number)
        self.assertEqual("E0:Associate Professor of Systems and Information Engineering", user_info.title)
        self.assertEqual("E0:EN-Eng Sys and Environment", user_info.department)
        self.assertEqual("faculty", user_info.affiliation)
        self.assertEqual("Staff", user_info.sponsor_type)

    def test_find_missing_user(self):
        try:
            user_info = LdapService().user_info("nosuch")
            self.assertFalse(True, "An API error should be raised.")
        except ApiError as ae:
            self.assertEqual("missing_ldap_record", ae.code)

    def test_get_user_with_caps(self):
        user_info = LdapService().user_info("LB3DP")
        self.assertIsNotNone(user_info)
        self.assertEqual("lb3dp", user_info.uid)

    def test_get_user_with_spaces(self):
        user_info = LdapService().user_info("    LB3DP ")
        # Call this a second time, becuase the error we ran into wasn't that it wasn't possible to find it,
        # but that it attepts to add it to the database a second time with the same id.
        user_info = LdapService().user_info("    LB3DP ")
        self.assertIsNotNone(user_info)
        self.assertEqual("lb3dp", user_info.uid)

    def test_search_users_falls_back_to_local_cache_in_development(self):
        # Seed the local cache, as if this user had been looked up before, while connected to the VPN.
        LdapService().user_info("lb3dp")

        original_development = app.config.get('DEVELOPMENT')
        app.config['DEVELOPMENT'] = True
        try:
            with patch.object(LdapService, '_LdapService__get_conn',
                              side_effect=LDAPSocketOpenError("vpn down")):
                results = LdapService.search_users("lb3dp", 10)
        finally:
            app.config['DEVELOPMENT'] = original_development

        self.assertEqual(1, len(results))
        self.assertEqual("lb3dp", results[0]['uid'])

    def test_search_users_returns_empty_when_ldap_down_outside_development(self):
        LdapService().user_info("lb3dp")

        original_development = app.config.get('DEVELOPMENT')
        app.config['DEVELOPMENT'] = False
        try:
            with patch.object(LdapService, '_LdapService__get_conn',
                              side_effect=LDAPSocketOpenError("vpn down")):
                results = LdapService.search_users("lb3dp", 10)
        finally:
            app.config['DEVELOPMENT'] = original_development

        self.assertEqual([], results)

