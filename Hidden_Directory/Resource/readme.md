Robots.txt dosyasını incelemeye başladığımızda, normalde arama motorlarının indekslemesini engellemek için kullanılan bu dosyada ilgimizi çeken bir satır gördük: Disallow: /hidden. Bu ifade, dizinin arama motorlarından saklanmak istendiğini gösteriyordu ancak elbette bizim tarafımızdan manuel olarak ziyaret edilmesini engellemiyordu. Bu yüzden tarayıcıdan doğrudan /hidden dizinine girdiğimizde içeride çok sayıda dosya ile karşılaştık. Dosyalar tek tek elle kontrol edildiğinde zaman kaybettirdiği için küçük bir script yazarak dizin içindeki tüm dosyaları otomatik olarak dolaşacak bir tarama işlemi gerçekleştirdik. Script, dizindeki her dosyayı GET isteğiyle çekiyor, flag formatına benzeyen bir içerik bulduğunda bunu ayıklayıp bize gösteriyordu. Bu şekilde dizin yapısını gezerek flag’in yer aldığı dosyayı tespit ettik ve başarıyla elde ettik.

Çözüm:

Bu tür bir zafiyetin oluşmasının temel sebebi, gizli olduğu varsayılan bir dizinin robots.txt aracılığıyla istemeden ifşa edilmesidir. Robots.txt yalnızca arama motorlarına yönelik bir “rica” dosyasıdır ve güvenlik amacıyla kullanılmamalıdır. Bu durumu engellemek için:
Gizlenmesi gereken dizinler hiçbir şekilde robots.txt içinde belirtilmemeli ve doğrudan dış erişime kapatılmalıdır.
Dizinlere erişim sunucu seviyesinde Yetkilendirme (Authorization) veya Kimlik Doğrulama (Authentication) ile korunmalıdır.
Dışarıdan listelenmesi gerekmeyen dizinler için directory listing kapatılmalıdır.
Hassas içerikler asla client tarafına açık bir klasörde tutulmamalı; gerektiğinde backend üzerinden kontrollü servislerle sunulmalıdır.