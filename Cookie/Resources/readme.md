Sayfayı incelerken, inspect aracılığıyla uygulamanın bizimle ilgili bazı durumları cookie üzerinden takip ettiğini fark ettik. Cookie değerleri arasında dikkat çeken şey, bir parametrenin MD5 ile hashlenmiş bir değer içermesiydi. Hash’i çözüp baktığımızda bunun “false” kelimesinin MD5 karşılığı olduğunu anladık. Bu parametrenin muhtemelen bir yetki veya erişim kontrolü amacıyla kullanıldığını fark edince, mantığını test etmek için değerini değiştirmeyi denedik. MD5 üzerinden “true” kelimesinin hash’ini ürettik ve cookie içindeki hashlenmiş “false” değerini hashlenmiş “true” ile değiştirdik. Sayfayı yenilediğimizde sistem cookie’ye tamamen güvendiği için yeni değeri geçerli saydı ve bu sayede flag görünür hâle geldi. Yani cookie içindeki basit bir boolean kontrolün hashlenmiş hâlini değiştirerek flag’i elde etmiş olduk.

Çözüm

Bu zafiyetin temel nedeni, güvenlikle ilgili bir kontrolün cookie içinde saklanması ve üstelik bunun herhangi bir sunucu doğrulaması olmadan işlenmesidir. MD5 gibi zayıf hashler de durumu daha kötü hâle getirir. Bunu engellemek için:
Yetki ve erişim kontrolleri asla client-side cookie üzerinden yapılmamalıdır.
Cookie’lerde kritik değerler saklanacaksa mutlaka imzalı (HMAC) veya JWT gibi doğrulanabilir token yapıları kullanılmalıdır.
MD5 gibi zayıf hash algoritmaları tamamen terk edilmeli, bunun yerine güçlü kriptografik algoritmalar kullanılmalıdır.
Cookie değerleri backend tarafından kontrol edilmeden hiçbir işlem yapılmamalıdır.
Güvenlik parametreleri kullanıcı tarafından değiştirilemeyecek şekilde server-side state mantığıyla yönetilmelidir.