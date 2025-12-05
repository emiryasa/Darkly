Robots.txt dosyasını kontrol ettiğimizde, normalde arama motorlarından saklanmak istenen dizinlerin listelendiğini biliyorduk. Dosyanın içinde “/whatever” şeklinde bir yol görünce bu dizine erişmeyi denedik. Dizin içinde dikkat çeken bir dosya vardı: .htpasswd. Bu dosya genellikle temel HTTP kimlik doğrulaması için kullanılan kullanıcı adı–şifre hashlerini barındırır. Dosyayı indirip açtığımızda içeride şu satırı bulduk:
root:437394baff5aa33daa618be47b75cb49

Bu değerin bir hash olduğunu fark ettik ve hash türünü analiz edip uygun araçlarla çözümledik. Hash’i çözdüğümüzde root kullanıcısının gerçek şifresine ulaşmış olduk. Ardından admin paneline gidip kullanıcı adı root, parola olarak da deşifre ettiğimiz şifreyi girerek başarılı şekilde oturum açtık. Admin paneline giriş yaptıktan sonra sisteme erişim sağlandı ve flag’i alabildik. Yani robots.txt → whatever → .htpasswd → hash decode zincirini kullanarak flag’e ulaşmış olduk.

Çözüm

Bu zafiyet birkaç temel hata nedeniyle ortaya çıkar:
Gizli dizinlerin robots.txt içinde ifşa edilmesi
.htpasswd gibi kritik dosyaların indirilebilir şekilde sunucuda açık bırakılması
Hashlerin zayıf algoritmalarla veya kolay kırılabilir şekilde saklanması
Admin panelinin ekstra korumaya sahip olmaması