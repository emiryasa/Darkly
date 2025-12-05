Şifremi unuttum sayfasını incelerken form yapısında bir gariplik olduğunu fark ettik. Normalde kullanıcıdan e-posta adresi istenmesi gerekirken, sayfada görünmeyen bir hidden input bulunduğunu inspect üzerinden gördük:
<input type="hidden" name="mail" value="webmaster@borntosec.com" maxlength="15">.
Bu değer kullanıcıya gösterilmiyor olsa da, client-side üzerinde tamamen değiştirilebilir durumdaydı. Biz de bu gizli alanın değerini kendi belirlediğimiz bir e-posta ile değiştirdik ve formu submit ettik. Sunucu tarafında hiçbir doğrulama yapılmadığından bu değiştirilmiş veri doğrudan işlendi ve sistem, bu manipüle edilmiş mail parametresine karşılık olarak flag’i üretti. Yani yalnızca hidden input’un value değerini değiştirerek flag’e ulaşmış olduk.

Çözüm

Bu zafiyetin temel nedeni, gizli olduğu sanılan ancak aslında tamamen kullanıcı kontrolünde olan client-side bir input değerine güvenilmesidir. Bunu engellemek için:
Hidden input’lar asla güvenlik kontrolü amacıyla kullanılmamalıdır.
Formdan gelen tüm değerler mutlaka server-side doğrulama ile kontrol edilmelidir.
E-posta, kullanıcı ID’si gibi kritik alanlar kullanıcıdan bağımsız olarak sunucu tarafında belirlenmeli, Ön tarafta editable hâle getirilmemelidir.
Kullanıcı tarafından değiştirilebilecek HTML elementlerine (hidden, text, select vb.) güvenilmemeli, güvenlik tamamen backend’de uygulanmalıdır.
İşlem doğrulama aşamalarında zorunlu olarak yetkilendirme ve kimlik doğrulama kullanılmalıdır.