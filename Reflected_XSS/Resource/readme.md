Sayfayı incelerken page=media endpoint’inin src parametresindeki girdiyi doğrudan yansıttığını fark ettik. İlk olarak şu URL'ye gittik:
http://X.X.X.X/?page=media&src=nsa
Bu sayfada NSA logosu görünüyordu ve görüntünün kaynağını kontrol ettiğimizde src parametresinin doğrudan HTML içinde kullanıldığını teyit ettik. Bu davranış, kullanıcı girdisinin filtrelenmediğini gösteriyordu. Ardından aynı parametreye HTML/JS yerleştirerek Reflected XSS denemesi yaptık. Normal script yüklemeyi denediğimizde:
http://x.x.x.x/index.php?page=media&src=data:text/html,<script>alert("xss")</script>
tarayıcıda belirli scriptleri çalıştırabildiğimizi gördük. Fakat aynı payload’ı Base64 formatında encode edip data: URI içerisine yerleştirdiğimizde bize flagi verdi
http://X.X.X.X/index.php?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgieHNzIik8L3NjcmlwdD4=
Bu URL’ye girdiğimiz anda tarayıcı Base64’ü decode etti ve HTML/JS’yi parse ederek scripti çalıştırdı. Böylece, site üzerinde tarayıcının bağlamında çalışan bir JavaScript kodu elde etmiş olduk.

Neden Sadece Base64 ile Çalıştı?

Bunun sebebi, uygulamanın data: URI’lerinde saf HTML içerik yerine Base64 beklemesiydi. “Normal” HTML payload’ı verdiğimizde tarayıcı veya uygulama tarafından karakterlerin bozulması, özel karakterlerin filtrelenmesi veya encoding çakışması oluştu. Ancak Base64 versiyonu tamamen güvenli bir karakter setinden oluştuğu için filtrelere takılmadı ve uygulama bunu doğrudan tarayıcıya iletti. Tarayıcı da data:text/html;base64, formatını gördüğünde decode edip HTML olarak çalıştırdı. Yani Base64, linkin şüpheli görünmemesi ve karakterlerin bozulmaması için gerekliydi; böylece script sorunsuz yürütüldü.
Sonuç olarak, src parametresine data: URI üzerinden Base64 kodlu HTML/JS enjekte ederek kullanıcı tarayıcısında Reflected XSS elde ettik. Payload’ın çalıştığına dair kanıt olarak alert penceresi görüntülenmiştir.

Çözüm

Bu zafiyet, geliştiricinin medya kaynağı parametresini hiçbir kontrol yapmadan HTML’e yerleştirmesi ve zararlı içeriklerin data: URI formatıyla bile kabul edilmesine izin vermesinden kaynaklanır. Bunu engellemek için:

1. data: URI’larını devre dışı bırakın veya sıkı şekilde doğrulayın.
Sadece belirli dosya türleri, yalnızca sunucu tarafında tanımlı medya ID’leri veya whitelist’lenmiş URL şemaları kabul edilmelidir.
2. Kullanıcı girdisini normalize edin ve doğrulayın.
src gibi HTML attribute içinde kullanılan değerler asla ham şekilde sayfaya yazılmamalı, yalnızca izin verilen formatlarda olmalıdır.
3. Bağlamsal output encoding kullanın.
HTML attribute içerisine kullanıcı girdisi gömülüyorsa uygun escaping yapılmalıdır.
4. Güvenlik başlıklarını uygulayın.
CSP kullanılarak inline scriptlerin çalışması engellenebilir, data: kaynakları tamamen yasaklanabilir.
X-Content-Type-Options: nosniff gibi başlıklar da etkili olur.
5. Untrusted HTML içeriklerini sayfaya enjekte etmeyin.
Gerekliyse sandboxed iframe kullanılmalı ve script çalıştırma izinleri kaldırılmalıdır.
6. Medya parametreleri için whitelist uygulayın.
Kullanıcıya tam URL girdisi değil, sadece sunucu tarafında doğrulanan medya referansları verilmelidir.