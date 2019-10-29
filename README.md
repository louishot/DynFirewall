# DynFirewall
To help to protect servers from remote attacks  such as ssh service 3306 database services, or windows remote desktop.
for dynamically updating firewall whitelist based from DNS TXT record


- Use  
python firewall_update_linux.py ip.txt.example.com

- add this line to your iptables configure file  
`-A INPUT -m set --match-set trusted src -j ACCEPT`  
/etc/sysconfig/iptables

- if you want ipset create on startup please check [systemd-ipset](https://github.com/BroHui/systemd-ipset-service) by BroHui

# DNS TXT record guide:
you can add IPv4 address or subnet. if you want add multiple IP or subnets you can use ',' split, also you can add txt alone for per ip address/subnet 
- Example
host     type  record  
ip.txt   TXT   "1.1.1.1,2.2.2.2/32"  
ip.txt   TXT   "3.3.3.3"  
ip.txt   TXT   "4.4.4.0/24"  
