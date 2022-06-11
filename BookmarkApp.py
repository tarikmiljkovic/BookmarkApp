from urllib.parse import urlparse
from datetime import datetime
from operator import itemgetter
import validators
import json


class BookmarkApp:
    def __init__(self, max_users, users):
        assert isinstance(max_users, int), "Parameter 'max_users' should be specified as integer."
        assert isinstance(users, list), "Parameter 'users' should be specified as list."

        if max_users < 1:
            raise ValueError("Parameter 'max_users' should be greater than 0.")
        elif len(users) != max_users:
            raise ValueError(
                "Parameter 'max_users' should not exceed number of users in 'users' variable.")

        self.max_users_num = max_users
        self.current_user = users[0]
        self.bookmarks = []
        self.domains = []
        self.secure_urls = 0
        self.users = users

    def select_user(self, option):

        assert isinstance(option, int), "Parameter 'option' should be specified as integer."
        if option < 0:
            raise ValueError("Parameter 'option' should be within range from 1 and max_users_num.")
        elif option > self.max_users_num - 1:
            raise ValueError("Parameter 'option' should be within range from 1 and max_users_num.")


        self.current_user = self.users[option]
        return True, "User '{}' has been selected.".format(self.users[int(option)])

    def add_new_bookmark(self, title, url, tag):
        assert isinstance(title, str), "Parameter 'title' should be specified as string."
        assert isinstance(url, str), "Parameter 'url' should be specified as string."
        assert isinstance(tag, list), "Parameter 'url' should be specified as string."


        valid = validators.url(url)
        if valid != True:
            raise ValueError("The URL is invalid.")
        else:
            data = {
                'title': title,
                'url': url,
                'user': self.current_user,
                'datetime': datetime.utcnow().isoformat(),
                'tag': tag
            }
            msg = ""
            domain_new_flag = 0
            data['domain'] = urlparse(data['url']).netloc
            if data['domain'] not in self.domains:
                self.domains.append(data['domain'])
                msg = msg.__add__("New domain added.")
            else:
                msg = msg.__add__("Domain already exists.")

            data['rating'] = 0
            for data_el in self.bookmarks:
                if data['user'] is data_el['user']:
                    if data['url'] is data_el['url']:
                        data_el['rating'] += 1
                        return True, "Bookmark already exists, rating has been increased."

            self.bookmarks.append(data)
            if "https" in data['url']:
                self.secure_urls += 1
                msg = msg.__add__(" New secure bookmark is added successfully.")
                return True, msg
            else:
                msg = msg.__add__(" New unsecure bookmark is added successfully.")
                return True, msg



    def filter_bookmarks(self, keywords):
        assert isinstance(keywords, list), "Parameter 'keywords' should be specified as list."

        filtered_bookmarks = []
        for data_el in self.bookmarks:
            for keyword in keywords:
                if (data_el['user'] == self.current_user) and (keyword in data_el['tag']):
                    if data_el not in filtered_bookmarks:
                        filtered_bookmarks.append(data_el)

        if len(filtered_bookmarks) == 0:
            return False, "Nothing has been found."
        else:
            return True, "{} item(s) have been found.".format(len(filtered_bookmarks)), filtered_bookmarks

    def remove_tag(self, title, url, tag):
        assert isinstance(title, str), "Parameter 'title' should be specified as string."
        assert isinstance(url, str), "Parameter 'url' should be specified as string."
        assert isinstance(tag, str), "Parameter 'tag' should be specified as string."

        valid = validators.url(url)
        if valid != True:
            raise ValueError("The URL is invalid.")
        else:

            for data_el in self.bookmarks:
                if data_el['url'] is url:
                    if data_el['user'] is self.current_user:
                        if tag in data_el['tag']:
                            data_el['tag'].remove(tag)
                            return True, "Tag '{}' has been removed.".format(tag)
                        else:
                            return False, "Tag does not exist in selected bookmark."

            return False, "There is no bookmark for user '{}'.".format(self.users[1])

    def remove_bookmark(self, url):
        assert isinstance(url, str), "Parameter 'url' should be specified as string."

        valid = validators.url(url)
        if valid != True:
            raise ValueError("The URL is invalid.")
        else:

            for data_el in self.bookmarks:
                if (data_el['user'] is self.current_user):
                    if data_el['url'] is url:
                        self.bookmarks.remove(data_el)
                        return True, "The bookmark has been deleted."

            return False, "The bookmark does not exist."

    def sort_bookmarks(self, option):
        assert isinstance(option, str), "Parameter 'option' should be specified as string."

        sorted_bookmarks = [d for d in self.bookmarks if d['user'] is self.current_user]

        if option == "rating":
            sorted_bookmarks = sorted(sorted_bookmarks, key=itemgetter('rating'), reverse=True)
            return True, "The bookmark for '{}' user is sorted according to rating parameter.".format(
                self.current_user), sorted_bookmarks

        elif option == "datetime":
            sorted_bookmarks = sorted(sorted_bookmarks, key=itemgetter('datetime'), reverse=True)
            return True, "The bookmark for '{}' user is sorted according to datetime parameter.".format(
                self.current_user), sorted_bookmarks

        else:
            raise ValueError("Parameter 'option' has only two possible values: rating and datetime")

    def export_bookmarks(self, filename):
        assert isinstance(filename, str), "Parameter 'filename' should be specified as string."

        with open(filename, 'w') as f:
            for data_el in self.bookmarks:
                json.dump(data_el, f)
                f.write('\n')

        return True, "Bookmarks were successfully exported in '{}' file.".format(filename)

    def import_bookmarks(self, filename):
        assert isinstance(filename, str), "Parameter 'filename' should be specified as string."

        file = open(filename, 'r')
        lines = file.readlines()
        self.bookmarks = []
        for line in lines:
            self.bookmarks.append(json.loads(line.strip()))

        file.close()
        return True, "Bookmarks from '{}' file were successfully imported.".format(filename)
