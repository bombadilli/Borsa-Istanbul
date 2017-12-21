import datetime
import requests
import zipfile
import pandas
import sqlite3


kokdizin = "http://www.borsaistanbul.com"
bulten_verileri_tablosu = "bultenverileri"
borsa_veritabani_yeri= "./veriler/borsaist.db"


def tablo_kolon_ismi_olustur(parametre_adi):
    """csv'den alınan başlıklardan veritabanı kolonları için isim 
    oluşturma"""
    import re
    regex = re.compile('[^a-zA-Z0-9 ]')
    parametre_adi= regex.sub('', parametre_adi)
    return parametre_adi.replace(" ", "_")

def kolon_isimlerini_degistir(df):
    new_column_names = {}
    for i in df.columns:
        new_column_names[i]= tablo_kolon_ismi_olustur(i)
    df.rename(columns = new_column_names, inplace = True)

def bulten_veri_url_olustur(tarih):
    """Verilen tarih için bulten verilerine erişim
    urlsini ve ilgili klasör ve dosya adını oluşturur"""
    #bultenverileriformati = "/data/thb/YYYY/AA/"
    #bultenverileri_dosya_formati= "thbYYYYAAGGS.zip"
    altdizin = "/data/thb/" + str(tarih.year)
    if tarih.month < 10:
        altdizin = altdizin + "/0" + str(tarih.month) + "/"
    else:
        altdizin = altdizin + "/" + str(tarih.month) + "/"
    dosyaadi = "thb" + str(tarih.year) 
    if tarih.month < 10:    
        dosyaadi += "0" + str(tarih.month)
    else:
        dosyaadi += str(tarih.month)
    if tarih.day <10:
        dosyaadi += "0"  + str(tarih.day)
    else:
        dosyaadi += str(tarih.day)
    zipdosyaadi = dosyaadi + "1.zip"
    csvdosyaadi = dosyaadi + "1.csv"
    url = kokdizin + altdizin + zipdosyaadi
    print (url)
    return url, zipdosyaadi, csvdosyaadi

def veri_al(tarih):
    url, zipdosyaadi,csvdosyaadi = bulten_veri_url_olustur(tarih)
    zipdosya = requests.get(url)
    status = zipdosya.status_code
    if status == 200:
        with open("./download/"+zipdosyaadi,'wb') as output:
            output.write(zipdosya.content)
        with zipfile.ZipFile("./download/"+ zipdosyaadi,'r') as zipdosya:
            zipdosya.extractall("./download/")
        with open ("./download/"+ csvdosyaadi,'r') as dosya:
            df = pandas.read_csv(dosya, header = 0, delimiter= ";", 
                                 skiprows= 0)
        df = df.drop(0)
    else :
        df= None
    return df, status

def baslangic_islemleri():
    conn = sqlite3.connect(borsa_veritabani_yeri)
    cur = conn.cursor()
    fromdate = datetime.date(2017,10,19)
    cur.execute("select name from sqlite_master where type = 'table'")
    tablolar = cur.fetchall()
    print (tablolar)
    if len(tablolar)==0 or ("bultenverileri" not in tablolar[0]):
        print (fromdate)
        df, status= veri_al(fromdate)
        kolon_isimlerini_degistir(df)
        df.to_sql("bultenverileri",conn, if_exists="append", index = False)
        cur.execute("create table 'alinan_veriler' (tarih date, durum integer)")
        date = (str(fromdate),1)
        cur.execute("insert into 'alinan_veriler'(tarih, durum) values (?,?)",
                    (date))
        conn.commit()
    cur.execute("select tarih from 'alinan_veriler'")
    alinmis_veriler = cur.fetchall()    
    return conn, cur, alinmis_veriler

def main():
    conn,cur, alinmis_veriler = baslangic_islemleri()
    #print (alinmis_veriler)
    bugun=datetime.date.today()
    date =max(alinmis_veriler)[0].split("-")
    fromdate = datetime.date(int(date[0]),int(date[1]),int(date[2]))
    fromdate = datetime.date(2015,12,1)
    while fromdate != bugun:
        islenen_tarih =(str(fromdate),)
        if (fromdate.weekday()) <5 and (islenen_tarih not in alinmis_veriler):#haftasonu değil ise
            print (islenen_tarih)
            df, status = veri_al(fromdate)
            if status == 200:
                kolon_isimlerini_degistir(df)
                df.to_sql("bultenverileri",conn, if_exists="append", index = False)
                dosya_url,zip_dosya_yeri, csv_dosya_adi = bulten_veri_url_olustur(fromdate)  
                cur.execute("insert into 'alinan_veriler'(tarih, durum) values (?, ?)",
                            ((islenen_tarih[0],1)))
                conn.commit()
                alinmis_veriler.append(islenen_tarih)
            else:
                cur.execute("insert into 'alinan_veriler'(tarih, durum) values (?, ?)",
                            ((islenen_tarih[0],0)))
                conn.commit()                
        fromdate+= datetime.timedelta(days=1)
        # Sonraki gune geç
    cur.close()


    conn.close()
    return

if __name__ == "__main__":
    main()
