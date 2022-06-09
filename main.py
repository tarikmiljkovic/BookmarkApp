from BookmarkApp import BookmarkApp

if __name__ == '__main__':
    app = BookmarkApp(3, ['user1', 'user2', 'user3'])
    ret_status, message = app.select_user(0)
    if (ret_status == True):
        print(message)

    ret_status, message = app.add_new_bookmark(title="Tarik", url="https://tarikmiljkovic.at", tag = [])
    if (ret_status == True):
        print(message)

    ret_status, message = app.add_new_bookmark(title="Tarik", url="https://tarikmiljkovic.at", tag = [])
    if (ret_status == True):
        print(message)

    ret_status, message = app.select_user(1)
    if (ret_status == True):
        print(message)

    ret_status, message = app.add_new_bookmark(title="Tarik", url="https://tarikmiljkovic.at", tag = [])
    if (ret_status == True):
        print(message)

    ret_status, message = app.export_bookmarks()

    app.import_bookmarks()