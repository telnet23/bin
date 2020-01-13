import sqlite3

columns = {
    'town': (0, 3),
    'voter_id': (4, 13),
    'last_name': (14, 49),
    'first_name': (50, 70),
    'middle_name': (71, 86),
    'prefix': (87, 92),
    'suffix': (93, 98),
    'status': (99, 100),
    'special_status': (101, 102),
    'reason_code': (103, 104),
    'voter_district': (105, 108),
    'voter_precinct': (109, 111),
    'congressional_district': (112, 115),
    'state_senate': (116, 119),
    'state_assembly': (120, 123),
    'poll_place': (124, 164),
    'local_voter_district': (165, 168),
    'local_voter_precinct': (169, 171),
    'special_voter_district': (172, 175),
    'special_voter_precinct': (176, 178),
    'voter_address_number': (179, 185),
    'voter_address_unit': (186, 194),
    'voter_street': (195, 235),
    'voter_locality': (236, 254),
    'voter_state': (255, 257),
    'voter_zip_code': (258, 263),
    'voter_zip_4': (264, 268),
    'voter_carrier': (269, 273),
    'mail_number': (274, 280),
    'mail_unit': (281, 289),
    'mail_street_1': (290, 330),
    'mail_street_2': (331, 351),
    'mail_city': (352, 382),
    'mail_state': (383, 385),
    'mail_country': (386, 406),
    'mail_zip_code': (407, 417),
    'mail_carrier': (418, 422),
    'date_of_birth': (423, 433),
    'telephone': (434, 444),
    'party': (445, 450),
    'party_unqualified': (451, 456),
    'sex': (457, 458),
    'accepted': (459, 469),
}

connection = sqlite3.connect('voters.sqlite')
cursor = connection.cursor()
cursor.execute('CREATE TABLE voters({})'.format(', '.join(columns.keys())))
for i in range(4):
    with open('SSP/ELCT/VOTER/EXT{}'.format(i+1), 'rb') as lines:
        for line in lines:
            if line.strip() == '\x1a':
                continue
            row = [line[a:b].strip() for (a, b) in columns.values()]
            print(row)
            c.execute('INSERT INTO voters({}) VALUES({})'.format(
                ', '.join(columns.keys()),
                ', '.join('?' * len(columns))), row)
cursor.close()
connection.commit()
