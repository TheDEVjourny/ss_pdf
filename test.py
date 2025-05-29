#-------------only Monitor---------
# import pyautogui as pg
# image = pg.screenshot("ss.jpg")

# from PIL import ImageGrab
# snapshot = ImageGrab.grab()
# save_path = "MySnapshot.jpg"
# snapshot.save(save_path)


#-----------MAIN WINDOW------------------------
# from PIL import ImageGrab
# from functools import partial
# # ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
# ImageGrab.grab = partial(ImageGrab.grab, bbox=(100, 0, 1920, 980)) #(L,T,R,B)
# snapshot = ImageGrab.grab()
# save_path = "MySnapshot.jpg"
# snapshot.save(save_path)

#-----------RIGHT-------------------------------
from PIL import ImageGrab
from functools import partial
# getting all screen
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
# taking only extended monitor
snapshot = ImageGrab.grab(bbox = (1920,0,3850,1080))
save_path = "MySnapshot.jpg"
snapshot.save(save_path)
# snapshot.show()
