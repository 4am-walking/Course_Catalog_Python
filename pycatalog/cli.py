import argparse
from pycatalog.catalog import execute


def parse_args():
    parser = argparse.ArgumentParser(
        description="Python Course Catalog",
        formatter_class=argparse.HelpFormatter,
    )

    searchGroup = parser.add_argument_group("Search Options")
    searchGroup.add_argument(
        "term",
        help="Term Code is YYYY then 20,30,40 for spring, summer, or fall i.e. 202440 is Fall 2024",
    )
    searchGroup.add_argument(
        "-s", "--subject", help="Subject Code i.e. CPSC, MATH, ENEE"
    )
    searchGroup.add_argument(
        "-n", "--number", help="Course Number i.e. 2100, 4700, 1100"
    )
    searchGroup.add_argument(
        "-k",
        "--keyword",
        help="Keyword i.e. Chemistry, Computer Architecture, Assembly",
    )
    searchGroup.add_argument("-l", "--level", help="Level i.e. Graduate, Undergraduate")
    searchGroup.add_argument(
        "-c",
        "--campus",
        help="Campus i.e. UT Chattanooga, UTC Hybrid/Online",
    )
    searchGroup.add_argument(
        "-i",
        "--instructor",
        help="Instructor i.e. Adam Sandler, Derek Savage",
    )

    outputGroup = parser.add_argument_group("Output Options")
    outputGroup.add_argument(
        "-o",
        "--output",
        help="Output file name. If not provided, output will be printed to the console",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    execute(args)
