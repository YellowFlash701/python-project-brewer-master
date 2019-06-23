# -*- coding: utf-8 -*-

from __future__ import unicode_literals

__all__ = [
    "PackageNotFoundError",
    "MultiplePackagesFoundError",
    "PackageFetchError",
    "HashValidationFailedError"
]


class PackageNotFoundError(Exception):

    def __init__(self, package_name):
        super(PackageNotFoundError, self).__init__("Package cannot be found: %s" % package_name)
        self.package_name = package_name


class MultiplePackagesFoundError(Exception):

    def __init__(self, package_name):
        super(MultiplePackagesFoundError, self).__init__("Multiple packages found: %s" % package_name)
        self.package_name = package_name


class PackageFetchError(Exception):

    def __init__(self, url):
        super(PackageFetchError, self).__init__("Package cannot be fetched: %s" % url)
        self.url = url


class HashValidationFailedError(Exception):

    def __init__(self, url, expected_hash, actual_hash):
        super(HashValidationFailedError, self).__init__("Hash validation for file %s failed. Expected: %s. Actual: %s" % (
            url, expected_hash, actual_hash
        ))
        self.url = url
        self.expected_hash = expected_hash
        self.actual_hash = actual_hash
