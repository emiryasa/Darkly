Ana sayfanın alt kısmındaki yönlendirme linkine gittikten sonra sayfayı inspect ederek kaynak kodunu inceledik ve HTML içinde yorum satırı olarak bırakılmış iki kritik satır fark ettik. Bu satırlarda, sayfaya erişim için özel bir User-Agent ile gelinmesi gerektiği ve isteğin belirli bir Referer üzerinden yapılmasının zorunlu olduğu açıkça belirtiliyordu. Bu ipuçlarının tamamen istemci tarafından kontrol edilen HTTP header’larına dayandığını görünce, ilgili değerlerin sunucu tarafından doğrulanmadan kabul edildiğini test etmeye karar verdik.

Yorum satırındaki bilgiler doğrultusunda User-Agent değerini ft_bornToSec olarak, Referer header’ını ise https://www.nsa.gov/
 şeklinde ayarlayıp isteği manuel olarak yeniden gönderdik. Ayrıca uygulamanın kullandığı cookie değerinin de doğrudan kabul edildiğini görünce isteğe I_am_admin cookie’sini de ekledik. Tüm bu bilgilerle birlikte isteği göndermek için aşağıdaki curl komutunu kullandık:

k1m07s09% curl 'http://x.x.x.x/index.php?page=e43ad1fdc54babe674da7c7b8f0127bde61de3fbe01def7d00f151c2fcca6d1c' \
  -H 'User-Agent: ft_bornToSec' \
  -H 'Referer: https://www.nsa.gov/' \
  -H 'Cookie: I_am_admin=b326b5062b2f0e69046810717534cb09' \
  | grep -i 'Flag'

Sunucu bu sahte header ve cookie bilgilerini gerçekmiş gibi kabul ederek erişimi doğruladı ve normalde korunan sayfayı bize açtı. Bu şekilde yalnızca header sahteciliği yaparak korumayı geçebildik ve sunucunun döndürdüğü yanıtta yer alan flag’i doğrudan elde ettik. Yani erişim kontrolü tamamen HTTP header’larına ve kontrolsüz cookie değerlerine güvendiği için, hiçbir kimlik doğrulama olmadan yalnızca User-Agent, Referer ve cookie bilgilerini değiştirerek hedef sayfaya ulaşmayı başardık.

Çözüm

Bu tür bir zafiyet, uygulamanın erişim kontrolünü istemci tarafından değiştirilebilen HTTP header’larına bağlamasından kaynaklanır. Bunu engellemek için:
Güvenlik kararları asla User-Agent, Referer veya benzeri client-side header’lara göre verilmemelidir; bunlar saldırgan tarafından kolayca spoof edilebilir.
Erişim kontrolü mutlaka sunucu taraflı kimlik doğrulama ile yapılmalı, kullanıcıyı doğrulamak için session, token veya benzeri sağlam mekanizmalar kullanılmalıdır.
Rol ve kaynak bazlı yetkilendirme (authorization) kuralları uygulanmalı; yalnızca doğru kimliği doğrulanmış kullanıcıların ilgili sayfaya erişmesine izin verilmelidir.
HTTP header’ları yalnızca loglama, analitik veya kullanıcı deneyimi optimizasyonu amaçlı kullanılmalı, güvenlik kontrollerinin parçası olmamalıdır.
Tasarım aşamasında güvenlik göz önüne alınarak, güvenlik kontrollerinin istemci tarafında değil tamamen backend seviyesinde uygulanması sağlanmalıdır.