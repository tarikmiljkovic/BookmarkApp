from urllib.parse import urlparse
from datetime import datetime
from operator import itemgetter
import validators
import json


class BookmarkApp:
    def __init__(self, max_users, users):
        if (type(max_users) is not int):
            raise TypeError("Parameter 'max_users' should be integer.")
        if (type(users) is not list):
            raise TypeError("Parameter 'users' should be list.")
        if (max_users <= 0):
            raise ValueError("Parameter 'max_users' should be greater than 0.")
        if (max_users > 3):
            raise OverflowError("Parameter 'max_users' should be lower than 3.")
        if (len(users) != max_users):
            raise ValueError("Please enter {} missing username(s).".format(abs(len(users)-max_users)))

        self.max_users_num = max_users
        self.current_user = None
        self.bookmarks = []
        self.domains = []
        self.secure_urls = 0


        self.users = users

    def select_user(self, option):
        if type(option) is not int:
            raise TypeError("Parameter 'option' should be integer.")
        if (option < 0) or (option > self.max_users_num):
            raise ValueError("Parameter 'option' should be within range from 1 and max_users_num.")

        self.current_user = self.users[option]
        return True, "User '{}' has been selected.".format(self.users[int(option)])

    def add_new_bookmark(self, title, url, tag):
        if (type(title) is not str):
            raise TypeError("Parameter 'title' should be specified as string.")

        if (type(url) is not str):
            raise TypeError("Parameter 'url' should be specified as string.")

        if (type(tag) is not list):
            raise TypeError("Parameter 'tag' should be specified as string.")

        valid = validators.url(url)
        if valid != True:
            raise ValueError ("The URL is invalid.")

        data = {
            'title': title,
            'url': url,
            'user': self.current_user,
            'datetime': datetime.utcnow().isoformat(),
            'tag': tag
        }

        data['domain'] = urlparse(data['url']).netloc
        if data['domain'] not in self.domains:
            self.domains.append(data['domain'])

        data['rating'] = 0
        for data_el in self.bookmarks:
            if data['user'] == data_el['user'] and data['url'] == data_el['url']:
                data_el['rating'] = data_el['rating'] + 1
                return True, "Bookmark already exists, rating has been increased."

        self.bookmarks.append(data)
        if ("https" in data['url']):
            self.secure_urls = self.secure_urls + 1
        return True, "New bookmark is added successfully."

    def filter_bookmarks(self, keywords=None):
        filtered_bookmarks = []
        for data_el in self.bookmarks:
            if data_el['user'] == self.current_user:
                for keyword in keywords:
                    if (keyword in data_el['tag']):
                        if (data_el not in filtered_bookmarks):
                            filtered_bookmarks.append(data_el)

        if filtered_bookmarks.len() == 0:
            return False, "Nothing has been found."
        else:
            return True, filtered_bookmarks

    def remove_tag(self, title=None, url=None, tag=None):
        if (tag is None):
            return False, "Tag is not provided."
        if (url is None):
            return False, "URL of bookmark is not provided."

        for data_el in self.bookmarks:
            if (data_el['user'] == self.current_user):
                if data_el['url'] == url:
                    if (tag in data_el['tag']):
                        data_el['tag'].remove(tag)
                        return True, "Tag has been removed."
                    else:
                        return False, "Tag does not exist."

    def remove_bookmark(self, url=None):
        if (url is None):
            return False, "URL of bookmark is not provided."

        for data_el in self.bookmarks:
            if (data_el['user'] == self.current_user):
                if data_el['url'] == url:
                    self.bookmarks.remove(data_el)
                    return True, "The bookmark has been deleted."

        return False, "The bookmark does not exist."

    def sort_bookmarks(self, option=None):
        if (option is None):
            return False, "The option is not specified."

        sorted_bookmarks = []
        for data_el in self.bookmarks:
            if (data_el['user'] == self.current_user):
                sorted_bookmarks.append(data_el)

        if option == "rating":
            newlist = sorted(sorted_bookmarks, key=itemgetter('rating'))
            return True, newlist

        elif option == "datetime":
            newlist = sorted(sorted_bookmarks, key=itemgetter('datetime'))
            return True, newlist

    def export_bookmarks(self):
        try:
            with open('bookmarks_data.json', 'w') as f:
                for data_el in self.bookmarks:
                    json.dump(data_el, f)
                    f.write('\n')

            return True, "Bookmarks were successfully exported."
        except:
            return False, "Bookmarks cannot be exported."

    def import_bookmarks(self):
        try:
            file = open('bookmarks_data.json', 'r')
            lines = file.readlines()
            self.bookmarks = []
            for line in lines:
                self.bookmarks.append(json.loads(line.strip()))
            return True, "Bookmarks were successfully imported."
        except:
            return False, "Bookmarks cannot be imported."
