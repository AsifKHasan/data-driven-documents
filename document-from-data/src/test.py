#!/usr/bin/env python3

import ftplib
from pprint import pprint

# things we have
ftp = ftplib.FTP("ftp.spectrum-bd.biz")
ftp.login("spectrum@spectrum-bd.biz", "B@ngl@1427")

data = []
ftp.cwd('/signature/')
things_we_have = ftp.nlst()

things_we_need = [
  'signature__Abdullah-Al-Hossain.Bin.Sarwar.png', 'signature__Asadul.Haque.png', 'signature__Asif.Yusuf.png', 'signature__Assaduzzaman.png', 'signature__Dipankar.Kumar.Biswas.png',
  'signature__Iqbal.Yusuf.png', 'signature__Md.Nasir.Uddin.png', 'signature__Md.Ahsan.Habib.Rocky.png', 'signature__Md.Atikur.Zaman.png', 'signature__Md.Faisal.Hossain.png',
  'signature__Md.Mijanur.Rahman.png', 'signature__Md.Nahidul.Islam.Siddique.png', 'signature__Md.Sohel.Rana.png', 'signature__Md.Yousuf.Ali.png', 'signature__Mir.Earfan.Elahi.png',
  'signature__Mohammad.Kamrul.Hasan.png', 'signature__Salman.Ahmed.Firoz.png', 'signature__Suday.Kumer.Ghosh.png', 'signature__Tanvir.Rahman.png', 'signature__Tufaha.Ashfaque.png',
  'signature__Alif.Arfab.png', 'signature__Altaf.Hossain.png', 'signature__Amimul.Ahshan.Avi.png', 'signature__Amiya.Ahmed.png', 'signature__Anis.Bulbul.png', 'signature__Arnab.Basak.png',
  'signature__Asif.Khan.Taj.png', 'signature__Farhana.Naz.png', 'signature__Kamrun.Nahar.png', 'signature__Khondoker.Tanvir.Hossain.png', 'signature__Laboni.Das.png',
  'signature__Mainur.Rahman.png', 'signature__Maly.Mohsem.png', 'signature__Md.Azfar.Inan.png', 'signature__Md.Ehtesham-Ul-Haque.png', 'signature__MD.Fuad.Hasan.Chowdhury.png',
  'signature__Md.Hafizur.Rahman.png', 'signature__Md.Jamal.Uddin.png', 'signature__Md.Kamruzzaman.Tanim.png', 'signature__Md.Shariar.Kabir.png', 'signature__Md.Tofiq.Akbar.png',
  'signature__Mehedi.Hasan.png', 'signature__Mohammad.Ashraful.Islam.png', 'signature__Mohammad.Mashud.Karim.png', 'signature__Mohammed.Kowsar.Rahman.Bhuiyan.png',
  'signature__Moshiur.Rahman.png', 'signature__Mst.Lutfunnahar.Lota.png', 'signature__Muhammad.Ashraf.Uddin.Bhuiyan.png', 'signature__Murshida.Mushfique.png',
  'signature__Mushfika.Faria.png', 'signature__Nafis.Ahmed.Fuad.png', 'signature__Naim.Reza.png', 'signature__Nasima.Aktar.png', 'signature__Shafayat.Ahmed.png',
  'signature__Syed.Mostofa.Monsur.png', 'signature__Syed.Taslimur.Rahaman.png', 'signature__Umme.Rumman.Usha.png', 'signature__Wakib.Hasan.png', 'signature__Abdullah.Al.Maruf.png',
  'signature__Arun.Chakraborty.png', 'signature__Ayesha.Siddika.png', 'signature__Bony.Tasnim.png', 'signature__Gaffar.Khan.png', 'signature__Golam.Kibria.png',
  'signature__Imran.Hossain.Pappu.png', 'signature__Imran.Howlader.png', 'signature__Imtiaz.Mahmood.png', 'signature__Ishrat.Fatima.png', 'signature__Jahin.Khan.Shourov.png',
  'signature__Kamrul.Hasan.Komol.png', 'signature__Kazi.Noor.Jahan.png', 'signature__Mahmudul.Hasan.png', 'signature__Maria.Nurjahanara.Bhuiaya.png', 'signature__Md.Masud.Rana.Tuhin.png',
  'signature__Md.Mokaddes.Ali.png', 'signature__Md.Motaher.Hossain.png', 'signature__Md.Andalib.Emdad.png', 'signature__Md.Bodrul.Alam.png', 'signature__Md.Habibur.Rahman.Tusher.png',
  'signature__Md.Jahangir.Alam.png', 'signature__Md.Jahidul.Islam.png', 'signature__Md.Kamrul.Hasan.png', 'signature__Md.Kamruzzaman.png', 'signature__Md.Mainul.Islam.png',
  'signature__MD.Masud.Rana-(BDEX).png', 'signature__MD.Masud.Rana-(BDO).png', 'signature__Md.Mehrab.Hossain.png', 'signature__MD.Monirul.Islam.Tipu.png',
  'signature__Md.Moshiur.Rahman.png', 'signature__Md.Nazmul.Hasan.Masum.png', 'signature__Md.Noor-E-Alom.Siddique.png', 'signature__Md.Rafaz.Uddin.png', 'signature__Md.Rasel.Molla.png',
  'signature__Md.Sohan.Kabir.png', 'signature__Mokul.Arfan.Dito.png', 'signature__Nahid.Kamal.png', 'signature__Ommul.Khair.Musammat.Tahera.png', 'signature__Palash.Kumar.Sinha.png',
  'signature__Rafiqul.Islam.Reyad.png', 'signature__Rajib.Gupta.png', 'signature__Redwan.Al.Rashed.png', 'signature__Rezaul.Karim.png', 'signature__S.M.Al-Amin.png',
  'signature__Sadia.Yasmin.png', 'signature__Saikat.Barua.png', 'signature__Salma.Afrose.png', 'signature__Sathe.Khan.Majlish.png', 'signature__Sayada.Sultana.png',
  'signature__Saythe.Kaniz.Fatema.png', 'signature__Shahadat.Hossain.png', 'signature__Shanawaz.Durjoy.png', 'signature__Sharmin.Ferdowsi.Shormi.png', 'signature__Siam.Samad.Prantik.png',
  'signature__Sohag.Ali.png', 'signature__Sufia.Khanom.png', 'signature__Suman.Miah.png', 'signature__Sumshur.Rahman.png', 'signature__Suraiya.Binte.Ali.png',
  'signature__Swpan.Kumar.Shill.png', 'signature__Syed.Ahmad.Mahdi.png', 'signature__Syed.Ahmad.Rasul.png', 'signature__Tania.Akter.png', 'signature__Tanvir.Ahmed.png',
  'signature__Tauhidul.Islam.png', 'signature__Ziaul.Hoq.png', 'signature__Zillur.Rahman.png', 'signature__Abed.Bin.Hossain.png', 'signature__Ahmed.Saquib.png', 'signature__Hasib.Mahmud.png',
  'signature__Jumana.Ahmed.png', 'signature__Md.Faizul.Bari.png', 'signature__A.K.M.Rakibul.Hasan.png', 'signature__A.S.M.Estiuk.Sadick.png', 'signature__Aabid.Rahman.png',
  'signature__Abdur.Rab.Marjan.png', 'signature__Abdur.Rahman.png', 'signature__Abdur.Rahman.Sagor.png', 'signature__Abu.Muhammad.Rashed.Mujib.Noman.png',
  'signature__Adiat.Islam.Sahih.png', 'signature__Ahmed.Jahin.Akif.png', 'signature__Airin.Sultana.png', 'signature__Akeed.Anjum.png', 'signature__Anan.Aiman.Tuba.png',
  'signature__Aqib.Asifur.Rahman.png', 'signature__Ashish.Kumar.Das.png', 'signature__Asma.Ul.Husna.png', 'signature__Atiqur.Rahman.png', 'signature__Dipika.Debnath.png',
  'signature__Fahim.Shahriar.png', 'signature__Faius.Mojumder.Nahin.png', 'signature__Ferdous.Rahman.png', 'signature__G.M.Ataur.Rahman.png', 'signature__Hasib.Ahmed.Prince.png',
  'signature__Ibrahim.Ibna.Md.Liaquat.Ullah.png', 'signature__Joy.Kabiraj.png', 'signature__Jyoti.Basu.Chakma.png', 'signature__K.M.Zabir.Tarique.png',
  'signature__Kamrul.Islam.Sarek.png', 'signature__Karzon.Chowdhury.png', 'signature__Kazi.Rakibur.Rahman.png', 'signature__Khaja.Ajijul.Haque.(Mithu).png',
  'signature__Khandakar.Asif.Hasan.png', 'signature__Khandakar.Rashed.Hassan.png', 'signature__Lubna.Saha.png', 'signature__Mahim.Jahan.Mim.png', 'signature__Manzur.Alam.png',
  'signature__Md.Farhad.Bhuiyan.png', 'signature__Md.Abdullah.Al.Mamun.png', 'signature__Md.Ahsanur.Rahman.png', 'signature__Md.Al-Shahariar.png', 'signature__Md.Anamul.Haque.png',
  'signature__Md.Anisur.Rahman.png', 'signature__Md.Apon.Reza.png', 'signature__Md.Arifur.Rahman.Bhuiyan.png', 'signature__Md.Asgor.Ali.png', 'signature__Md.Asheq.Ullah.png',
  'signature__Md.Ashraful.Hossain.png', 'signature__Md.Atikul.Islam.png', 'signature__Md.Atiqur.Rahman.png', 'signature__Md.Azizul.Hakim.png', 'signature__Md.Ekramul.Bari.png',
  'signature__Md.Ferdous.Mahmud.png', 'signature__Md.Hasibur.Rahman.png', 'signature__Md.Humayun.Kabir.png', 'signature__Md.Ibrahim.Hossain.png', 'signature__Md.Ibrahim.Ullah.png',
  'signature__Md.Istiyak.Ahmed.Milon.png',   'signature__Md.Jakir.Hossain.png', 'signature__Md.Jubaer.Hossain.png', 'signature__Md.Kamruzzaman-(SECL).png',
  'signature__Md.Kaziul.Islam.png', 'signature__Md.Khalid.Saifullah.Gazi.png',  'signature__Md.Mahabub.Al-Islam.png', 'signature__Md.Mahasin.Alam.png', 'signature__Md.Mahmudul.Hasan.png',
  'signature__Md.Mashrurul.Hakim.png', 'signature__Md.Mazharul.Islam.png', 'signature__Md.Mobusshar.Islam.png', 'signature__Md.Mominul.Islam.png', 'signature__Md.Murshadul.Islam.png',
  'signature__Md.Murshid.Sarker.png', 'signature__Md.Najmul.Hasan.Sharon.png', 'signature__Md.Nazmul.Hasan.png', 'signature__Md.Nazmul.Hossain.png', 'signature__Md.Rabiul.Islam.png',
  'signature__Md.Raqibul.Islam.png', 'signature__Md.Rejuanul.Haque.png', 'signature__Md.Rejwan.ull.Alam.png', 'signature__Md.Rezaul.Islam.png', 'signature__Md.Rezaul.Karim.png',
  'signature__Md.Robiul.Awoul.png', 'signature__Md.Rokonuzzaman.png', 'signature__Md.Saidur.Rahman.Shamim.png', 'signature__Md.Saiful.Islam.png', 'signature__Md.Sajal.Biswas.png',
  'signature__Md.Salman.Hossen.png', 'signature__Md.Samim.Hosen.png', 'signature__Md.Sayeem.Khan.png', 'signature__Md.Shahin.Sheikh.png', 'signature__Md.Sharafat.Hossain.Kamal.png',
  'signature__Md.Shariful.Islam.png', 'signature__Md.Shidratul.Islam.Rifat.png', 'signature__Md.Sirajul.Islam.png', 'signature__Md.Tuhin.Reza.png', 'signature__Md.Zahidul.Islam.png',
  'signature__Miskatun.Nahar.png', 'signature__Mohammad.Main.Uddin.png', 'signature__Mohammad.Nazmul.Hasan.png', 'signature__Mohammad.Saiful.Islam.png',
  'signature__Mohammad.Shamsur.Rahman.png', 'signature__Monjur.Ahmed.png', 'signature__Muhammad.Aminur.Rahman.png', 'signature__Muhammad.Myanuddin.png',
  'signature__Muhsinur.Rahman.Chowdhury.png', 'signature__Nur-E-Asma.Tabassum.png', 'signature__Nusrat.Jahan.Mahmud.png', 'signature__Raihan.Ur.Rashid.png',
  'signature__Rajib.Chowdhury.png', 'signature__Rifat.Ara.Swarna.png', 'signature__Rishad.Ali.Mimo.png', 'signature__S.M.Azharul.Islam.png', 'signature__Sagar.Saha.png',
  'signature__Saiful.Islam.png', 'signature__Saiful.Islam.Sonnet.png', 'signature__Sakib.Ibn.Abdullah.png', 'signature__Saleh.Ahammed.png', 'signature__Samin.Tawsib.Tanjim.png',
  'signature__Sanjoy.Kumar.Saha.png', 'signature__Sanmoon.Yasmin.png', 'signature__Sarkar.Abul.Kalam.Azad.png', 'signature__Sayeda.Fatema.Ferdousi.png', 'signature__Sayeda.Tanjila.png',
  'signature__Shahida.Begum.png', 'signature__Shaikh.Tojibul.Islam.png', 'signature__Shajir.Uddin.Haider.png', 'signature__Shihan.Zaman.png', 'signature__Shohag.Hossain.png',
  'signature__Shuvo.Das.png', 'signature__SK.Maruf.Hosen.png', 'signature__Sonjoy.Kumar.png', 'signature__Soumen.Sikder.Shuvo.png', 'signature__Syed.Shah.Md.Adib.png',
  'signature__Tanmoy.Chandra.Dhar.png', 'signature__Tasnim.Kabir.Ratul.png', 'signature__Tridib.Biswas.png', 'signature__Arnab.Kumar.Ghosh.png', 'signature__Khairul.AN-AM.png',
  'signature__Md.Asif.Atick.png', 'signature__Md.Imtiaz.Morshed.Bin.Zaman.png', 'signature__Md.Monirul.Islam.png', 'signature__Md.Najib.Hasan.png',
  'signature__Saleh.Ahammed.Masum.Khan.png'
]

print(f"we need {len(things_we_need)} things")
print(f"we have {len(things_we_have)} things")

# things_we_have_correct = set(things_we_have).intersection(things_we_need)
# print(f"we have {len(things_we_have_correct)} correct things")
# pprint(things_we_have_correct)

# things_we_have_wrong = set(things_we_have) - set(things_we_need)
# print(f"we have {len(things_we_have_wrong)} extra/wrong things")
# pprint(things_we_have_wrong)

things_we_are_missing = set(things_we_need) - set(things_we_have)
print(f"we have {len(things_we_are_missing)} missing things")
pprint(things_we_are_missing)
