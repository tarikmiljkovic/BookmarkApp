import unittest
from BookmarkApp import BookmarkApp



class Test_BookmarkApp__init__(unittest.TestCase):
    def test_001__init__max_users_negative_value(self):
        users = None
        self.assertRaises(ValueError, BookmarkApp, -1, users)

    def test_002__init__max_users_zero_value(self):
        users = None
        self.assertRaises(ValueError, BookmarkApp, 0, users)

    def test_003__init__max_users_string_value(self):
        users = None
        self.assertRaises(ValueError, BookmarkApp, '1', users)

    def test_004__init__max_users_float_value(self):
        users = None
        self.assertRaises(ValueError, BookmarkApp, 0.1, users)

    def test_005__init__max_users_maximum_value_overflow(self):
        users = None
        self.assertRaises(ValueError, BookmarkApp, 4, users)

    def test_006__init__users_non_list_type(self):
        users = ('user1', 'user2')
        self.assertRaises(ValueError, BookmarkApp, 2, users)

    def test_007__init__max_users_not_equal_to_num_of_users(self):
        users = ['user1', 'user2','user3']
        self.assertRaises(ValueError, BookmarkApp, 1, users)

        users = ['user1']
        self.assertRaises(ValueError, BookmarkApp, 3, users)


class Test_BookmarkApp_select_user(unittest.TestCase):
    def test_003_select_user_robustness(self):
        users = ['user1', 'user2']
        app = BookmarkApp(2, users)
        ret_status, message = app.select_user(None)
        self.assertFalse(ret_status)

    def test_004_select_user_normal(self):
        users = ['user1', 'user2']
        app = BookmarkApp(2, users)
        ret_status, message = app.select_user(0)
        self.assertTrue(ret_status, msg=message)



if __name__ == '__main__':
    unittest.main()