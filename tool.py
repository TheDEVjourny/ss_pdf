from PIL import ImageGrab,Image
from functools import partial
from pathlib import Path
import keyboard as kb


def screen_shot(save_path, main_screen = False,show_captured_ss = False):
    ''' '''
    ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
    
    BBOX = None 
    if not main_screen:
        BBOX = (1920,0,3850,1080) #(L,T,R,B)
    snapshot = ImageGrab.grab(bbox = BBOX)
    snapshot.save(save_path)
    if show_captured_ss:
        snapshot.show()
    return save_path


def create_notes(images:list,remove_images = True,output_path = r"Download\Notes.pdf"):
    image_dir = Path(r"images")        
    # create list of images
    pil_imgs = [
        Image.open(image) for image in images
    ]
    # images alreasy present
    if not images:
        pil_imgs = [
            Image.open(image_path) for image_path in image_dir.iterdir()
        ]
    # create pdf
    pil_imgs[0].save(
        output_path,"PDF",resolution = 100.0, save_all = True,append_images = pil_imgs[1:]
    )
    # remove images used in pdf
    if remove_images:
        # image_dir = Path(r"images")
        for image_path in image_dir.iterdir():
            image_path.unlink()

def main():
    COUNT = 0
    SS_LIST = []
    TAKE_SS = "right ctrl"
    CREATE_PDF = "right shift"
    STOP = "esc"
    REMOVE_IMAGE = "num lock"
    # infinite loop
    while(True):
        command = kb.read_key()
        # print(command)
        if command == TAKE_SS: 
            COUNT += 1
            image_name = screen_shot(f"images\ss-{COUNT}.png")
            SS_LIST.append(image_name)
            print(f"photo -- {COUNT}")
        elif command == CREATE_PDF:
            create_notes(SS_LIST)
            print("pdf created system ended")
            break
        elif command == REMOVE_IMAGE:
            image_no = int(input("Enter image number:"))
            image = f"images\ss-{image_no}.png"
            if image in SS_LIST:
                SS_LIST.remove(image)
            print(f"IMAGE no {image_no} REMOVED FROM PDF LIST")
            print(SS_LIST)
        elif command == STOP:
            break

# run SS-TO-PDF tool
main()