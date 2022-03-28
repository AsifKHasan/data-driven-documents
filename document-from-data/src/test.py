#!/usr/bin/env python3

import ftplib
from pprint import pprint

# things we have
ftp = ftplib.FTP("ftp.spectrum-bd.biz")
ftp.login("spectrum@spectrum-bd.biz", "B@ngl@1427")

data = []
ftp.cwd('/photo/celloscope')
things_we_have = ftp.nlst()

things_we_need = [
    'photo__Ahmed.Nafis.Fuad.png', 'photo__Alif.Arfab.png', 'photo__Altaf.Hossain.png', 'photo__Amimul.Ahshan.Avi.png', 'photo__Amiya.Ahmed.png', 'photo__Anis.Bulbul.png', 'photo__Arnab.Basak.png', 'photo__Asif.Khan.Taj.png', 'photo__Farhana.Naz.png', 'photo__Kamrun.Nahar.png', 'photo__Khondoker.Tanvir.Hossain.png', 'photo__Laboni.Das.png', 'photo__Mainur.Rahman.png', 'photo__Maly.Mohsem.png', 'photo__Md.Azfar.Inan.png', 'photo__Md.Ehtesham-Ul-Haque.png', 'photo__MD.Fuad.Hasan.Chowdhury.png', 'photo__Md.Hafizur.Rahman.png', 'photo__Md.Jamal.Uddin.png', 'photo__Md.Kamruzzaman.Tanim.png', 'photo__Md.Shariar.Kabir.png', 'photo__Md.Tofiq.Akbar.png', 'photo__Mehedi.Hasan.png', 'photo__Mohammad.Ashraful.Islam.png', 'photo__Mohammad.Mashud.Karim.png', 'photo__Mohammed.Kowsar.Rahman.Bhuiyan.png', 'photo__Moshiur.Rahman.png', 'photo__Mst.Lutfunnahar.Lota.png', 'photo__Muhammad.Ashraf.Uddin.Bhuiyan.png', 'photo__Murshida.Mushfique.png', 'photo__Mushfika.Faria.png', 'photo__Naim.Reza.png', 'photo__Nasima.Aktar.png', 'photo__Shafayat.Ahmed.png', 'photo__Syed.Mostofa.Monsur.png', 'photo__Syed.Taslimur.Rahaman.png', 'photo__Umme.Rumman.Usha.png', 'photo__Wakib.Hasan.png'
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
