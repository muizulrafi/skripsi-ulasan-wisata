from playwright.sync_api import sync_playwright
import pandas as pd
import time
import re
import os

data = []

def get_lat_long(url):
    try:
        coords = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
        if coords:
            return coords.group(1), coords.group(2)
    except:
        pass
    return "", ""

def scrape_google_maps(url, nama_tempat):
    with sync_playwright() as p:
        # === DIUBAH: headless=True agar bisa jalan di server GitHub Actions ===
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
            ]
        )
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        page.goto(url)
        time.sleep(5)

        # ambil alamat
        try:
            alamat = page.locator('button[data-item-id="address"]').inner_text()
        except:
            alamat = ""

        # ambil koordinat
        time.sleep(5)
        current_url = page.url
        lat, long = get_lat_long(current_url)

        # klik tab review
        try:
            page.locator('button:has-text("ulasan")').first.click()
            time.sleep(5)
        except:
            try:
                page.locator('button:has-text("reviews")').first.click()
                time.sleep(5)
            except:
                print(f"Tidak menemukan tombol review: {nama_tempat}")

        # scroll dalam panel review
        for _ in range(30):
            page.mouse.wheel(0, 5000)
            time.sleep(2)

        reviews = page.query_selector_all('div.jftiEf')

        for r in reviews:
            try:
                text = r.query_selector('.wiI7pd').inner_text()
            except:
                text = ""

            try:
                rating = r.query_selector('.kvMYJc').get_attribute("aria-label")
            except:
                rating = ""

            try:
                waktu = r.query_selector('.rsqaWe').inner_text()
            except:
                waktu = ""

            data.append({
                "nama_tempat": nama_tempat,
                "alamat": alamat,
                "latitude": lat,
                "longitude": long,
                "review": text,
                "rating": rating,
                "waktu_review": waktu
            })

        browser.close()


