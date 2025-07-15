import os
import time
import math

#--------------Driver Library-----------------#
#from .OLED_Driver import Device_Init, Display_Image, Clear_Screen, Display_Buffer
from .LCD_Driver import Init, ShowImage, clear, ShowBuffer, bl_DutyCycle
#from .ST7789 import ST7789#Init, ShowImage, clear, ShowBuffer

#--------------Image Library------------------#
from PIL import Image, ImageDraw, ImageFont, ImageColor

# temporary (lol)
from threading import Thread

#--------------Assets------------------#
base_path = os.path.join(os.path.dirname(__file__), os.pardir) # root of repo eg. /software/ since main.py calls process
path = os.path.dirname(__file__) + '/'

battery_sprite_path = base_path + "/menu/menu-sprites/battery_25_15.jpg"
folder_sprite_path = base_path + "/menu/menu-sprites/folder_21_18.jpg"
gear_sprite_path = base_path + "/menu/menu-sprites/gear_23_20.jpg"

#small_font = ImageFont.truetype(base_path + "/display/alt-font.ttc", 13)
#large_font = ImageFont.truetype(base_path + "/display/alt-font.ttc", 16)

small_font = ImageFont.truetype(f"{path}alt-font.ttc", 14)
large_font = ImageFont.truetype(f"{path}alt-font.ttc", 18)

width = 240
height = 240

