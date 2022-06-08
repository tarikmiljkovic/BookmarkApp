import unittest
from BookmarkApp import BookmarkApp



class Test_BookmarkApp__init__(unittest.TestCase):
    def test_001_ensure_init_app_with_wrong(self):
        users = None
        self.assertRaises(ValueError, BookmarkApp, 0, users)

    def test_002_init_app_exceed_max_num_of_users(self):
        users = ['user1', 'user2','user3']
        self.assertRaises(ValueError, BookmarkApp, 1, users)


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