from PIL  import Image
from PIL import ImageDraw
from PIL import ImageFont

import os

font_path = "../../display/"

main_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

battery_sprite_path = main_dir + "/menu/menu-sprites/battery_25_15.jpg"
folder_sprite_path = main_dir + "/menu/menu-sprites/folder_21_18.jpg"
gear_sprite_path = main_dir + "/menu/menu-sprites/gear_23_20.jpg"

path = os.path.dirname(__file__) + '/'
small_font = ImageFont.truetype(f"{path}alt-font.ttc", 14)
large_font = ImageFont.truetype(f"{path}alt-font.ttc", 18)

# this code can be ran on windows/host computer side
# easier than trying to run on pi (starting/stopping physical OLED)
# 1.875

width = 240
height = 240

def render_menu():
  image = Image.new("RGB", (width, height), "BLACK")
  draw = ImageDraw.Draw(image)

  draw.text((int(width*0.05), int(height*0.05)), "video", fill = "WHITE", font = small_font, align='center', anchor='lm')
  draw.text((int(width*0.05), int(height*0.85)), "S: 1/60", fill = "WHITE", font = small_font, align='center', anchor='lm')
  draw.text((int(width*0.05), int(height*0.95)), "E: 100", fill = "WHITE", font = small_font, align='center', anchor='lm')
  draw.text((int(width*0.5), int(height*0.5)), "Camera on", fill = "WHITE", font = large_font, align='center', anchor='mm')
  draw.text((int(width*0.7), int(height*0.05)), "3 hrs", fill = "WHITE", font = small_font, align='center', anchor='lm')
  draw.text((int(width*0.6), int(height*0.925)), "24", fill = "WHITE", font = small_font, align='center', anchor='lm')

  battery_icon = Image.open(battery_sprite_path)
  folder_icon = Image.open(folder_sprite_path)
  gear_icon = Image.open(gear_sprite_path)

  image.paste(battery_icon, (int(width*0.85), int(height*0.02)))
  image.paste(folder_icon, (int(width*0.7), int(height*0.89)))
  image.paste(gear_icon, (int(width*0.85), int(height*0.88)))

  image.save(f"{path}menu.jpg")

def render_settings():
  image = Image.new("RGB", (width, height), "BLACK")
  draw = ImageDraw.Draw(image)

  draw.line([(0, 0), (width, 0)], fill = "WHITE", width = int(height*0.3))
  draw.text((int(width*0.05), int(height*0.04)), "Settings", fill = "BLACK", font = large_font, align='center', anchor='la')
  draw.text((int(width*0.05), int(height*0.2)), "Telemetry", fill = "WHITE", font = large_font, align='center', anchor='la')

  image.save(f"{path}settings.png")

render_menu()
render_settings()