# LIST TEMPAT
tempat_wisata = [
    ("Pantai Istana Presiden Pelabuhanratu", "https://www.google.com/maps/place/Pantai+Istana+Presiden+Pelabuhanratu/@-6.9804283,106.5235143,1471m/data=!3m1!1e3!4m10!1m2!2m1!1swisata+dekat+kecamatan+pelabuhanratu!3m6!1s0x2e6827f17a026b35:0x2d7c0d02e8d7d851!8m2!3d-6.9804283!4d106.5330415!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVJDT1dWWU0zWkJSUkFC4AEA-gEECAAQLw!16s%2Fg%2F11dfwz9100?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Wisata Alam Pantai Sukawayana", "https://www.google.com/maps/place/Wisata+Alam+Pantai+Sukawayana/@-6.9655912,106.5041528,1471m/data=!3m1!1e3!4m10!1m2!2m1!1swisata+dekat+kecamatan+pelabuhanratu!3m6!1s0x2e4283ea86358043:0x7a2424a904ef8993!8m2!3d-6.9655912!4d106.51368!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVJpYjJGeVYzUkJSUkFC4AEA-gEECAAQRQ!16s%2Fg%2F11j83qz2jy?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Pantai Citepus Sukabumi","https://www.google.com/maps/place/Pantai+Citepus+Sukabumi/@-6.9702815,106.5103845,1471m/data=!3m1!1e3!4m10!1m2!2m1!1swisata+dekat+kecamatan+pelabuhanratu!3m6!1s0x2e429d5c130f0ec5:0x8723773d2057b8ab!8m2!3d-6.9702815!4d106.5199117!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVVI0WjNGNk0yWkJFQUXgAQD6AQQIABAp!16s%2Fg%2F11q4bhq1sc?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Pantai Batu Bintang","https://www.google.com/maps/place/Pantai+Batu+Bintang/@-7.0206327,106.5304302,1471m/data=!3m1!1e3!4m10!1m2!2m1!1swisata+dekat+kecamatan+pelabuhanratu!3m6!1s0x2e682764a64f0907:0x7887beb38bda667b!8m2!3d-7.0206327!4d106.5399574!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgFEQ2k5RFFVbFJRVU52WkVOb2RIbGpSamx2VDJva2RWRnFUWGhoYld4eFl6SnZORlZVU25GVU1uaEdaRmRTYlZSV1JSQULgAQD6AQQIDxA8!16s%2Fg%2F11ddxz7lyh?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Pantai buffalo","https://www.google.com/maps/place/Pantai+buffalo/@-7.0046609,106.5332972,1471m/data=!3m1!1e3!4m10!1m2!2m1!1swisata+dekat+kecamatan+pelabuhanratu!3m6!1s0x2e6827ea2f2211bd:0xd2d44b2c3c7f21ae!8m2!3d-7.0046609!4d106.5428244!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgFEQ2k5RFFVbFJRVU52WkVOb2RIbGpSamx2VDJ4Sk5GRlhWVFZWYkRsWVpIcHNORkY2VGtSV2JFWndXbXhzUmsxWVl4QULgAQD6AQQIABAh!16s%2Fg%2F11ssz3mmyg?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Taman Bunga Pelabuhan Ratu","https://www.google.com/maps/place/Taman+Bunga+Pelabuhan+Ratu/@-6.9800499,106.5384153,1471m/data=!3m1!1e3!4m10!1m2!2m1!1swisata+dekat+kecamatan+pelabuhanratu!3m6!1s0x2e6827e4f9691b5f:0xe37e356cd2048885!8m2!3d-6.9800499!4d106.5479425!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVJ1YTA1VWVUSm5SUkFC4AEA-gEECAAQFw!16s%2Fg%2F11hy_zdwx7?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Taman Citepus (Ruang Terbuka Hijau) RTH","https://www.google.com/maps/place/Taman+Citepus+(Ruang+Terbuka+Hijau)+RTH/@-6.9757459,106.5187212,1471m/data=!3m1!1e3!4m10!1m2!2m1!1swisata+dekat+kecamatan+pelabuhanratu!3m6!1s0x2e429dabff98d0a3:0x2f26f7ad3ecc9b00!8m2!3d-6.9757459!4d106.5282484!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVU5rY0V0MWFXRjNFQUXgAQD6AQQIABAZ!16s%2Fg%2F11g0j45cl4?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Pantai Pelabuhan Ratu","https://www.google.com/maps/place/Pantai+Pelabuhan+Ratu/@-6.9757981,106.5193373,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e429d50d71b837f:0xc060a6b36fff085d!8m2!3d-6.9757981!4d106.5288645!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVVJsYkhJMlowaG5FQUXgAQD6AQQIABA5!16s%2Fg%2F11hcys2__8?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Smile hill Pelabuhan Ratu","https://www.google.com/maps/place/Bukit+Senyum+Pelabuhan+Ratu/@-6.9757459,106.5187212,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e6827fa247a24e9:0xc77dae165223adf0!8m2!3d-6.9741182!4d106.5425818!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEjQ2haRFNVaE5NRzluUzBWSlEwRm5UVU4zZVMxeGJWWkJFQUXgAQD6AQQIABBF!16s%2Fg%2F11g72f6pbr?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Pantai Karang Sari","https://www.google.com/maps/place/Pantai+Karang+Sari/@-6.9820503,106.5310902,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e6827f6b51e7215:0xf2c3635a085c43dd!8m2!3d-6.9820503!4d106.5406174!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5UVU52TWpkeFRtZFJSUkFC4AEA-gEECGwQLQ!16s%2Fg%2F11c1mzvwtj?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("i-Pe Beach Pelabuhanratu","https://www.google.com/maps/place/i-Pe+Beach+Pelabuhanratu/@-6.9757981,106.5193373,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e429dc80734f0df:0xf24492c34d4f8926!8m2!3d-6.9801481!4d106.5328618!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVU5TYzE5dWNrNW5FQUXgAQD6AQQIABA6!16s%2Fg%2F11fqtv5y0k?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Pantai Twenty Cipatuguran","https://www.google.com/maps/place/Pantai+Twenty+Cipatuguran/@-7.0104574,106.5308756,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e6827835c20659b:0xcd328d4365a54602!8m2!3d-7.0104574!4d106.5404028!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVU5xYkdRMk1rUlJFQUXgAQD6AQQIABA3!16s%2Fg%2F11lx0kdgpr?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Pantai Gopalo","https://www.google.com/maps/place/Pantai+Gopalo/@-7.0028326,106.5321359,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e682700563755f3:0xe1c188c527c94515!8m2!3d-7.0028326!4d106.5416631!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVVJrTlhWZk1GZDNFQUXgAQD6AQQIABA5!16s%2Fg%2F11vqqyb6n6?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Pantai Kandita","https://www.google.com/maps/place/Pantai+Kandita/@-6.9846541,106.5333459,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e68270019fd8aa3:0x2d212f0481ca4b13!8m2!3d-6.9832869!4d106.5411592!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgFEQ2k5RFFVbFJRVU52WkVOb2RIbGpSamx2VDJKV09YWk1ka1ZSVFhkUWFUVlRXbFJvVkVkV01IZHZZbE51VFhkWVFBQULgAQD6AQQIABAf!16s%2Fg%2F11vr7pr1m_?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Situ Rawa Kalong","https://www.google.com/maps/place/Situ+Rawa+Kalong/@-6.9963507,106.534164,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e68278faa01db01:0xb695d6e44377a945!8m2!3d-6.9963507!4d106.5436912!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVJOYTFveVZtdG5SUkFC4AEA-gEECAAQEw!16s%2Fg%2F11gbg2gdwm?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Ilove Palabuhanratu","https://www.google.com/maps/place/Ilove+Palabuhanratu/@-6.9973042,106.5470379,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e682753573969df:0x7eae401b1c86eb86!8m2!3d-6.9973042!4d106.5565651!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEjQ2haRFNVaE5NRzluUzBWSlEwRm5UVU40Vm5oUVoyZG5FQUXgAQD6AQQIABAY!16s%2Fg%2F11j3xfw4p6?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Taman Bunga Gunung Sumping","https://www.google.com/maps/place/Taman+Bunga+Gunung+Sumping/@-6.9794898,106.5382497,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e6827efa3e46851:0x47bd8828586f79ef!8m2!3d-6.9794898!4d106.5477769!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgEJY2l0eV9wYXJrmgFEQ2k5RFFVbFJRVU52WkVOb2RIbGpSamx2VDJzNVJrMHpWa0pTVkZWMFVrUlZlV0ZHUW10Tk0yaFZURlZXYlZReFJSQULgAQD6AQQIABA9!16s%2Fg%2F11c0pz7ggq?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Saung Bintang Katineung, wisata pantai, air dan kuliner","https://www.google.com/maps/place/Saung+Bintang+Katineung,+wisata+pantai,+air+dan+kuliner/@-7.0190344,106.5318328,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e68272fd9ad1f03:0xf236af584e6aa2e6!8m2!3d-7.0190344!4d106.54136!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVVJQZDA5Mk5XY25FQUXgAQD6AQQIABAu!16s%2Fg%2F11p01yy5l1?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Dermaga Karang Sari Pelabuhanratu","https://www.google.com/maps/place/Dermaga+Karang+Sari+Pelabuhanratu/@-6.9829183,106.5302345,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e6827f4c252af97:0xfb5e68c8c99be65e!8m2!3d-6.9829183!4d106.5397617!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVJrYkhOMVJYbEJSUkFC4AEA-gEECAAQGg!16s%2Fg%2F11k52ngtpd?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Pantai Cipatuguran Palabuhanratu","https://www.google.com/maps/place/Pantai+Cipatuguran+Palabuhanratu/@-7.0041654,106.5394698,735m/data=!3m2!1e3!4b1!4m6!3m5!1s0x2e6827c5967fcfc3:0x2b743d8a3465ce33!8m2!3d-7.0041707!4d106.5420447!16s%2Fg%2F11v5_yky40?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Hidden Gems Pelabuhanratu","https://www.google.com/maps/place/Hidden+Gems+Pelabuhanratu/@-6.9808003,106.5267779,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e68276ff3794cc9:0xa6ef1806c118ca65!8m2!3d-6.9808003!4d106.5363051!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEjQ2haRFNVaE5NRzluUzBWSlEwRm5UVU5aVlhkUGJWcG5FQUXgAQD6AQQIABAn!16s%2Fg%2F11l6lm3bv1?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Goa Karang Pamulang","https://www.google.com/maps/place/Goa+Karang+Pamulang/@-6.9829183,106.5302345,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e68278957a2d117:0x4623cb1456ce0f9f!8m2!3d-6.9808326!4d106.5365371!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgEEcGFya5oBI0NoWkRTVWhOTUc5blMwVkpRMEZuU1VOUWFXTnBRbEYzRUFF4AEA-gEECAAQKw!16s%2Fg%2F11g0g_8y83?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Pantai kampung perahu jayanti","https://www.google.com/maps/place/Pantai+kampung+perahu+jayanti/@-7.0184757,106.5384616,735m/data=!3m2!1e3!4b1!4m6!3m5!1s0x2e68275ac0206687:0xc4a6838ae8fd6541!8m2!3d-7.018481!4d106.5410365!16s%2Fg%2F11t6pqwc3b?entry=ttu&g_ep=EgoyMDI2MDMzMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Muara Citepus Palabuhanratu","https://www.google.com/maps/place/Muara+Citepus+Palabuhanratu/@-6.9721883,106.5159515,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e429de874f66117:0x7222ce1d61305f70!8m2!3d-6.9721883!4d106.5254787!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVF5ZDBscVJEUkJSUkFC4AEA-gEECAAQLQ!16s%2Fg%2F11ghnyh45t?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Dermaga baru","https://www.google.com/maps/place/Dermaga+baru/@-6.9833106,106.5372791,735m/data=!3m2!1e3!4b1!4m6!3m5!1s0x2e682799ece68fbb:0x851c3d326959766!8m2!3d-6.9833159!4d106.539854!16s%2Fg%2F11rndj4gdj?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Pantai Citepus","https://www.google.com/maps/place/Pantai+Citepus/@-6.9776957,106.5208042,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e429d5743e4f645:0xfe7c7860376ba30f!8m2!3d-6.9776957!4d106.5303314!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgEFYmVhY2iaASNDaFpEU1VoTk1HOW5TMFZKUTBGblNVTnRlV0poZGtwbkVBReABAPoBBAgAEEY!16s%2Fg%2F11b6dp3k6r?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Jangilus Monument","https://www.google.com/maps/place/Patung+jangilus/@-6.9974842,106.5471295,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e6827978de143b9:0xbb54831702dedf71!8m2!3d-6.9974842!4d106.5566567!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgETaGlzdG9yaWNhbF9sYW5kbWFya5oBI0NoWkRTVWhOTUc5blMwVkpRMEZuU1VReU1HTTNkbFpCRUFF4AEA-gEECAAQRA!16s%2Fg%2F11f0wnrssm?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Pesanggrahan Tenjo Resmi Pelabuhan Ratu","https://www.google.com/maps/place/Pesanggrahan+Tenjo+Resmi+Pelabuhan+Ratu/@-6.9798259,106.5237724,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e429d58406893db:0x8d64c29db6da63fa!8m2!3d-6.9798259!4d106.5332996!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgETaGlzdG9yaWNhbF9sYW5kbWFya5oBI0NoWkRTVWhOTUc5blMwVkpRMEZuVFVSQk0yRlBVVmRSRUFF4AEA-gEECAAQQw!16s%2Fg%2F11clwm9mq_?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Lapang Cangehgar Pelabuhanratu","https://www.google.com/maps/place/Lapang+Cangehgar+Pelabuhanratu/@-6.9927301,106.5483274,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e682792462afe9f:0x5e323cd356f530a5!8m2!3d-6.9927301!4d106.5578546!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgEJY2l0eV9wYXJrmgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVJhZVhKNmF6bEJSUkFC4AEA-gEECCcQPg!16s%2Fg%2F11g0hdr3qf?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Alun - Alun Palabuhanratu","https://www.google.com/maps/place/Alun+-+Alun+Palabuhanratu/@-6.988354,106.5413627,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e6827fad2961901:0xb3f64f3162c50716!8m2!3d-6.988354!4d106.5508899!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgEGZ2FyZGVumgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5UVU5CWjNZemJuTlJSUkFC4AEA-gEECAAQNw!16s%2Fg%2F11c1s2js2f?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("ALUN ALUN GADOBANGKONG","https://www.google.com/maps/place/ALUN+ALUN+GADOBANGKONG/@-6.9846541,106.5333459,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e6827870d11f1b1:0x177c4d281136683d!8m2!3d-6.9846541!4d106.5428731!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgEJY2l0eV9wYXJrmgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVVJFYmpobVprdEJFQUXgAQD6AQQIABAs!16s%2Fg%2F11vcrnqd_9?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Taman Tenjo Resmi","https://www.google.com/maps/place/Taman+Tenjo+Resmi/@-6.9797091,106.5427574,735m/data=!3m2!1e3!4b1!4m6!3m5!1s0x2e6827efcf60ec55:0x32dad7ef2fd26ee6!8m2!3d-6.9797144!4d106.5476283!16s%2Fg%2F11c1n763gz?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Waterpark Citepus Pelabuhanratu","https://www.google.com/maps/place/Waterpark+Citepus+Pelabuhanratu/@-6.9771,106.5213595,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e429db598a9d657:0xbe55ae98dc7b3aab!8m2!3d-6.9771!4d106.5308867!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgEKd2F0ZXJfcGFya5oBI0NoWkRTVWhOTUc5blMwVkpRMEZuU1VSQ05qaFVMV05CRUFF4AEA-gEECAAQHw!16s%2Fg%2F11g8v9k4_f?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Taman Bappeda","https://www.google.com/maps/place/Taman+Bappeda/@-6.9820333,106.5469668,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e6827e98e16a819:0x7b317b74bafa5471!8m2!3d-6.9820333!4d106.556494!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgEJY2l0eV9wYXJrmgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVJVTTNWdVpqQkJSUkFC4AEA-gEECAAQRA!16s%2Fg%2F11g9qcvbx0?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("PANTAI CIBANGBAN","https://www.google.com/maps/place/PANTAI+CIBANGBAN/@-6.9592437,106.4148982,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e4284ba53f6e66d:0xfb767af56029f236!8m2!3d-6.9592437!4d106.4244254!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgESdG91cmlzdF9hdHRyYWN0aW9umgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVU5DT1MxaWJXUlJFQUXgAQD6AQQIABAx!16s%2Fg%2F11b_2vghtf?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
    ("Taman Kota Cangehgar Palabuhanratu","https://www.google.com/maps/place/Taman+Kota+Cangehgar+Palabuhanratu/@-6.9820333,106.5469668,1471m/data=!3m1!1e3!4m11!1m3!2m2!1swisata+dekat+kecamatan+pelabuhanratu!6e1!3m6!1s0x2e6827530496a26b:0x27ebd9f9804cfa95!8m2!3d-6.9926475!4d106.5589459!15sCiR3aXNhdGEgZGVrYXQga2VjYW1hdGFuIHBlbGFidWhhbnJhdHVaJiIkd2lzYXRhIGRla2F0IGtlY2FtYXRhbiBwZWxhYnVoYW5yYXR1kgEJY2l0eV9wYXJrmgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVVIxYlY5cUxVaEJFQUXgAQD6AQQIABAf!16s%2Fg%2F11g0kd1rgk?entry=ttu&g_ep=EgoyMDI2MDQwMS4wIKXMDSoASAFQAw%3D%3D"),
]

# =========================================================
# LOAD DATA LAMA (supaya ulasan baru ditambahkan, bukan ganti)
# =========================================================
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
save_path = os.path.join(base_dir, "data", "raw", "dataset_final.csv")

if os.path.exists(save_path):
    df_lama = pd.read_csv(save_path)
    ulasan_lama = set(
        df_lama['review'].dropna().str.strip().tolist()
    )
    print(f"Data lama ditemukan: {len(df_lama)} baris")
else:
    df_lama = pd.DataFrame()
    ulasan_lama = set()
    print("Belum ada data lama, mulai dari awal")

# =========================================================
# LOOP SCRAPING
# =========================================================
for nama, url in tempat_wisata:
    print(f"Scraping: {nama}")
    scrape_google_maps(url, nama)

# =========================================================
# FILTER: hanya simpan ulasan yang BARU (belum ada di dataset)
# =========================================================
data_baru = [
    d for d in data
    if str(d.get('review', '')).strip() not in ulasan_lama
    and str(d.get('review', '')).strip() != ''
]

print(f"\nUlasan baru ditemukan: {len(data_baru)}")

if data_baru:
    df_baru = pd.DataFrame(data_baru)
    df_gabung = pd.concat([df_lama, df_baru], ignore_index=True)
    df_gabung.to_csv(save_path, index=False)
    print(f"Berhasil ditambahkan! Total data sekarang: {len(df_gabung)} baris")
else:
    print("Tidak ada ulasan baru. Dataset tidak berubah.")
