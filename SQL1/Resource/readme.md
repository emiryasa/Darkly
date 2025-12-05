Resim listeleme fonksiyonunun URL üzerinden aldığı parametreleri analiz ederken uygulamanın bu girdileri doğrudan SQL sorgularına eklediğini fark ettik. Parametre üzerinde basit bir UNION SELECT denemesi yaptığımızda uygulamanın sorguyu olduğu gibi çalıştırdığını ve hata vermeden SQL Injection’a açık olduğunu doğruladık. Bu davranışı kullanarak veritabanındaki tabloları keşfetmek için UNION SELECT ile information_schema.tables üzerinde sorgulama yaptık ve kullanılan tablo isimleri arasından list_images tablosunu bulduk. Ardından aynı yöntemi kullanarak list_images tablosundaki kolonları information_schema.columns üzerinden enumerate ettik ve tablonun id, url, title, comment kolonlarından oluştuğunu belirledik.

Bu noktadan sonra, tablo içeriğini görüntülemek için UNION SELECT içinde CONCAT fonksiyonuyla satır verilerini birleştirip uygulamanın çıktısında gösterilmesini sağladık. Bu işlemin ardından bir satırın comment kolonunda dikkat çekici bir MD5 hash’i tespit ettik. Açıklamada verilen ipuçlarına göre bu hash’in önce MD5 olarak çözülmesi, ardından çıkan kelimenin SHA-256 hash’inin alınması gerektiğini öğrendik. MD5 değerini çözdüğümüzde “albatroz” kelimesine ulaştık ve bu değerin SHA-256 çıktısını aldığımızda flag olarak kullanılan değeri elde ettik.


Sömürü sırasında kullandığımız örnek (sanitize edilmiş) UNION payload’ları aşağıdaki yapıdaydı:

-- Tabloları keşfetme
1 AND 1=0 UNION SELECT table_name, NULL 
FROM information_schema.tables 
WHERE table_schema = database()--

-- list_images kolonlarını bulma
1 AND 1=0 UNION SELECT column_name, NULL 
FROM information_schema.columns 
WHERE table_name = CHAR(108,105,115,116,95,105,109,97,103,101,115)--  (list images ASCII hali)

-- Tablo verisini çekme
1 UNION SELECT 1, CONCAT(id, url, title, comment) 
FROM list_images


Bu sorgular, uygulamanın kullanıcı girdisini hiçbir filtreleme veya doğrulama olmadan SQL sorgularına eklediğini ve UNION tabanlı injection’a tamamen açık olduğunu gösterdi. Böylece tabloları keşfedip kolonları enumerate ederek nihayetinde flag’e ulaşmış olduk.

Çözüm

Bu zafiyet, uygulamanın kullanıcı girdisini hiçbir kontrol uygulamadan SQL sorgularına eklemesinden kaynaklanır. Bunu engellemek için:

Hazırlanmış ifadeler (prepared statements) ve parametreli sorgular kullanılmalı; kullanıcı girdisi asla doğrudan sorgu metnine eklenmemelidir.
Veritabanı kullanıcısı minimum yetkilerle çalışmalı; gerekmediği sürece information_schema erişimi kapatılmalıdır.
Hassas ipuçları, hash'ler veya kritik bilgi içeren veriler doğrudan veritabanına kaydedilmemeli; zorunlu ise yavaş hash algoritmaları (bcrypt, Argon2) kullanılmalı.
WAF veya query-level filtering mekanizmaları ile UNION, INFORMATION_SCHEMA, CHAR() gibi tipik SQLi izleri tespit edilip engellenmelidir.
Uygulama genelinde giriş doğrulama (input validation), whitelist tabanlı kontroller ve güçlü çıktı kaçırma (output encoding) uygulanmalıdır.
Hatalar kullanıcıya ham olarak gösterilmemeli; ayrıntılı hata mesajları log’lara yazılmalı, istemci tarafında gizlenmelidir.
Kod incelemesi, penetration testler ve otomatik SAST/DAST araçlarıyla SQL Injection kontrolü periyodik olarak yapılmalıdır.