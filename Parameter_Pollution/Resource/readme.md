Survey kısmını incelerken, sayfanın bize sunduğu seçeneklerin yalnızca 1 ile 10 arasında olduğunu fark ettik. Inspect panelini açıp HTML yapısını incelediğimizde, seçeneklerin tamamen client-side tanımlandığını ve hiçbir şekilde sunucu tarafından sınırlandırılmadığını gördük. <select> elemanında listelenen değerler arasında flag’e giden mantığın saklı olduğundan şüphelenip yeni bir seçenek eklemeyi denedik. Kodda 10’a kadar seçenek vardı; biz de manuel olarak <option value="11">11</option> şeklinde bir seçenek daha ekledik. Daha sonra bu yeni seçeneği seçip formun otomatik olarak gönderilmesini sağladığımızda, sistem bu değeri hiç doğrulamadığı için 11’i geçerli bir input olarak işledi ve karşılığında flag’i üretti. Böylece yalnızca HTML drop-down listesine bir seçenek ekleyerek flag’i elde etmiş olduk.

Çözüm

Bu zafiyetin temel sebebi, kullanıcıdan gelen verinin hiçbir şekilde sunucu tarafında doğrulanmaması ve sınırların yalnızca client-side arayüzde belirlenmiş olmasıdır. Bu yöntemin kötüye kullanılmasını engellemek için:
Formlardan gelen değerler mutlaka server-side doğrulama ile kontrol edilmelidir.
Beklenen değer aralıkları (örn. 1–10) backend tarafından kesin olarak sınırlandırılmalıdır.
HTML üzerindeki seçeneklerin değil, sunucu tarafında kabul edilen parametrelerin belirleyici olması sağlanmalıdır.
Kullanıcı manipülasyonlarına karşı tüm inputlar için white-list yaklaşımı uygulanmalıdır.
Kritik işlemler asla sadece istemci tarafındaki form yapısına güvenerek tasarlanmamalıdır.