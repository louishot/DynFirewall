import sys,os
import dns.resolver
cmd_show = 'netsh advfirewall firewall show rule "Remote Desktop (TCP-In) by Auto Managed"'
cmd_add = 'netsh advfirewall firewall add rule name="Remote Desktop (TCP-In) by Auto Managed" protocol=TCP dir=in localport=3389 remoteip="{subnet}" service=any profile=any description="For foreign Windows editions" action=allow'
cmd_update = 'netsh advfirewall firewall set rule name="Remote Desktop (TCP-In) by Auto Managed" new remoteip="{subnet}"'
cmd_task = 'Schtasks /create /tn "Firewall_Update" /RU SYSTEM /sc daily /st 00:00 /RI 1 /K /DU 24:00 /tr "C:\Windows\system32\firewall_update.exe ip.txt.example.com"'



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


def update_firewall(IPs):
    try:
        os.popen("chcp 437")
        if isinstance(IPs, list) and len(IPs) > 0:
            ip_str = ",".join(str(i) for i in IPs)
            res = os.popen(cmd_update.format(subnet=ip_str)).readlines()
            if 'Ok.\n' in res:
                print("Updated rules to %s" % ip_str)
            else:
                print("Update rules failed")


    except Exception as errors:
        print(errors)
        print("Update rules failed")


def check_managed_rules():
    try:
        os.popen("chcp 437")
        res = os.popen(cmd_show).readlines()
        if 'No rules match the specified criteria.\n' in res:
            print("No managed rules found")
            print("Creating managed rules")
            res = os.popen(cmd_add.format(subnet="127.0.0.1")).readlines()
            if 'Ok.\n' in res:
                print("Created managed rules")
            else:
                print(res)
                print("Create managed rules failed")
        else:
            print("Found managed rules")
            print("Trying to update rules")

    except Exception as errors:
        print(errors)
        print("Check managed rules failed")










check_managed_rules()
try:
    if sys.argv[1]:
        update_firewall(get_txt_by_domain(sys.argv[1]))
except Exception as errors:
    print(errors)
    print("example: Example.exe google.com")
    print("example: Example.py google.com")




