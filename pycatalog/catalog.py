import requests
from pycatalog.config import get_dynamic_params


def format_course_data(data):
    professor = "N/A or TBD"
    professor_contact = ""
    if data["faculty"]:
        professor = data["faculty"][0]["displayName"]
        professor_contact = data["faculty"][0]["emailAddress"]
    return f"""
    Course: {data['courseTitle']}
    CRN: {data['courseReferenceNumber']}
    Subject: {data['subjectDescription']}
    Course Number: {data['courseNumber']}
    Professor: {professor}
    Professor Contact: {professor_contact}
    Seats available: {data['seatsAvailable']}
    ---------------------------------------------------------
    """


def execute(args):
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

    jsonURL = get_dynamic_params(args)
    jsonResponse = requests.get(
        jsonURL, headers=session.headers, cookies=session.cookies
    ).json()

    nextInd = "y"
    try:
        if args.output:
            open(args.output, "w").close()
        for data in jsonResponse["data"]:
            course_info = format_course_data(data)
            if args.output:
                with open(args.output, "a") as f:
                    f.write(course_info)
            else:
                print(course_info)
                if nextInd == "y":
                    nextInd = input("Would you like to see the next course? y/n/A: ")
                elif nextInd == "n":
                    break
                elif nextInd == "a":
                    continue
    except Exception as e:
        print(e, "\n Error, could not parse JSON response.")
