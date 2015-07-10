__author__ = 'bromix'

from ..abstract_context_ui import AbstractContextUI


class MockContextUI(AbstractContextUI):
    def __init__(self, context):
        AbstractContextUI.__init__(self)

        self._context = context
        pass

    def create_progress_dialog(self, heading, text=None, background=False):
        return MockProgressDialog(heading, text)

    def get_skin_id(self):
        return 'skin.kodion.dummy'

    def on_keyboard_input(self, title, default='', hidden=False):
        print '[' + title + ']'
        print "Returning 'Hello World'"
        # var = raw_input("Please enter something: ")
        var = u'Hello World'
        if var:
            return True, var

        return False, ''

    def show_notification(self, message, header='', image_uri='', time_milliseconds=5000):
        self._context.log('=======NOTIFICATION=======')
        self._context.log('Message  : %s' % message)
        self._context.log('header   : %s' % header)
        self._context.log('image_uri: %s' % image_uri)
        self._context.log('Time     : %d' % time_milliseconds)
        self._context.log('==========================')
        pass

    def open_settings(self):
        self._context.log("called 'open_settings'")
        pass

    def refresh_container(self):
        self._context.log("called 'refresh_container'")
        pass

    pass

