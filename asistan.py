import speech_recognition as sr
import os
import webbrowser
import time
import asyncio
import edge_tts
import pygame
import pyautogui
import datetime
import screen_brightness_control as sbc

# --- 1. AYARLAR VE LOG SİSTEMİ ---
VOICE = "tr-TR-AhmetNeural"
SORU_LOG_DOSYASI = "sorulan_sorular.txt"
pygame.mixer.init()

def jarvis_islem_merkezi(komut):
    komut = komut.lower()
    
    # Soru Kayıt Sistemi
    with open(SORU_LOG_DOSYASI, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}] {komut}\n")

    # --- SİSTEM & DONANIM KOMUTLARI ---
    if "parlaklık" in komut or "parlaklığı" in komut:
        try:
            mevcut = sbc.get_brightness()[0]
            if "arttır" in komut or "yükselt" in komut:
                sbc.set_brightness(min(mevcut + 15, 100))
                metni_seslendir("Parlaklık artırıldı.")
            elif "azalt" in komut or "düşür" in komut:
                sbc.set_brightness(max(mevcut - 15, 0))
                metni_seslendir("Parlaklık azaltıldı.")
            else:
                sayi = [int(s) for s in komut.split() if s.isdigit()]
                if sayi: sbc.set_brightness(sayi[0])
                metni_seslendir("Parlaklık ayarlandı.")
            return True
        except: return False

    elif "ekran görüntüsü al" in komut:
        metni_seslendir("Ekran görüntüsü alınıyor.")
        tarih = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pyautogui.screenshot(f"ekran_{tarih}.png")
        return True

    # --- UYGULAMA & MEDYA KOMUTLARI ---
    elif "not defteri aç" in komut:
        metni_seslendir("Not defterini açıyorum.")
        os.system("notepad.exe")
        return True

    elif "visual studio aç" in komut:
        metni_seslendir("Visual Studio Code açılıyor.")
        os.system("code")
        return True

    elif "android studio aç" in komut:
        metni_seslendir("Android Studio başlatılıyor.")
        os.startfile(r"C:\Program Files\Android\Android Studio\bin\studio64.exe")
        return True

    elif "müzik aç" in komut or "bizim müziği aç" in komut:
        metni_seslendir("AC/DC - Back in Black başlatılıyor efendim.")
        webbrowser.open("https://www.youtube.com/watch?v=pAgnJDJN4VA")
        return True

    elif "soruları ver" in komut:
        metni_seslendir("Sorduğunuz tüm soruları getiriyorum.")
        os.system(f"notepad.exe {SORU_LOG_DOSYASI}")
        return True

    # --- 100 SORULUK BİLGİ BANKASI VE SOHBET (BURASI GERİ GELDİ) ---
    bilgi_bankasi = {
        # Sohbet
        "merhaba": "Merhaba efendim, sizi duymak çok güzel. Emrinizdeyim.",
        "nasılsın": "Tüm sistemlerim optimize durumda, harikayım. Ya siz?",
        "naber": "Sistemler tıkır tıkır çalışıyor efendim, her şey yolunda.",
        "kimsin": "Ben Mehmet Bey'in sadık asistanı JARVİS'im.",
        
        # Bilgi (100 Soru Örnekleri)
        "türkiye'nin başkenti": "Türkiye'nin başkenti Ankara'dır.",
        "en yüksek dağ": "Dünyanın en yüksek dağı Everest'tir.",
        "en büyük gezegen": "Güneş sisteminin en büyük gezegeni Jüpiter'dir.",
        "pi sayısı": "Pi sayısı yaklaşık 3 virgül 14'tür.",
        "yerçekimi": "Yerçekimini Isaac Newton sistemleştirmiştir.",
        "istanbul'un fethi": "İstanbul 1453 yılında fethedilmiştir.",
        "en hızlı hayvan": "Dünyanın en hızlı hayvanı karada çitadır.",
        "ay'a ilk kim gitti": "Ay'a ayak basan ilk insan Neil Armstrong'dur.",
        "en büyük okyanus": "Dünyanın en büyük okyanusu Pasifik Okyanusu'dur."
        # Buraya diğer 100 soruyu önceki gibi eklemeye devam edebilirsiniz...
    }

    for soru, cevap in bilgi_bankasi.items():
        if soru in komut:
            metni_seslendir(cevap)
            return True

    return False

# --- TEMEL FONKSİYONLAR ---
async def metni_seslendir_async(metin):
    print(f"JARVİS: {metin}")
    dosya = "cevap.mp3"
    try:
        communicate = edge_tts.Communicate(metin, VOICE, rate="+10%")
        await communicate.save(dosya)
        pygame.mixer.music.load(dosya)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): await asyncio.sleep(0.1)
        pygame.mixer.music.unload()
    except: pass

def metni_seslendir(metin):
    asyncio.run(metni_seslendir_async(metin))

def asistan_dinle():
    r = sr.Recognizer()
    with sr.Microphone() as kaynak:
        r.adjust_for_ambient_noise(kaynak, duration=0.8)
        print("\n--- JARVİS Dinliyor ---")
        try:
            audio = r.listen(kaynak, timeout=5, phrase_time_limit=8)
            return r.recognize_google(audio, language='tr-TR').lower()
        except: return ""

if __name__ == "__main__":
    metni_seslendir("Sistemler tamamen geri yüklendi efendim. Sizi dinliyorum.")
    while True:
        komut = asistan_dinle()
        if komut == "": continue
        print(f"Sen: {komut}")
        
        if "kendini kapat" in komut or "hoşça kal" in komut:
            metni_seslendir("Tamamdır efendim, görüşmek üzere. Kendinize iyi bakın.")
            break
        
        if not jarvis_islem_merkezi(komut):
            metni_seslendir("Bunu henüz öğrenmedim efendim, ama isterseniz not alabilirim.")