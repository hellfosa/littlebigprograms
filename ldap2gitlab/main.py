import requests
import ldap3
import json
import argparse

class ldap2gitlab(object):

    def __init__(self, server, bind_user, bind_pwd, search_path, group, gitlab_url, gitlab_apikey):
        self.server = server
        self.bind_user = bind_user
        self.bind_pwd = bind_pwd
        self.search_path = search_path
        self.group = group
        self.gitlab_url = gitlab_url
        self.gitlab_apikey = gitlab_apikey

    def show_ad_group(self):
        server = ldap3.Server(self.server, get_info=ldap3.ALL)
        filter = '(&(objectclass=Person)(memberOf=CN={0},{1}))'.format(self.group, self.search_path)
        with ldap3.Connection(server, user=self.bind_user, password=self.bind_pwd, auto_bind=True) as conn:
            conn.search(self.search_path, filter, attributes=['sAMAccountName'])
            return conn.response_to_json()

    def show_member_id(self, aduser):
        self.aduser = aduser
        get_url = "{0}/api/v3/users/?private_token={1}".format(self.gitlab_url, self.gitlab_apikey)
        get_users = requests.get(get_url).json()
        dict = {}

        for user in get_users:
            for key in user:
                if key == 'id':
                    userid = (user['id'])
                if key == 'username':
                    username = (user['username'])
            dict[username] = userid

        if self.aduser in dict.keys():
            return dict[self.aduser]

    def add_member(self, member_id, group_id, access_level):
        self.member_id = member_id
        self.group_id = group_id
        self.access_level = access_level
        post_url = "{0}/api/v3/groups/{1}/members?private_token={2}".format(self.gitlab_url, self.group_id, self.gitlab_apikey)
        params = {'id': self.group_id, 'user_id': self.member_id, 'access_level': self.access_level}
        return requests.post(post_url, params=params).json()

    def edit_member(self, member_id, group_id, access_level):
        self.member_id = member_id
        self.group_id = group_id
        self.access_level = access_level
        post_url = "{0}/api/v3/groups/{1}/members/{2}?private_token={3}".format(self.gitlab_url, self.group_id, self.member_id, self.gitlab_apikey)
        params = {'id': self.group_id, 'user_id': self.member_id, 'access_level': self.access_level}
        return requests.put(post_url, params=params).json()

def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', nargs='?')
    parser.add_argument('-u', '--ldap_user', nargs='?')
    parser.add_argument('-p', '--ldap_pwd', nargs='?')
    parser.add_argument('-b', '--ldap_bind_dn', nargs='?')
    parser.add_argument('-w', '--ldap_group', nargs='?')
    parser.add_argument('-r', '--gitlab_url', nargs='?')
    parser.add_argument('-a', '--gitlab_apikey', nargs='?')
    parser.add_argument('-g', '--gitlab_group', nargs='?')
    parser.add_argument('-l', '--gitlab_access_level', nargs='?')
    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    group = ldap2gitlab(args.server, args.ldap_user, args.ldap_pwd, args.ldap_bind_dn, args.ldap_group, args.gitlab_url, args.gitlab_apikey)
    parsed_json = json.loads(group.show_ad_group())
    data = parsed_json['entries']
    for item in data:
        for key, value in item['attributes'].items():
            id = group.show_member_id(value)
            add = group.add_member(id, args.gitlab_group, args.gitlab_access_level)
            if add['message'] == 'Already exists':
                group.edit_member(id, args.gitlab_group, args.gitlab_access_level)
