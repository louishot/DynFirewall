import sys,os
import dns.resolver

ipset_create_cmd = 'create {name} hash:net family inet hashsize 1024 maxelem 65536'
ipset_add_cmd = 'add {name} {subnet}'

#iptables configure
iptables_configure = '-A INPUT -m set --match-set %s src -j ACCEPT'

crontab = '* * * * * /usr/local/bin/managed_firewall'

def check_ipset_config():
    if not os.path.isfile('/etc/sysconfig/ipset'):
        os.system('echo "-A INPUT -m set --match-set %s src -j ACCEPT" >> /etc/sysconfig/ipset' % 'trusted')

def get_txt_by_domain(domain):
    try:
        print("Geting TXT record from domain %s" % domain)
        answers = dns.resolver.query(domain, 'TXT')
        txt = []
        for data in answers:
            if data:
                for txt_str in data.strings:
                    for str in txt_str.decode().split(","):
                        txt.append(str)

        print("Successful get TXT record from domain %s" % domain)

        return txt
    except Exception as errors:
        print(errors)
        print("Geting TXT record from domain %s failed" % domain)
        return ""




def update_firewall(ips):
    try:
        if isinstance(ips, list) and len(ips) > 0:
            trusted_list = os.popen("ipset list trusted").read()
            if not trusted_list:
                os.system("ipset create trusted hash:net")
            for ip in ips:
                if ip not in trusted_list:
                    status = os.system("ipset add trusted %s" % ip)
                    if status != 0:
                        print('added %s to trust list failed' % ip)
                    else:
                        print('add %s to trust list success' % ip)
                else:
                    print("%s it's already added" % ip)


    except Exception as errors:
        print(errors)
        print('Update failed')














try:
    if sys.argv[1]:
        update_firewall(get_txt_by_domain(sys.argv[1]))
        check_ipset_config()
except Exception as errors:
    print(errors)
    print("example: run google.com")
    print("example: run google.com")

