import urllib.parse

staticParams = {
    "txt_partOfTerm": "1",
    "startDatepicker": "",
    "endDatepicker": "",
    "pageOffset": "0",
    "pageMaxSize": "1000",
    "sortColumn": "subjectDescription",
    "sortDirection": "asc",
}


def build_url(baseURL, params):
    queryParams = {k: v for k, v in params.items() if v}
    return f"{baseURL}?{urllib.parse.urlencode(queryParams)}"


def get_dynamic_params(args):
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
    return jsonURL
