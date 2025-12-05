Dosya yükleme sayfasını incelerken, uygulamanın yüklenen dosyaların gerçek türünü doğrulamadığını ve yalnızca istemcinin gönderdiği Content-Type değerine güvendiğini fark ettik. Yani sunucu dosyanın gerçekten bir resim olup olmadığını kontrol etmiyor, yalnızca header’da “image/jpeg” yazmasına bakarak dosyayı kabul ediyordu. Bu davranış, dosya içeriğinin sunucu tarafında analiz edilmediğini gösterdiği için, zararlı bir betiğin (script) JPEG dosyası gibi gösterilerek yüklenebileceğini test etmeye karar verdik.

Bunun için /tmp dizini altında hazırladığımız dosyayı, normal bir resim yükleme isteğiymiş gibi MIME türünü spoof ederek gönderdik. İçeriği ne olursa olsun sunucunun Content-Type’a güvendiğini doğrulamak amacıyla, dosyayı “image/jpeg” olarak işaretleyip POST isteğiyle yükledik. Bu testi gerçekleştirmek için aşağıdaki curl komutunu kullandık:

curl -s -X POST \
  -F "uploaded=@/tmp/malicious_script.sh;type=image/jpeg" \
  -F "Upload=Upload" \
  "$(printf '%s' "http://x.x.x.x/index.php?page=upload")" \
  | grep 'flag'


Sunucu dosyanın MIME türünü yalnızca header üzerinden değerlendirdiği için yüklemeyi hiçbir kontrol yapmadan kabul etti ve dosyayı işlemden geçirerek yanıt içinde flag’i döndürdü. Böylece dosya yükleme fonksiyonunun, Content-Type’a tamamen güvendiği için zararlı dosyaları dahi sorunsuzca işlediğini ve bunun sonuç olarak flag’in elde edilmesine yol açtığını görmüş olduk.

Çözüm

Bu zafiyet, uygulamanın dosya türünü yalnızca istemci tarafından gönderilen Content-Type veya dosya uzantısına bakarak doğrulamasından kaynaklanır. Bunu önlemek için:
Content-Type ve dosya uzantıları asla güvenlik doğrulaması için kullanılmamalıdır. Dosyanın gerçek türü sunucu tarafında magic bytes/signature ile doğrulanmalıdır.
Yüklenen dosyalar webroot dışında depolanmalı veya bulunduğu klasörde script çalıştırma tamamen devre dışı bırakılmalıdır.
Kullanıcıdan gelen dosya adı korunmamalı; yüklenen dosyalar rastgele adlandırılarak güvenli bir formatta saklanmalıdır.
Sadece belirli dosya türlerine izin veren katı bir allowlist kullanılmalıdır.
Resim yüklemelerinde sunucu tarafında re-encode işlemi yapılarak dosya yeniden kaydedilmeli ve zararlı içerik tamamen temizlenmelidir.
Upload dizininde PHP/CGI çalıştırması devre dışı bırakılmalıdır (ör. Apache: php_admin_flag engine off).
Kötü amaçlı yüklemeleri tespit etmek için antivirüs veya heuristic analiz eklenmeli ve tüm upload işlemleri loglanmalıdır.
Dosya yükleme özelliği için rate-limit, kullanıcı doğrulaması ve kötü niyetli trafiğe karşı izleme yapılmalıdır.