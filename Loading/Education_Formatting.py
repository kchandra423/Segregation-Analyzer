import pprint

from Loading import client

# distrcits source is ::::Data Source: U.S. Department of Education National Center for Education Statistics Common Core of Data (CCD) "Local Education Agency (School District) Universe Survey" 2018-19 v.1a  2019-20 v.1a; "Local Education Agency (School District) Universe Survey Geographic Data (EDGE)" 2018-19 v.1a; "Public Elementary/Secondary School Universe Survey" 2018-19 v.1a.
# schools source is  :::::Data Source: U.S. Department of Education National Center for Education Statistics Common Core of Data (CCD) "Public Elementary/Secondary School Universe Survey" 2018-19 v.1a  2019-20 v.1a; "Public Elementary/Secondary School Universe Survey Geographic Data (EDGE)" 2018-19 v.1a.

educational_institutes = client.get_database('EducationData')
districts = educational_institutes.get_collection("districts_raw")
schools = educational_institutes.get_collection("schools_raw")
district_map = {}
school_map = {}


def clean_education_data():
    cleaned_districts = clean_districts()
    cleaned_schools = clean_schools()
    result_districts = remove_districts(cleaned_districts)
    result_schools = remove_schools(cleaned_schools)
    educational_institutes.create_collection("Districts").insert_many(result_districts)
    educational_institutes.create_collection("Schools").insert_many(result_schools)


def remove_districts(given_districts):
    chosen = []
    for district in given_districts:
        if len(district['Schools']) <= 2 or district['POP'] < 50:
            del district_map[district['District_ID']]
        else:
            chosen.append(district)
    return chosen


def remove_schools(given_schools):
    chosen = []
    for school in given_schools:
        if find_district(school['District_ID']) is not None:
            chosen.append(school)
    return chosen


def find_district(_id):
    return district_map.get(_id, None)


def clean_schools():
    formatted = []
    all_schools = schools.find()
    for school in all_schools:
        school: dict
        for key in school.keys():
            if school[key] == '†' or school[key] == '–' or school[key] == '‡':
                school[key] = None
        school['NAME'] = capitalize(school.pop('School Name').lower())
        del school['State Name']
        school['District_ID'] = school.pop('Agency ID')
        school['School_ID'] = school.pop('School ID')
        black = school.pop('Black or African American Students')
        hispanic = school.pop('Hispanic Students')
        # ignore where not reported
        if black is None:
            continue
        if hispanic is None:
            continue
        brown = int(black) + int(hispanic)
        school['BROWN'] = brown
        pop = school.pop('Total Race')
        if pop is None:
            continue
        pop = int(pop)

        # ignore if not reported
        if pop == 0:
            continue
        school['POP'] = pop

        result = find_district(school['District_ID'])
        if result is None:
            # pprint.pprint(school)
            continue
        else:
            result['POP'] += school['POP']
            result['BROWN'] += school['BROWN']
            result['Schools'].append(school['_id'])
        formatted.append(school)
    return formatted


def clean_districts():
    formatted = []
    all_districts = districts.find()
    for district in all_districts:
        district: dict
        for key in district.keys():
            if district[key] == '†' or district[key] == '–' or district[key] == '‡':
                district[key] = None
        district['NAME'] = capitalize(district.pop('Agency Name').lower())
        district['State_Name'] = capitalize(district.pop('State Name').lower())
        district['District_ID'] = district.pop('Agency ID')
        district['County_Name'] = capitalize(district.pop('County Name').lower())
        state = district.pop('FIPS')
        if len(state) == 1:
            state = '0' + state
        county = district.pop('County Number')[-3:]
        district['state'] = state
        district['county'] = county

        district['Schools'] = []
        district['POP'] = 0
        district['BROWN'] = 0
        formatted.append(district)
        district_map[district['District_ID']] = district
    return formatted


def capitalize(message):
    parts = message.split(" ")
    capitalized_parts = [p.capitalize() for p in parts]
    return " ".join(capitalized_parts)
