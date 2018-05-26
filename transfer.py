import os
import requests
import sys

session = requests.Session()

base = sys.argv[1]
schools = sys.argv[2:]

for school in schools:
    print(school)
    school_response = session.get(f'{base}/school/{school}')
    subjects = school_response.json()
    for subject in subjects:
        print(school, subject)
        subject_response = session.get(f'{base}/{school}/{subject}')
        courses = subject_response.json()
        if 'error' in courses:
            print(school, subject, 'error')
            continue
        if not os.path.exists(school):
            os.mkdir(school)
        with open(os.path.join(school, subject.replace('/', '_') + '.json'), 'wb') as save:
            save.write(subject_response.content)
