"""Module containing mock functions which replace checkedCast() in tests."""

def mock_auth_checked_cast(proxy):
    """Checks if the mock proxy passed as an argument is mocking an
    Authenticator proxy."""
    if proxy.name == 'AuthenticatorPrx':
        return proxy
    return None

def mock_catalog_checked_cast(proxy):
    """Checks if the mock proxy passed as an argument is mocking a
    MediaCatalog proxy."""
    if proxy.name == 'MediaCatalogPrx':
        return proxy
    return None

def mock_file_checked_cast(proxy):
    """Checks if the mock proxy passed as an argument is mocking a
    FileService proxy."""
    if proxy.name == 'FileServicePrx':
        return proxy
    return None
