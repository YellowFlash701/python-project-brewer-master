# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import argparse
from io import open
import os.path

from pythonbrewer.brew import generate_homebrew_formula

import logging
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="A utility to generate Homebrew formula templates for Python packages"
    )
    parser.add_argument(
        "package_name",
        help="The name of the Python package for which to generate a Homebrew formula template (must already"
             "be installed via pip)"
    )
    parser.add_argument(
        "output_file",
        help="Where to write the formula template (Ruby file)"
    )
    parser.add_argument(
        "-n", "--formula-name",
        default=None,
        help="The name of the Homebrew formula"
    )
    parser.add_argument(
        "-d", "--description",
        default="",
        help="A description for the formula"
    )
    parser.add_argument(
        "-H", "--homepage",
        default="",
        help="The URL of the homepage for this package"
    )
    parser.add_argument(
        "-g", "--git-repo",
        default="",
        help="The URL for the Git repository for this package"
    )
    parser.add_argument(
        "-r", "--release-url",
        default=None,
        help="The URL from which to fetch the release package for the primary Python package (this can, for example, "
             "be a release in your project's GitHub repo)"
    )
    parser.add_argument(
        "-s", "--suffixes",
        default="py2.py3-none-any.whl,.tar.gz,.zip",
        help="A string containing a comma-separated list (no whitespace) of the desired suffixes for dependency "
             "files in order of precedence (default: \"py2.py3-none-any.whl,.tar.gz,.zip\")"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Display verbose logging information"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s' if args.verbose else "%(message)s",
    )

    formula_name = args.formula_name if args.formula_name is not None else \
        ''.join(args.package_name.split('-')).capitalize()

    logger.debug("Formula name: %s" % formula_name)

    output_file = os.path.abspath(args.output_file)
    with open(output_file, "wt", encoding="utf-8") as f:
        template = generate_homebrew_formula(args.package_name, formula_name, args.description,
                                             args.homepage, args.git_repo, release_url=args.release_url,
                                             required_suffixes=args.suffixes.split(","))
        f.write(template)

    logger.info("Wrote template to %s" % output_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())
