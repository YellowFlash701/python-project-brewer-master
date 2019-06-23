# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import hashlib

import requests
import html5lib

from pythonbrewer.errors import *

import logging
logger = logging.getLogger(__name__)

__all__ = [
    "fetch_pypi_package_files",
    "get_pypi_sha256"
]


def get_html_namespace(tree):
    p = re.compile(r"\{(?P<namespace>[^\}]+)\}.+")
    m = p.match(tree[0].tag)
    return m.group('namespace') if m is not None else None


def html_findall(tree, namespace, xpath):
    return tree.findall(xpath.format(ns="{%s}" % namespace))


def fetch_pypi_package_files(package_name, package_version, required_suffixes=None):
    """Attempts to fetch a list of files for the given package/version from PyPI.

    Args:
        package_name: The name of the package for which to fetch files.
        package_version: The version of the package for which to fetch files.
        required_suffixes: The required suffixes for the package files we want. Leave as None if you want all files for
            the particular version. If supplied, it must be a list and must specify, in order of precedence,
            the suffixes.

    Returns:
        A list of URLs to different distributions for the specified package.
    """
    response = requests.get("https://pypi.python.org/simple/%s" % package_name)
    if response.status_code >= 300:
        raise PackageNotFoundError(package_name)

    expected_prefix = ("%s-%s" % (package_name, package_version)).lower()
    expected_prefix_underscore = ("%s-%s" % (package_name.replace("-", "_"), package_version)).lower()

    logger.debug("Expecting PyPI filename prefixes: %s or %s" % (expected_prefix, expected_prefix_underscore))

    # parse the incoming HTML
    tree = html5lib.parse(response.text)
    namespace = get_html_namespace(tree)
    links = html_findall(tree, namespace, "./{ns}body/{ns}a")

    urls_for_suffix = dict([(suffix, []) for suffix in required_suffixes])
    urls = []
    for link in links:
        filename = re.sub(r"\.[0]+(\d+)", r".\1", link.text.strip().lower())
        url = link.attrib["href"]

        if filename.startswith(expected_prefix) or filename.startswith(expected_prefix_underscore):
            if required_suffixes is not None:
                for suffix in required_suffixes:
                    if filename.endswith(suffix):
                        urls_for_suffix[suffix].append(url)
            else:
                urls.append(url)

    # gives us a list of urls sorted by suffix
    if required_suffixes is not None:
        for suffix in required_suffixes:
            urls.extend(urls_for_suffix[suffix])

    for url in urls:
        logger.debug("Found possible URL: %s" % url)

    return urls


def get_pypi_sha256(url):
    """Downloads the given file from the specified URL, optionally validating the MD5/SHA256 hash (if one is supplied
    in the URL itself). Returns the SHA-256 hash of the given file."""
    hash_index_md5 = url.find("#md5=")
    hash_index_sha256 = url.find("#sha256=")

    response = requests.get(url)
    if response.status_code >= 300:
        raise PackageFetchError(url)

    if hash_index_md5 > -1:
        hash_index_sha256 += len("#md5=")
        md5 = hashlib.md5(response.content).hexdigest().lower()
        if md5 != url[hash_index_md5]:
            raise HashValidationFailedError(url, url[hash_index_md5], md5)

    if hash_index_sha256 > -1:
        hash_index_sha256 += len("#sha256=")
        sha256 = hashlib.sha256(response.content).hexdigest().lower()
        if sha256 != url[hash_index_sha256:]:
            raise HashValidationFailedError(url, url[hash_index_sha256:], sha256)
        return url[hash_index_sha256:]

    return hashlib.sha256(response.content).hexdigest()
