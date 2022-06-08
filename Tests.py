import unittest
from BookmarkApp import BookmarkApp



class Test_BookmarkApp__init__(unittest.TestCase):
    def test_001__init__max_users_negative_value(self):
        users = ['user1', 'user2','user3']
        self.assertRaises(ValueError, BookmarkApp, -1, users)

    def test_002__init__max_users_zero_value(self):
        users = ['user1', 'user2','user3']
        self.assertRaises(ValueError, BookmarkApp, 0, users)

    def test_003__init__max_users_string_value(self):
        users = ['user1', 'user2','user3']
        self.assertRaises(TypeError, BookmarkApp, '1', users)

    def test_004__init__max_users_float_value(self):
        users = ['user1', 'user2','user3']
        self.assertRaises(TypeError, BookmarkApp, 0.1, users)

    def test_005__init__max_users_maximum_value_overflow(self):
        users = ['user1', 'user2','user3']
        self.assertRaises(OverflowError, BookmarkApp, 4, users)

    def test_006__init__users_non_list_type(self):
        users = ('user1', 'user2')
        self.assertRaises(TypeError, BookmarkApp, 2, users)

    def test_007__init__max_users_not_equal_to_num_of_users(self):
        users = ['user1', 'user2','user3']
        self.assertRaises(ValueError, BookmarkApp, 1, users)

        users = ['user1']
        self.assertRaises(ValueError, BookmarkApp, 3, users)


class Test_BookmarkApp_select_user(unittest.TestCase):
    def test_008_select_user_option_non_integer_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            ret_status, message = app.select_user(None)

        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            ret_status, message = app.select_user("1")

    def test_009_select_user_option_negative_value(self):
        with self.assertRaises(ValueError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            ret_status, message = app.select_user(-1)

    def test_010_select_user_option_exceeds_max_value(self):
        with self.assertRaises(ValueError):
            users = ['user1', 'user2']
            max_user_num = 3
            app = BookmarkApp(max_user_num, users)
            ret_status, message = app.select_user(max_user_num)

    def test_011_select_user_normal(self):
        users = ['user1', 'user2']
        app = BookmarkApp(2, users)
        ret_status, message = app.select_user(0)
        self.assertTrue(ret_status, msg=message)

class Test_BookmarkApp_add_new_bookmark(unittest.TestCase):
    def test_011_add_new_bookmark_title_wrong_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.add_new_bookmark(1, "https://github.com/", ['git'])

if __name__ == '__main__':
    unittest.main()