class Display:
  def __init__(self, main):
    self.main = main
    self.active_img = None
    self.active_icon = None
    self.utils = main.utils
    self.file_count = self.utils.get_file_count() # maybe shouldn't be here

    # setup LCD
    Init()
    clear()
    bl_DutyCycle(50)
  
  def render_menu_base(self, center_text = "Camera on", photo_text = "photo"):
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.text((int(width*0.05), int(height*0.05)), photo_text, fill = "WHITE", font = small_font, align='center', anchor='lm')
    draw.text((int(width*0.05), int(height*0.9)), "Auto", fill = "WHITE", font = small_font, align='center', anchor='lm')
    # manual photography mode
    # draw.text((int(width*0.05), int(height*0.85)), "S: 1/60", fill = "WHITE", font = small_font, align='center', anchor='lm')
    # draw.text((int(width*0.05), int(height*0.95)), "E: 100", fill = "WHITE", font = small_font, align='center', anchor='lm')
    draw.text((int(width*0.5), int(height*0.5)), center_text, fill = "WHITE", font = large_font, align='center', anchor='mm')
    draw.text((int(width*0.7), int(height*0.05)), self.main.battery.get_remaining_time(), fill = "WHITE", font = small_font, align='center', anchor='lm')
    draw.text((int(width*0.6), int(height*0.925)), str(self.utils.get_file_count()), fill = "WHITE", font = small_font, align='center', anchor='lm')

    battery_icon = Image.open(battery_sprite_path)
    folder_icon = Image.open(folder_sprite_path)
    gear_icon = Image.open(gear_sprite_path)

    image.paste(battery_icon, (int(width*0.85), int(height*0.02)))
    image.paste(folder_icon, (int(width*0.7), int(height*0.89)))
    image.paste(gear_icon, (int(width*0.85), int(height*0.88)))

    return image

  def start_menu(self):
    menu_base = self.render_menu_base()

    ShowImage(menu_base)

  def display_image(self, img_path):
    image = Image.open(img_path)
    ShowImage(image)

  def display_buffer(self, buffer):
    ShowBuffer(buffer)

  def clear_screen(self):
    clear()

  def show_boot_scene(self):
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.text((20, 55), "Pi Zero Cam", fill = "WHITE", font = large_font)
    draw.text((20, 70), "v 1.1.0", fill = "WHITE", font = small_font)

    ShowImage(image)

    time.sleep(3)

    self.clear_screen()

  def set_menu_center_text(self, draw, text, x = width*0.5, y = height*0.5):
    draw.text((x, y), text, fill = "WHITE", font = large_font, align='center', anchor='mm')

  def draw_active_icon(self, icon_name):
    image = self.render_menu_base("")
    draw = ImageDraw.Draw(image)

    if (icon_name == "Files"):
      draw.line([(int(width*0.6), int(height*0.96)), (int(width*0.8), int(height*0.96))], fill = "MAGENTA", width = 2)
      self.set_menu_center_text(draw, "Files")

    if (icon_name == "Camera Settings"):
      draw.line([(int(width*0.05), int(height*0.95)), (int(width*0.25), int(height*0.95))], fill = "MAGENTA", width = 2)
      self.set_menu_center_text(draw, "Camera Settings")

    if (icon_name == "Photo Video Toggle"):
      draw.line([(int(width*0.04), int(height*0.08)), (int(width*0.22), int(height*0.08))], fill = "MAGENTA", width = 2)
      self.set_menu_center_text(draw, "Toggle Mode")

    if (icon_name == "Settings"):
      draw.line([(int(width*0.83), int(height*0.96)), (int(width*0.97), int(height*0.96))], fill = "MAGENTA", width = 2)
      self.set_menu_center_text(draw, "Settings")
    
    ShowImage(image)
  
  def toggle_text(self, mode):
    if (mode == "video"):
      image = self.render_menu_base("Tap to record", "video")
    else:
      image = self.render_menu_base("Toggle Mode", "photo")

    ShowImage(image)

  def draw_text(self, text):
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)
    font = large_font

    draw.text((0, int(height*0.75)), text, fill = "WHITE", font = font)

    ShowImage(image)

  def get_settings_img(self):
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.line([(0, 0), (width, 0)], fill = "WHITE", width = int(height*0.3))
    draw.text((int(width*0.05), int(height*0.04)), "Settings", fill = "BLACK", font = large_font, align='center', anchor='la')
    draw.text((int(width*0.05), int(height*0.2)), "Telemetry", fill = "WHITE", font = large_font, align='center', anchor='la')
    draw.text((int(width*0.05), int(height*0.36)), "Battery Profiler", fill = "WHITE", font = large_font, align='center', anchor='la')
    draw.text((int(width*0.05), int(height*0.52)), "Timelapse", fill = "WHITE", font = large_font, align='center', anchor='la')
    draw.text((int(width*0.05), int(height*0.68)), "Shutdown", fill = "WHITE", font = large_font, align='center', anchor='la')

    return image
  
  def render_settings(self):
    image = self.get_settings_img()

    ShowImage(image)

  def render_battery_profiler(self):
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.text((0, int(height*0.375)), "Profiling battery", fill = "WHITE", font = large_font)
    draw.text((0, int(height*0.56)), "Press back to cancel", fill = "WHITE", font = small_font)

    ShowImage(image)

  def render_timelapse(self):
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.text((0, int(height*0.375)), "5 min timelapse", fill = "WHITE", font = large_font)
    draw.text((0, int(height*0.56)), "Press back to cancel", fill = "WHITE", font = small_font)

    ShowImage(image)

  def render_shutdown(self):
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.text((int(width*0.5), int(height*0.5)), "OK?", fill = "WHITE", font = large_font, align='center', anchor='mm')

    ShowImage(image)

  def render_battery_charged(self, is_charged = False):
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.text((int(width*0.17), int(height*0.375)), "Battery Charged?", fill = "WHITE", font = small_font)
    draw.text((int(width*0.17), int(height*0.56)), "Yes", fill = "CYAN" if is_charged else "WHITE", font = small_font)
    draw.text((int(width*0.47), int(height*0.56)), "No", fill = "WHITE" if is_charged else "CYAN", font = small_font) # default option

    ShowImage(image)

  def draw_active_telemetry(self):
    image = self.get_settings_img()
    draw = ImageDraw.Draw(image)

    draw.line([(0, int(height*0.2)), (0, int(height*0.3))], fill = "MAGENTA", width = 2)

    ShowImage(image)

  def draw_active_battery_profiler(self):
    image = self.get_settings_img()
    draw = ImageDraw.Draw(image)

    draw.line([(0, int(height*0.35)), (0, int(height*0.45))], fill = "MAGENTA", width = 2)

    ShowImage(image)

  def draw_active_timelapse(self):
    image = self.get_settings_img()
    draw = ImageDraw.Draw(image)

    draw.line([(0, int(height*0.51)), (0, int(height*0.61))], fill = "MAGENTA", width = 2)

    ShowImage(image)
  
  def draw_active_shutdown(self):
    image = self.get_settings_img()
    draw = ImageDraw.Draw(image)

    draw.line([(0, int(height*0.67)), (0, int(height*0.77))], fill = "MAGENTA", width = 2)

    ShowImage(image)

  def render_live_telemetry(self):
    while (self.main.menu.active_menu_item == "Telemetry"):
      image = Image.new("RGB", (width, height), "BLACK")
      draw = ImageDraw.Draw(image)

      #accel = self.main.imu.accel
      #gyro = self.main.imu.gyro
      accel = [0,0,0]
      gyro = [0,0,0]

      draw.line([(0, 0), (width, 0)], fill = "WHITE", width = int(height*0.3))
      draw.text((int(width*0.05), 0), "Raw Telemetry", fill = "BLACK", font = large_font)
      draw.text((int(width*0.05), int(height*0.26)), "accel x: " + str(accel[0])[0:8], fill = "WHITE", font = small_font)
      draw.text((int(width*0.05), int(height*0.36)), "accel y: " + str(accel[1])[0:8], fill = "WHITE", font = small_font)
      draw.text((int(width*0.05), int(height*0.46)), "accel z: " + str(accel[2])[0:8], fill = "WHITE", font = small_font)
      draw.text((int(width*0.05), int(height*0.56)), "gyro x: " + str(gyro[0])[0:8], fill = "WHITE", font = small_font)
      draw.text((int(width*0.05), int(height*0.66)), "gyro y: " + str(gyro[1])[0:8], fill = "WHITE", font = small_font)
      draw.text((int(width*0.05), int(height*0.76)), "gyro z: " + str(gyro[2])[0:8], fill = "WHITE", font = small_font)

      ShowImage(image)
    
  # special page, it is not static
  # has active loop to display data
  def render_telemetry_page(self):
    # this is not good, brought in main context into display to pull imu values
    Thread(target=self.render_live_telemetry).start()
  
  # this will need a background process to generate thumbnails
  # since it takes 5+ seconds to do the step below/show files

  # this takes a list of img file paths (up to 4)
  # if it's a video, need ffmpeg to get a thumbnail (future)
  # render the OLED scene with these images and pagination footer
  # yeah this is hard, need offsets
  # https://stackoverflow.com/a/451580

  def get_files_scene(self, file_paths, page, pages):
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)
    base_img_path = base_path + "/captured-media/"

    # this is dumb, my brain is blocked right now, panicking, too much to do
    # this code has to be reworked anyway this is like a demo
    page_map = [[], [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]] # matches file list

    new_size = (80, 80)

    files = page_map[page]
    
    for file in files:
      cam_image = Image.open(base_img_path + file_paths[file])
      base_width= 84
      wpercent = (base_width / float(cam_image.size[0]))
      hsize = int((float(cam_image.size[1]) * float(wpercent)))
      cam_image = cam_image.resize((base_width, hsize), resample=Image.LANCZOS)

      # this is dumb
      if (file == 0):
        image.paste(cam_image, (int(width*0.083), int(height*0.07)))
      if (file == 1):
        image.paste(cam_image, (int(width*0.583), int(height*0.07)))
      if (file == 2):
        image.paste(cam_image, (int(width*0.083), int(height*0.6)))
      if (file == 3):
        image.paste(cam_image, (int(width*0.583), int(height*0.6)))

    if (page > 1):
      draw.text((int(width*0.07), int(height*0.9)), "<", fill = "WHITE", font = small_font)

    draw.text((int(width*0.5), int(height*0.9)), str(page) + "/" + str(pages), fill = "WHITE", font = small_font)

    if (pages > 1):
      draw.text((int(width*0.9), int(height*0.9)), ">", fill = "WHITE", font = small_font)

    return image

  def render_files(self):
    files = self.utils.get_files()
    file_count = len(files)
    self.main.menu.files_pages = 1 if ((file_count / 4) < 1) else math.ceil(file_count / 4)

    if (file_count == 0):
      self.draw_text("No Files")
    else:
      self.main.active_menu = "Files"
      files_scene = self.get_files_scene(files, self.main.menu.files_page, self.main.menu.files_pages)
      ShowImage(files_scene)
