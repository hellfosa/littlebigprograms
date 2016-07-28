import requests
import ldap3
import json
import argparse

class ldap2gitlab(object):

    def __init__(self):
        pass

    def show_ad_group(self):
        server = ldap3.Server(args.server, get_info=ldap3.ALL)
        filter = '(&(objectclass=Person)(memberOf=CN={0},{1}))'.format(args.ldap_group, args.ldap_bind_dn)
        with ldap3.Connection(server, user=args.ldap_user, password=args.ldap_pwd, auto_bind=True) as conn:
            conn.search(args.ldap_bind_dn, filter, attributes=['sAMAccountName'])
            return conn.response_to_json()

    def show_member_id(self, aduser):
        get_url = "{0}/api/v3/users/?private_token={1}".format(args.gitlab_url, args.gitlab_apikey)
        get_users = requests.get(get_url).json()
        dict = {}

        for user in get_users:
            for key in user:
                if key == 'id':
                    userid = (user['id'])
                if key == 'username':
                    username = (user['username'])
            dict[username] = userid

        if aduser in dict.keys():
            return dict[aduser]

    def add_member(self, member_id, group_id, access_level):
        post_url = "{0}/api/v3/groups/{1}/members?private_token={2}".format(args.gitlab_url, group_id, args.gitlab_apikey)
        params = {'id': group_id, 'user_id': member_id, 'access_level': access_level}
        return requests.post(post_url, params=params).json()

    def edit_member(self, member_id, group_id, access_level):
        post_url = "{0}/api/v3/groups/{1}/members/{2}?private_token={3}".format(args.gitlab_url, group_id, member_id, args.gitlab_apikey)
        params = {'id': group_id, 'user_id': member_id, 'access_level': access_level}
        return requests.put(post_url, params=params).json()

def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', nargs='?')
    parser.add_argument('-u', '--ldap_user', nargs='?')
    parser.add_argument('-p', '--ldap_pwd', nargs='?')
    parser.add_argument('-b', '--ldap_bind_dn', nargs='?', default='OU=it, OU=main, OU=spb, OU=users, OU=humans, OU=mbk, DC=infocom, DC=lan')
    parser.add_argument('-w', '--ldap_group', nargs='?')
    parser.add_argument('-r', '--gitlab_url', nargs='?')
    parser.add_argument('-a', '--gitlab_apikey', nargs='?')
    parser.add_argument('-g', '--gitlab_group', nargs='?')
    parser.add_argument('-l', '--gitlab_access_level', nargs='?')
    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    group = ldap2gitlab()
    parsed_json = json.loads(group.show_ad_group())
    data = parsed_json['entries']
    for item in data:
        for key, value in item['attributes'].items():
            id = group.show_member_id(value)
            add = group.add_member(id, args.gitlab_group, args.gitlab_access_level)
            if add['message'] == 'Already exists':
                group.edit_member(id, args.gitlab_group, args.gitlab_access_level)

