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

    pageoffset = 0
    nextInd = "y"
    try:
        if args.output:
            open(args.output, "w").close()
        print("Fetching courses... This may take a while.")

        while True:
            jsonURL = get_dynamic_params(args, pageoffset)
            response = requests.get(
                jsonURL, headers=session.headers, cookies=session.cookies
            )
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code}")
                break

            jsonResponse = response.json()
            if not jsonResponse.get("data"):
                print("No more courses found.")
                break
            for data in jsonResponse["data"]:
                course_info = format_course_data(data)
                if args.output:
                    with open(args.output, "a") as f:
                        f.write(course_info + "\n")
                else:
                    print(course_info)
                    if nextInd == "y":
                        nextInd = input(
                            "Would you like to see the next course? y/n/A: "
                        )
                    elif nextInd == "n":
                        return
                    elif nextInd == "a":
                        nextInd = "a"

            pageoffset += 500
    except Exception as e:
        print(e, "\n Error, could not parse JSON response.")
