#!/bin/bash

cat << EOF | ldapadd -x -D "cn=Manager,dc=zhexinit,dc=com" -w 5ro39MrWoptFJyBb  -H ldap://ldap.zhexinit.com
dn: cn=$3,ou=$5,dc=zhexinit,dc=com
uid: $3
cn: $3
sn: $2
#givenName: $3
uidNumber: $8
gidNumber: 1000
displayName: $3
objectClass: posixAccount
objectClass: top
objectClass: person
objectClass: shadowAccount
objectClass: inetOrgPerson
objectClass: sambaSamAccount
gecos: $3
loginShell: /sbin/nologin
homeDirectory: /home/$3
userPassword: zhexinit.com
employeeNumber: $1
#homePhone: 0531-123456
#mobile: 15212345678
mail: $4
postalAddress: HangZhou
pwdPolicySubentry: cn=default,ou=ppolicy,dc=zhexinit,dc=com
pwdReset: TRUE
sambaSID: S-1-5-21-1144631128-2437640235-3610393127-$1
sambaNTPassword: zhexinit.com
o: $6
departmentNumber: $7

EOF
