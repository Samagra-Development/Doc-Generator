from interface import Interface


class URLShortener(Interface):
    """
    Interface for URL Shortner
    """

    def apply(self, long_url):
        pass

    def get_long(self, short_url):
        pass
