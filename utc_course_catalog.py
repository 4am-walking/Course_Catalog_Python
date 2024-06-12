import requests
import argparse
import urllib.parse


def build_url(baseURL, params):
    queryParams = {k: v for k, v in params.items() if v}
    return f"{baseURL}?{urllib.parse.urlencode(queryParams)}"


def main():
    parser = argparse.ArgumentParser(
        description="Python Course Catalog",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "term",
        help="Term Code is YYYY then 20,30,40 for spring, summer, or fall i.e. 202440 is Fall 2024",
    )
    parser.add_argument("-s", "--subject", help="Subject Code i.e. CPSC, MATH, ENEE")
    parser.add_argument("-n", "--number", help="Course Number i.e. 2100, 4700, 1100")
    parser.add_argument(
        "-k",
        "--keyword",
        help="Keyword i.e. Chemistry, Computer Architecture, Assembly",
    )
    parser.add_argument("-l", "--level", help="Level i.e. Graduate, Undergraduate")
    parser.add_argument(
        "-c",
        "--campus",
        help="Campus i.e. UT Chattanooga, UTC Hybrid/Online",
    )
    parser.add_argument(
        "-i",
        "--instructor",
        help="Instructor i.e. Adam Sandler, Derek Savage",
    )
    args = parser.parse_args()

    staticParams = {
        "txt_partOfTerm": "1",
        "startDatepicker": "",
        "endDatepicker": "",
        "pageOffset": "0",
        "pageMaxSize": "1000",
        "sortColumn": "subjectDescription",
        "sortDirection": "asc",
    }

    dynamicParams = {
        "txt_subject": args.subject,
        "txt_courseNumber": args.number,
        "txt_keywordlike": args.keyword,
        "txt_level": args.level,
        "txt_campus": args.campus,
        "txt_instructor": args.instructor,
        "txt_term": args.term,
    }

    full_params = {**dynamicParams, **staticParams}
    baseURL = "https://sis-reg.utc.edu:443/StudentRegistrationSsb/ssb/searchResults/searchResults"
    jsonURL = build_url(baseURL, full_params)

    pilotURL = (
        "https://sis-reg.utc.edu:443/StudentRegistrationSsb/ssb/term/search?mode=search"
    )
    pilotData = {
        "term": args.term,
    }

    session = requests.session()
    session.get(pilotURL)

    requests.post(
        pilotURL, headers=session.headers, cookies=session.cookies, data=pilotData
    )

    jsonResponse = requests.get(
        jsonURL, headers=session.headers, cookies=session.cookies
    ).json()
    nextInd = "Y"
    try:
        for i in range(len(jsonResponse["data"])):
            data = jsonResponse["data"][i]
            print(f"Course: {data['courseTitle']}")
            print(f"Seats available: {data['seatsAvailable']}")
            if nextInd == "Y" or nextInd == "y":
                nextInd = input("Would you like to see the next course? y/n/A")
            elif nextInd == "N" or nextInd == "n":
                break
            elif nextInd == "A" or nextInd == "a":
                continue
    except Exception as e:
        print(e, "\n Error, could not parse JSON response.")


if __name__ == "__main__":
    main()
