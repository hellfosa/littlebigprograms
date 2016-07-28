# littlebigprograms
some python scripts and more

###################ldap2gitlab#################

Скрипт для синхронизации пользователей в группе LDAP с группой в Gitlab. 
Использовать как:
python3 main.py -s "ldap_сервер" -u "ldap_user" -p "ldap_pwd" -w "ldap_group" -r "http://gitlab_url" -a "gitlab_apikey" -g "gitlab_group" -l "gitlab_accell_level" -b "ldap_binddn"

ldap_bindn - вводить в полном формате (к примеру "OU=users, DC=example, DC=com")
