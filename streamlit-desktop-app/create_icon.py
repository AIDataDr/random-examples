from pathlib import Path
from PIL import Image, ImageDraw
assets = Path(__file__).resolve().parent / 'assets'
assets.mkdir(exist_ok=True)
image = Image.new('RGBA', (256, 256))
draw = ImageDraw.Draw(image)
draw.rounded_rectangle((8, 8, 248, 248), radius=40, fill='#2563EB')
for x, y in [(48,155),(90,110),(132,50),(174,90)]:
    draw.rectangle((x,y,x+30,205), fill='white')
image.save(assets / 'logo.png')
image.save(assets / 'app.ico', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
