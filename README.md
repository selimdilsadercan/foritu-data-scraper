<div align="center">

[![Refresh Lessons](https://github.com/itu-helper/data-updater/actions/workflows/refresh_lessons.yml/badge.svg)](https://github.com/itu-helper/data-updater/actions/workflows/refresh_lessons.yml)
[![Refresh Course Plans](https://github.com/itu-helper/data-updater/actions/workflows/refresh_course_plans.yml/badge.svg)](https://github.com/itu-helper/data-updater/actions/workflows/refresh_course_plans.yml)
[![Refresh Courses](https://github.com/itu-helper/data-updater/actions/workflows/refresh_courses.yml/badge.svg)](https://github.com/itu-helper/data-updater/actions/workflows/refresh_courses.yml)
[![Refresh Misc](https://github.com/itu-helper/data-updater/actions/workflows/refresh_misc.yml/badge.svg)](https://github.com/itu-helper/data-updater/actions/workflows/refresh_misc.yml)

![GitHub repo size](https://img.shields.io/github/repo-size/itu-helper/data-updater?label=Repository%20Size&logo=github&style=flat-square)
![GitHub](https://img.shields.io/github/license/itu-helper/data-updater?label=License&style=flat-square)
![GitHub issues](https://img.shields.io/github/issues-raw/itu-helper/data-updater?label=Issues&style=flat-square)

# **ITU Helper**

</div>

<div align="left">
    <img src="https://raw.githubusercontent.com/itu-helper/home/main/images/logo.png" align="right"
     alt="ITU Helper Logo" width="180" height="180">
</div>
<div align="center">

_İTÜ'lüler için İTÜ'lülerden_

_ITU Helper_ İstanbul Teknik Üniversitesi öğrencilerine yardım etmek amacıyla ön şart görselleştirme, ders planı oluşturma ve resmi İTÜ sitelerini birleştirme gibi hizmetler sağlayan bir açık kaynaklı websitesidir.

_ITU Helper_'a [_bu adresten_](https://itu-helper.github.io/home/) ulaşabilirsiniz.

</div>
<br>
<br>
<br>

# **itu-helper/data-updater**

## **Ne İşe Yarar?**

_Github Actions_ kullanarak **Veri Yenileme Aralıkları** kısmında belirtilen aralıklarda, İTÜ'nün çeşitli sitelerinden ders planlarını ve programlarını okur ve [itu-helper/data](https://github.com/itu-helper/data) _repo_'suna _commit_ eder. Daha sonra, [itu-helper/sdk](https://github.com/itu-helper/sdk) _repo_'suyla veya manuel olarak bu datalara erişilebilirsiniz.

## **Veri Yenileme Aralıkları**

- **(00:04 - 02:49) 5 dk'de bir**: _Lesson_'lar güncellenir.
- **(02:55)**: Bina ve program kodları güncellenir.
- **(03:00)**:
  - **Pazartesileri**: _Course_'lar güncellenir.
  - **Salıları**: Ders Planları güncellenir.
- **(05:04 - 23:49) 5 dk'de bir**: _Lesson_'lar güncellenir.

> [!NOTE]
> _Lesson_'ların daha sık güncellenmesinin nedeni kontenjan verilerinin güncel tutulmasının gerekmesidir. _Course_'ların ve Ders Planlarının güncellendiği sırada _Lesson_'ların güncellenememsi _Github Actions_'da kullandığımız _Git Auto Commit_'in repo'da değişiklik olması durumda commit atamamasındandır.

## **Verilerin İsimlendirilmesi**

- **Dersler**
  - _MAT 281E_ → Course
  - _CRN: 22964, MAT 281E_ → Lesson
- **Ders Planları**
  - _Bilgisayar ve Bilişim Fakültesi_ → Faculty
  - _Yapay Zeka ve Veri Mühedisliği_ → Program
  - _2021-2022 / Güz Dönemi Öncesi_ → Iteration

## **Nasıl Kullanılır?**

Veriler otomatik olarak [Veri Yenileme Aralıkları](#veri-yenileme-aralıkları) bölümünde belirtilen saatlerde güncellenir. Manuel olarak çalıştırmak isterseniz, aşağıdaki kodu çalıştırın. `{SCRAP_TARGET}` yazan yere de, _scrap_'lenecek olan veriyi girin (`lesson`, `course`, `course_plan`, `misc`).

```console
python src/run.py -scrap_target {SCRAP_TARGET}
```

## **Toplanan Verilerden Nasıl Yararlanılır?**

Verilerden yararlanırken izleyebileceğiniz iki ana yol bulunmakta. İlk olarak, önerdiğimiz yöntem olan [itu-helper/sdk](https://github.com/itu-helper/sdk) _repo_'sunda bulunan SDK'mizden yararlanmanız. Diğer yöntem ise, verileri _HTTP request_ ile okumak. Bu yöntemin dezavantajı, okuduğunuz dosyalardan bağlantıları kendiniz oluşturmanız gerekmesi. Daha detaylı bilgi için, [itu-helper/sdk](https://github.com/itu-helper/sdk)'nin [HTTP request](https://github.com/itu-helper/sdk?tab=readme-ov-file#http-request) bölümüne bakabilirsiniz.

## **Bilinen Problemler**

### **1. Eksik Ders İsimleri**

Dersler (Course) _scrap_'lenirken kullanılan [sayfa](https://www.sis.itu.edu.tr/TR/ogrenci/lisans/ders-bilgileri/ders-bilgileri.php), bazı dersler için isim bulundurmuyor veya yanlış isim bulundurmuyor. Örneğin `YZV 311E` dersi için görünen ders adı `N`, başka sayfalarda `Veri Madenciliği` olarak görünmesine rağmen.
