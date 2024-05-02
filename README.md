# Basis Data B11

Tutor buat nambahin htmlnya:
1. pull main
2. git checkout -b namabranch
3. tambahin html di dalem folder `main/templates/namahtml.html`
4. push ke branch sendiri

<br>
Tutor nyambungin per page: 

- besok dah

<br>
JANGAN MIGRATE - kalo migrate dia bikin tabel aneh2
<br>

buat database ada testing ngefetch json di views, selanjutnya blom tau lagi cara nyambungin ke html

CARA SETTING PATH POSTGRESQL
- masuk ke C/program files/PostgreSQL/bin
- copy path
- buka env (search aja)
- pencet environment variable
- nanti muncul ada 2 kotak, yg atas sama bawah. cari variable Path dari kotak atas terus pencet
- trus pencet new
- paste path yg udh di copy tadi
- pencet ok sampe selesai

<br>

CARA AKSES DATABASE
```txt
langsung jalanin di terminal aja (harus udh setting path postgresql 16/bin di env device)

psql -h aws-0-ap-southeast-1.pooler.supabase.com -p 5432 -d postgres -U postgres.zlanhhaiuvfbjlkpfndl

pass : basisdatab11gacor

abistu \d buat ngecek tablenya (25 table total)
```