Sayfayı incelerken sosyal medya butonlarının linklerine göz atmak için inspect’i açtık. HTML içinde tanımlı olan bu linklerin statik olduğunu fark edince, link adreslerini manuel olarak değiştirmeyi denedik. Normalde bu tür butonlar sadece dış sitelere yönlendirme yapar, fakat burada ilginç biçimde link alanı istemcide (client-side) kontrol edilen bir değişkene bağlanmıştı. Biz de URL’yi kendi belirlediğimiz bir değere çevirdiğimizde sayfa beklenmedik şekilde farklı bir tepki verdi ve güncellenen URL üzerinden flag doğrulaması yapılarak çıktı üretildi. Böylece yalnızca inspect panelinde sosyal medya linklerinden herhangi birini düzenleyerek flag’i elde etmiş olduk. Yani basitçe link yönlendirmelerini manipüle ettik ve sistem bunu kontrol etmediği için flag görünür hâle geldi.

Çözüm

Bu tür bir zafiyetin oluşmasının nedeni, güvenlik açısından kritik bir kontrolün istemci tarafında bırakılmasıdır. Kullanıcı tarafında değiştirilebilen HTML veya JavaScript değişkenlerine güvenmemek gerekir. Bunu engellemek için:
Flag, doğrulama veya kritik veriler server-side doğrulama olmadan asla client tarafında tetiklenmemelidir.
Inspect ile değiştirilebilir HTML özellikleri (href, value, onclick vb.) hiçbir şekilde güvenlik mekanizmasının parçası olmamalıdır.
Herhangi bir parametre veya URL değişikliğinin sunucu tarafından tam doğrulamadan geçirilmesi sağlanmalıdır.
Hassas işlemler için backend doğrulaması, yetkilendirme kontrolleri ve açıkça kontrol edilen endpoint’ler kullanılmalıdır.