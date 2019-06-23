# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from future.utils import iteritems

from pipdeptree import build_dist_index, construct_tree, sorted_tree

from pythonbrewer.errors import *

import logging
logger = logging.getLogger(__name__)

__all__ = [
    "build_dep_list"
]


def get_children(key_tree, n):
    return key_tree.get(n.key, [])


def recursive_build_tree(key_tree, n):
    tree = dict()
    for child in get_children(key_tree, n):
        tree[child.project_name] = child.as_dict()
        tree[child.project_name]['deps'] = recursive_build_tree(key_tree, child)
    return tree if len(tree) else None


def recursive_extract_dep_list(key_tree, cur_key):
    deps = []
    logger.debug("Extracting dependencies for: %s" % cur_key)
    for package in key_tree[cur_key]:
        # if this package has dependencies, add those first
        if len(key_tree[package.key]) > 0:
            deps.extend(recursive_extract_dep_list(key_tree, package.key))

        logger.debug("Adding %s as a dependency" % package.key)
        # add this package as a dependency
        deps.append(package)

    return deps


def build_dep_list(package_name, local_only=True):
    """Builds a dependency list for the given package, assuming the given package has already been
    installed. The dependency list is provided in the order in which it needs to be installed.

    Args:
        package_name: The name of the package for which to build a dependency tree.
        local_only: Look in local distribution? Default: True.

    Returns:
        A Python list containing information about the dependencies for that package.
    """
    ## Dealing with pip 10.* api chagnes
    ## The solution is from:
    ## https://github.com/naiquevin/pipdeptree/blob/master/pipdeptree.py
    try:
        from pip._internal.utils.misc import get_installed_distributions
    except ImportError:
        from pip import get_installed_distributions
    packages = get_installed_distributions(local_only=local_only)
    dist_index = build_dist_index(packages)
    tree = sorted_tree(construct_tree(dist_index))
    nodes = tree.keys()
    # filter by our desired package only
    nodes = [p for p in nodes if p.key == package_name or p.project_name == package_name]
    if len(nodes) == 0:
        raise PackageNotFoundError(package_name)
    if len(nodes) > 1:
        raise MultiplePackagesFoundError(package_name)

    key_tree = dict((k.key, v) for k, v in iteritems(tree))
    deps = recursive_extract_dep_list(key_tree, package_name)

    unique_deps = []
    seen_deps = set()
    for dep in deps:
        if dep.key not in seen_deps:
            unique_deps.append(dep.as_dict())
            seen_deps.add(dep.key)
        else:
            logger.debug("Duplicate dependency found: %s" % dep.project_name)
    return unique_deps
