import unittest
import os
from os.path import exists

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
    def test_012_add_new_bookmark_title_wrong_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.add_new_bookmark(1, "https://github.com/", ['git'])

    def test_013_add_new_bookmark_url_wrong_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.add_new_bookmark("title", 1, ['git'])

    def test_014_add_new_bookmark_tag_wrong_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.add_new_bookmark("title", "https://github.com/", 1)

    def test_015_add_new_bookmark_invalid_url(self):
        with self.assertRaises(ValueError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.add_new_bookmark("title", "abc123", [])

    def test_016_add_new_bookmark_unique_bookmark(self):
        app = BookmarkApp(2, ['user1', 'user2'])
        ret_status, message = app.add_new_bookmark("GIT", "https://github.com/", ['git', 'code'])
        self.assertTrue(ret_status)
        self.assertEqual(message, "New bookmark is added successfully.")

    def test_017_add_new_bookmark_duplicate_bookmark(self):
        app = BookmarkApp(2, ['user1', 'user2'])
        ret_status, message = app.add_new_bookmark("GIT", "https://github.com/", ['git', 'code'])
        ret_status, message = app.add_new_bookmark("GIT", "https://github.com/", ['git', 'code'])
        self.assertTrue(ret_status)
        self.assertEqual(message, "Bookmark already exists, rating has been increased.")

class Test_BookmarkApp_filter_bookmarks(unittest.TestCase):
    def test_018_filter_bookmarks_keywords_wrong_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.filter_bookmarks(1)

        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.filter_bookmarks(None)

    def test_019_filter_bookmarks_single_keywoed(self):
        max_users = 2
        users = ['user1', 'user2']
        app = BookmarkApp(max_users, users)
        ret_status, message = app.add_new_bookmark("GIT", "https://github.com/", ['git', 'code'])
        ret_status, message, filtered_bookmarks = app.filter_bookmarks(['git'])
        self.assertTrue(ret_status)
        self.assertIn(str(len(filtered_bookmarks)), message)

    def test_020_filter_bookmarks_multiple_keywords(self):
        max_users = 2
        users = ['user1', 'user2']
        app = BookmarkApp(max_users, users)
        ret_status, message = app.add_new_bookmark("GIT", "https://github.com/", ['git', 'code'])
        ret_status, message, filtered_bookmarks = app.filter_bookmarks(['git', 'code'])
        self.assertTrue(ret_status)
        self.assertIn(str(len(filtered_bookmarks)), message)

    def test_021_filter_bookmarks_not_found(self):
        max_users = 2
        users = ['user1', 'user2']
        app = BookmarkApp(max_users, users)
        ret_status, message = app.add_new_bookmark("GIT", "https://github.com/", ['git', 'code'])
        ret_status, message = app.filter_bookmarks(['tool'])
        self.assertFalse(ret_status)
        self.assertIn(message, "Nothing has been found.")

class Test_BookmarkApp_remove_tag(unittest.TestCase):
    def test_022_remove_tag_title_wrong_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.remove_tag(1, "https://github.com/", "git")

    def test_023_remove_tag_url_wrong_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.remove_tag("title", 1, "git")

    def test_024_remove_tag_tag_wrong_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.remove_tag("title", "https://github.com/", 1)

    def test_025_remove_tag_invalid_url(self):
        with self.assertRaises(ValueError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.remove_tag("title", "abc123", "tag")

    def test_026_remove_tag_remove_existing_single_tag(self):
        users = ['user1', 'user2']
        app = BookmarkApp(2, users)
        title = "GIT"
        url = "https://github.com/"
        tags = ['git', 'code']
        ret_status, message = app.add_new_bookmark(title, url, tags)
        ret_status, message = app.remove_tag(title, url, "git")
        self.assertTrue(ret_status)

    def test_027_remove_tag_remove_non_existing_single_tag(self):
        users = ['user1', 'user2']
        app = BookmarkApp(2, users)
        title = "GIT"
        url = "https://github.com/"
        tags = ['git', 'code']
        ret_status, message = app.add_new_bookmark(title, url, tags)
        ret_status, message = app.remove_tag(title, url, "tool")
        self.assertFalse(ret_status)

class Test_BookmarkApp_remove_bookmark(unittest.TestCase):
    def test_028_remove_bookmark_url_wrong_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.remove_bookmark(1)

        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.remove_bookmark(None)

    def test_029_remove_bookmark_invalid_url(self):
        with self.assertRaises(ValueError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.remove_bookmark("abc123")

    def test_030_remove_bookmark_existing_bookmark(self):
        users = ['user1', 'user2']
        max_users = 2
        app = BookmarkApp(max_users, users)

        url = "https://github.com/"
        ret_status, message = app.add_new_bookmark("GIT", url, ['git', 'code'])
        ret_status, message = app.remove_bookmark(url)
        self.assertTrue(ret_status)
        self.assertEqual(message, "The bookmark has been deleted.")

    def test_031_remove_bookmark_non_existing_bookmark(self):
        users = ['user1', 'user2']
        max_users = 2
        app = BookmarkApp(max_users, users)

        url = "https://github.com/"
        ret_status, message = app.add_new_bookmark("GIT", url, ['git', 'code'])

        url = "https://google.com/"
        ret_status, message = app.remove_bookmark(url)
        self.assertFalse(ret_status)
        self.assertEqual(message, "The bookmark does not exist.")


class Test_BookmarkApp_sort_bookmarks(unittest.TestCase):
    def test_032_sort_bookmarks_option_wrong_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.sort_bookmarks(1)

        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.sort_bookmarks(None)

    def test_033_sort_bookmarks_option_wrong_value(self):
        with self.assertRaises(ValueError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.sort_bookmarks("aabbcc112233")

    def test_034_sort_bookmarks_according_to_rating(self):
        users = ['user1', 'user2']
        max_users = 2
        app = BookmarkApp(max_users, users)

        url = "https://github.com/"
        ret_status, message = app.add_new_bookmark("GIT", url, ['git', 'code'])
        url = "https://github.com/"
        ret_status, message = app.add_new_bookmark("GIT", url, ['git', 'code'])
        url = "https://github.com/"
        ret_status, message = app.add_new_bookmark("GIT", url, ['git', 'code'])

        url = "https://google.com/"
        ret_status, message = app.add_new_bookmark("Google", url, ['google', 'knowledge'])
        url = "https://google.com/"
        ret_status, message = app.add_new_bookmark("Google", url, ['google', 'knowledge'])


        url = "https://youtube.com/"
        ret_status, message = app.add_new_bookmark("YouTube", url, ['google', 'fun'])

        ret_status, message, sorted_bookmarks = app.sort_bookmarks("rating")
        self.assertTrue(ret_status)
        self.assertEqual(message, "The bookmark for '{}' user is sorted according to rating parameter.".format(app.current_user))

    def test_035_sort_bookmarks_according_to_datetime(self):
        users = ['user1', 'user2']
        max_users = 2
        app = BookmarkApp(max_users, users)

        url = "https://github.com/"
        ret_status, message = app.add_new_bookmark("GIT", url, ['git', 'code'])

        url = "https://google.com/"
        ret_status, message = app.add_new_bookmark("Google", url, ['google', 'knowledge'])

        url = "https://youtube.com/"
        ret_status, message = app.add_new_bookmark("YouTube", url, ['google', 'fun'])

        ret_status, message, sorted_bookmarks = app.sort_bookmarks("datetime")
        self.assertTrue(ret_status)
        self.assertEqual(message,
                         "The bookmark for '{}' user is sorted according to datetime parameter.".format(app.current_user))

class Test_BookmarkApp_export_bookmarks(unittest.TestCase):
    def test_036_export_bookmarks_filename_wrong_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.export_bookmarks(1)

        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.export_bookmarks(None)

    def test_037_export_bookmarks(self):
        users = ['user1', 'user2']
        max_users = 2
        app = BookmarkApp(max_users, users)

        url = "https://github.com/"
        ret_status, message = app.add_new_bookmark("GIT", url, ['git', 'code'])

        url = "https://google.com/"
        ret_status, message = app.add_new_bookmark("Google", url, ['google', 'knowledge'])

        url = "https://youtube.com/"
        ret_status, message = app.add_new_bookmark("YouTube", url, ['google', 'fun'])

        filename = "bookmarks_data.json"
        if (exists(filename)):
            os.remove(filename)

        ret_status, message = app.export_bookmarks(filename)
        self.assertTrue(ret_status)
        self.assertEqual(message, "Bookmarks were successfully exported in '{}' file.".format(filename))
        self.assertTrue(exists(filename))

class Test_BookmarkApp_import_bookmarks(unittest.TestCase):
    def test_038_import_bookmarks_filename_wrong_type(self):
        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.import_bookmarks(1)

        with self.assertRaises(TypeError):
            users = ['user1', 'user2']
            app = BookmarkApp(2, users)
            app.import_bookmarks(None)

    def test_037_export_bookmarks(self):
        users = ['user1', 'user2']
        max_users = 2
        app = BookmarkApp(max_users, users)

        url = "https://github.com/"
        ret_status, message = app.add_new_bookmark("GIT", url, ['git', 'code'])

        url = "https://google.com/"
        ret_status, message = app.add_new_bookmark("Google", url, ['google', 'knowledge'])

        url = "https://youtube.com/"
        ret_status, message = app.add_new_bookmark("YouTube", url, ['google', 'fun'])

        filename = "bookmarks_data.json"
        if (exists(filename)):
            os.remove(filename)

        ret_status, message = app.export_bookmarks(filename)

        app.bookmarks = []
        ret_status, message = app.import_bookmarks(filename)
        self.assertTrue(ret_status)
        self.assertEqual(message, "Bookmarks from '{}' file were successfully imported.".format(filename))
        self.assertNotEqual(app.bookmarks, [])