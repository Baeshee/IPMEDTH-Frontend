from PyQt5.Qt import QDesktopServices, QUrl


def open_url(uri):
    """Open a URL in the default browser.

    Args:
        uri (str): The URL to open.
    """
    url = QUrl(uri)
    QDesktopServices.openUrl(url)
