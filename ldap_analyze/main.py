import ldap3
import json
import csv
import argparse


class ldap_analyze(object):

    def __init__(self, server, bind_user, bind_pwd, search_path):
        self.server = server
        self.bind_user = bind_user
        self.bind_pwd = bind_pwd
        self.search_path = search_path

    def show_ad_group(self):
        server = ldap3.Server(self.server, get_info=ldap3.ALL)
        filter = '(&(objectCategory=Person)(sAMAccountName=*))'
        with ldap3.Connection(server, user=self.bind_user, password=self.bind_pwd, auto_bind=True) as conn:
            conn.search(self.search_path, filter, attributes=['sAMAccountName', 'lastLogon', 'name', 'userAccountControl'])
            return conn.response_to_json()

def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', nargs='?')
    parser.add_argument('-u', '--ldap_user', nargs='?')
    parser.add_argument('-p', '--ldap_pwd', nargs='?')
    parser.add_argument('-b', '--ldap_bind_dn', nargs='?')
    parser.add_argument('-o', '--output', nargs='?')


    return parser


if __name__ == '__main__':

    parser = create_parser()
    args = parser.parse_args()

    ad = ldap_analyze(args.server, args.ldap_user, args.ldap_pwd, args.ldap_bind_dn)

    with open(args.output, 'w', newline='') as csvfile:
        parsed_json = json.loads(ad.show_ad_group())
        data = parsed_json['entries']
        for item in data:
            if item['attributes'].get('lastLogon') is None:
                item['attributes']['lastLogon'] = 'None'
            if item['attributes']['userAccountControl'] == 512:
                item['attributes']['userAccountControl'] = 'Enabled'
            if item['attributes']['userAccountControl'] == 514:
                item['attributes']['userAccountControl'] = 'Disabled'
            if item['attributes']['userAccountControl'] == 66048:
                item['attributes']['userAccountControl'] = 'Enabled, Password Does not Expire'
            if item['attributes']['userAccountControl'] == 66050:
                item['attributes']['userAccountControl'] = 'Disabled, Password Does not Expire'
            if item['attributes']['userAccountControl'] == 66080:
                item['attributes']['userAccountControl'] = 'Enabled, Password Does not Expire, Not Required'
            if item['attributes']['userAccountControl'] == 66082:
                item['attributes']['userAccountControl'] = 'Disabled, Password Does not Expire, Not Required'
            listwriter = csv.writer(csvfile, delimiter=';')
            listwriter.writerow([item['attributes']['sAMAccountName'], item['attributes']['name'], item['attributes']['lastLogon'], item['attributes']['userAccountControl']])
