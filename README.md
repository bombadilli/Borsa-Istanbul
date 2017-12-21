# Borsa-Istanbul

Program ile Borsa İstanbul tarafından günlük yayınlanan bülten verilerinin ( http://www.borsaistanbul.com/veriler/verileralt/hisse-senetleri-piyasasi-verileri/bulten-verileri ) adresinden indirilerek, yerelde bir SQLlite veritabanına yazılması sağlanmaktadır.

Programın çalıştırıldığı zaman 2015-12-01 tarihinden çalıştırıldığı güne kadar olan verileri zip formatında indirmekte, csv dosyalarını açarak veri tabanına işlemektedir. Veri tabanına işleme sırasında csv dosyada bulunan kolon isimleri içerisinde bulunan kolon isimleri içindeki boşluklar çıkarılarak veritabanına yeni kolon isimleri ile kayıt yapılmaktadır.

Ek bir tablo içerisinde geçmişte indirilmiş olan verilerin kayıtları tutulduğu için her defasında tekrar verileri indirmek yerine en son indirilen tarihten bu yana olan veriler indirilerek veri tabanına kaydedilmektedir. Bu şekilde main içerisinde bulunan fromdate parametresi ile oynanarak verilerin parçalı indirilmesi de mümkün. 

2015-12-01 tarihi Borsa-İstanbul tarafından verilerin csv formatında verilmeye başlanması nedeni ile seçilmiştir. bu tarihten önceki veriler excel formatında verildiği için ayrı bir çalışma yapılması gerekiyor. Fırsat bulunması veya yardım gelmesi durumunda bu konuda ilerleyen dönemde bir şeyler yapmayı hedefliyorum. 

yine verilerin okunması ve buradan çeşitli analizlerin yürütülmesi için de bir çalışma hedefliyorum. Biraz daha uzun vadede döviz kurları ve diğer yatırım/ekonomik araçları da buraya dahil etmeyi hedefliyorum.
