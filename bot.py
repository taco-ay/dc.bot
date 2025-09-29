import discord
from discord.ext import commands
from logic import foto_uret, foto_cevir # Hem foto_uret hem de foto_cevir'i içeri aktarıyoruz
import os # Dosya işlemlerini yapmak için os modülünü içeri aktarıyoruz

# ÖNEMLİ: config.py dosyasında API ve SECRET KEY var. 
# Discord botunun çalışması için ayrıca bir TOKEN'a ihtiyacınız var.
# config.py'ye 'TOKEN="SENIN_DISCORD_BOT_TOKENIN"' eklediğinizi varsayıyorum.
# Eğer eklemediyseniz, bot.py'nin en başına TOKEN'ı manuel olarak ekleyin.

# ÖRNEK:
# from config import TOKEN 
TOKEN = "MTM2NjQ3MTQyMzI0MTIyODMyOQ.GhS9nu.axdRqbphQ0vNeDJUmX808Ton2SLNQzw7HszNuk" # Eğer config.py'de yoksa burayı kullanın

# Burası Discord Intents'i doğru şekilde almanız için
intents = discord.Intents.default()
intents.message_content = True # Botun mesaj içeriğini okuması için bu gerekli

# Komut öneki ve intent'ler ile bot'u başlatıyoruz
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Botun hazır olduğunu belirten mesaj
    print(f"{bot.user} olarak giriş yaptım.")
    
@bot.command()
async def selam(ctx):
    # Basit bir selamlama komutu
    await ctx.send(f"Selam {ctx.author.mention}, ben {bot.user.mention}'im")

@bot.command()
async def create_img(ctx, *, prompt: str):
    """
    Kullanıcının verdiği metin (prompt) ile resim oluşturan komut.
    Örn: !create_img Bir deniz kenarında gün batımı, dijital sanat
    """
    
    # Kullanıcıya bekleme mesajı gönderiliyor
    message = await ctx.send(f"**'{prompt}'** için resim oluşturuluyor... Lütfen bekleyin. Bu işlem biraz zaman alabilir.")
    
    # Oluşturulacak dosyanın adı. Discord için .jpeg uzantısı kullanıyoruz.
    file_name = "output.jpeg" 
    
    try:
        # 1. Fotoğrafı Base64 stringi olarak al
        # 'logic.py' dosyanızdaki 'foto_uret' fonksiyonu Base64 string'i döndürüyor.
        base64_img = foto_uret(prompt)
        
        # 2. Base64 string'i bir dosyaya çevir
        # 'foto_cevir' fonksiyonu Base64 string'i alır ve belirtilen yola kaydeder.
        foto_cevir(base64_img, file_name)

        # 3. Dosyayı Discord'a gönder
        with open(file_name, "rb") as f:
            picture = discord.File(f)
            # Bekleme mesajını güncelleyip resmi gönderiyoruz
            await message.edit(content=f"İşte **'{prompt}'** için oluşturulan resim:")
            await ctx.send(file=picture)
            
    except Exception as e:
        # Herhangi bir hata oluşursa kullanıcıya bildir
        await message.edit(content=f"Hata oluştu: Resim oluşturulamadı. Detay: {e}")
        print(f"Hata oluştu: {e}") # Konsola hatayı yazdır
        
    finally:
        # İşlem bittikten sonra sunucuda oluşturulan dosyayı siliyoruz (isteğe bağlı ama önerilir)
        if os.path.exists(file_name):
            os.remove(file_name)
            
# Botu çalıştırıyoruz
bot.run(TOKEN)