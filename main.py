from BookmarkApp import BookmarkApp

if __name__ == '__main__':
    app = BookmarkApp(['Tarik', 'Emina', 'Richard'])
    ret_status, message = app.select_user(0)
    if (ret_status == True):
        print(message)

    ret_status, message = app.add_new_bookmark(title="prvo", url="https://mentalibor.ba")
    if (ret_status == True):
        print(message)

    ret_status, message = app.add_new_bookmark(title="drugo", url="https://mentalibor.com")
    if (ret_status == True):
        print(message)

    ret_status, message = app.select_user(1)
    if (ret_status == True):
        print(message)

    ret_status, message = app.add_new_bookmark(title="drugo", url="https://mentalibor.com")
    if (ret_status == True):
        print(message)

    ret_status, message = app.export_bookmarks()

    app.import_bookmarks()