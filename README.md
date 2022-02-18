# my-own-cipher
Program dibuat dengan bahasa Python. Untuk antarmuka program, dibuat dengan dependensi PyQt5. Algoritma stream cipher ini dibuat dengan melakukan modifikasi terhadap RC4, yaitu dengan memodifikasi prosedur KSA dan menambahkan LFSR. Program dapat menerima pesan yang diketikkan dari papan ketik dan pesan berupa file sembarang (file teks maupun file biner)

Algoritma enkripsi stream cipher dilakukan dengan proses sebagai berikut:
- KSA
- PRGA
- LFSR 4-bit (sebanyak 8 kali)

KSA dibuat lebih kompleks dengan mengubah proses pengacakan (permutasi) nilai-nilai di dalam larik S berdasarkan kunci K.

Supaya dapat dilakukan LFSR 4-bit, angka desimal yang didapatkan dari PRGA akan diubah menjadi dalam bentuk biner 8-bit. Kemudian biner 8-bit tersebut akan dibagi menjadi 2 bagian, sehingga akan dimiliki 2 bilangan biner 4-bit. Masing-masing biner 4-bit tersebut akan dilakukan LFSR 4-bit sebanyak 8 kali. Kemudian, 2 bilangan biner 4-bit yang telah dilakukan LFSR 4-bit akan digabungkan kembali, kemudian dikonversi dalam bentuk string sebagai hasil enkripsinya.

Setelah selesai melakukan proses enkripsi (setelah melakukan LFSR 4-bit), algoritma dekripsi stream cipher dilakukan dengan proses sebagai berikut:
- LFSR 4-bit (sebanyak 7 kali) 
  - LFSR untuk input file
  - LFSR untuk input text
- KSA
- PRGA
  - PRGA untuk input file
  - PRGA untuk input text

Proses enkripsi dan dekripsi hampir sama, perbedaannya hanyalah di urutan melakukan LFSR 4-bit dan jumlah dilakukan LFSR 4-bit. Perbedaan PRGA / LFSR untuk input yang berbeda (file dan teks) juga tidak jauh berbeda, hanya pemrosesan dalam bentuk file membaca bentuk binary dari file tersebut sedangkan pemrosesan dalam bentuk teks langsung memproses string yang terdapat pada teks. 

Sehingga, dapat diringkas proses melakukan enkripsi dan dekripsi stream cipher adalah sebagai berikut:
- KSA
- PRGA
- LFSR 4-bit (sebanyak 8 kali)
- LFSR 4-bit (sebanyak 7 kali)
- KSA
- PRGA
