Login sayfasını analiz ederken giriş formunun hem kullanıcı adı hem de şifre parametrelerini doğrudan GET isteği üzerinden aldığını fark ettik. Bu yapı herhangi bir rate limit, IP engelleme veya CAPTCHA korumasına sahip olmadığı için kaba kuvvet (brute force) saldırılarına tamamen açıktı. Bu durumu test etmek amacıyla geniş bir kullanıcı adı listesi ve yaygın kullanılan şifrelerden oluşan bir parola listesi kullanarak Python ile bir brute force script’i hazırladık. Script, her kullanıcı adı–şifre kombinasyonu için sunucuya bir GET isteği gönderiyor, dönen HTML içinde hata belirteci olan “WrongAnswer.gif” görüntüsünü arıyor ve bu işaret yoksa girişin başarılı olduğunu kabul ediyordu. Bu yöntemle sistemin herhangi bir güvenlik kontrolü yapmadığını görerek doğru şifreyi bulduk, giriş yaptık ve ardından flag’e eriştik. Yani yalnızca sunucunun brute force korumalarının eksikliğinden yararlanarak login kısmını geçip flag’i elde ettik.

Çözüm
Bu tür bir zafiyet, giriş formunun herhangi bir brute force koruması olmadan kullanıcı isteklerini doğrudan işlemesinden kaynaklanır. Bunu engellemek için:
Rate limiting uygulanmalı (belirli sayıdan fazla hatalı denemeyi geçici olarak engellemek).
IP bazlı geçici ban veya gecikme (throttling) sistemleri kullanılmalı.
Kullanıcı adı ve şifre girişlerinde CAPTCHA veya benzeri insan doğrulama mekanizmaları eklenmeli.
Başarısız login denemeleri için her istek arasında yapay gecikme (sleep) uygulanmalı.
GET üzerinden kimlik bilgisi alınmamalı; login işlemi POST metoduna taşınmalı.
Çok bilinen default kullanıcı adları ve şifreler sistemde bulunmamalı, kullanıcılar ilk girişte zorunlu şifre değişikliğine yönlendirilmelidir.