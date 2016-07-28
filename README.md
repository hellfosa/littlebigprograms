# littlebigprograms
some python scripts and more

###################ldap2gitlab################# 

Скрипт для синхронизации пользователей в группе LDAP с группой в Gitlab. 
Использовать как:
python3 main.py -s "ldap_сервер" -u "ldap_user" -p "ldap_pwd" -w "ldap_group" -r "http://gitlab_url" -a "gitlab_apikey" -g "gitlab_group" -l "gitlab_accell_level" -b "ldap_binddn"

ldap_bindn - вводить в полном формате (к примеру "OU=users, DC=example, DC=com")
ldap_user - обязательно указывать с двумя \ 

Таким образом полная строчка будет выглядеть как:
python3 main.py -s ldap.example.com -u "EXAMPLE\\\admin" -p "admin_pass" -w "gitlab_users" -r "http://gitlab.example.com" -a "gitlab_api_key" -g "group_in_gitlab" -l 30 (или другой уровень привилегий, от 10 до 50) -b "OU=users, DC=example, DC=com"


Ограничения скрипта 


Скрипт не создает пользователей в Gitlab, и может добавить только уже существующих пользователей :(
