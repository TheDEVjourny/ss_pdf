from PIL import ImageGrab,Image
from functools import partial
from pathlib import Path
import keyboard as kb
import datetime
import time
from docx import Document
from docx.shared import Inches
import json
import shutil

#------------------- Configuration -------------------                      
def configure():
    '''
    configure the tool with user input
    '''
    try:
        CONFIG = json.load(open("config.json"))
    except FileNotFoundError:
        print("Config file not found. Using default settings.")
        CONFIG = DEFAULT_CONFIG
    
    TAKE_SS = CONFIG.get("TAKE_IMAGE", "right ctrl")
    CREATE_DOCUMENT = CONFIG.get("CREATE_DOC", "right shift")
    DOC_TYPE = CONFIG.get("Document_type", "pdf")
    STOP = CONFIG.get("STOP_PROCESS", "esc")
    IMAGE_Type = CONFIG.get("IMAGE_Type", "png")
    OUTPUT_PATH = CONFIG.get("Output_Path", "")
    return (
        TAKE_SS, CREATE_DOCUMENT, STOP, 
        DOC_TYPE,IMAGE_Type,OUTPUT_PATH
    )

DEFAULT_CONFIG = {
    "Min_Time_Delay": 1,
    "SS_Type": ".png",
    "MAIN_SCREEN": True,
    "TAKE_IMAGE": "right ctrl",
    "CREATE_DOC": "right shift",
    "STOP_PROCESS": "esc",
    "REMOVE_IMAGE": "num lock",
    "Document_type": ".docx",
    "need_all_images": False
}

#------------------- Utility Functions -------------------

def screen_shot(
        save_path, 
        main_screen = False,
        show_captured_ss = False
    ):
    ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
    BBOX = None 
    if not main_screen:
        # setup for anothesd screen
        BBOX = (1920,0,3850,1080) #(L,T,R,B)
    snapshot = ImageGrab.grab(bbox = BBOX)
    snapshot.save(save_path)
    if show_captured_ss:
        snapshot.show()
    return save_path

def remove_dir_images(image_dir):
    for image_path in image_dir.iterdir():
            image_path.unlink()

def create_pdf(
    images:list = [],
    remove_images = True,
    output_path = r"Download\Notes.pdf"
):
    '''
    the function will create notes in pdf fromat
    '''
    image_dir = Path(r"images") 
    pil_imgs = []     
    # images alreasy present
    if not images:
        pil_imgs = [
            Image.open(image_path) for image_path in image_dir.iterdir()
        ]
    else:
        # create list of images
        pil_imgs = [
            Image.open(image) for image in images
        ]
    # create pdf
    pil_imgs[0].save(
        output_path,"PDF",resolution = 100.0, save_all = True,append_images = pil_imgs[1:]
    )
    # remove images used in pdf
    if remove_images:
        remove_dir_images(image_dir)

def create_docx(
    images:list = [],
    remove_images = True,
    output_path = r"Download\Notes.docx"
    ):
    image_dir = Path(r"images")
    doc = Document()
    # images already present
    if not images:
        image_paths = [image_path for image_path in image_dir.iterdir()]
    else:
        image_paths = images

    for index,image_path in enumerate(image_paths):
        doc.add_paragraph().text = f"Image: {index + 1}"
        doc.add_picture(str(image_path), width=Inches(6))
        doc.add_paragraph().text = "DEFECT : NA"  # Add space between images

    doc.save(output_path)
    
    if remove_images:
        remove_dir_images(image_dir)

def create_current_timestamp() -> int:
    now = datetime.datetime.now()
    return int(now.timestamp() * 1000)

def export_files(output_path,doc_type,remove_from_temp = True):
    '''
    export files to the output path
    '''
    exportable_file = Path(f"Download\\Notes.{doc_type}")
    exported_path = Path(output_path)
    shutil.copy2(exportable_file, exported_path)
    if remove_from_temp:
        # remove files from temp
        if exportable_file.exists():
            exportable_file.unlink()

#------------------- Main Process -------------------

def main():
    COUNT,SS_LIST = 0,[]
    (
        TAKE_SS,CREATE_DOCUMENT,
        STOP,DOC_TYPE,IMAGE_TYPE,OUTPUT_PATH
    ) = configure()
    while(True):
        try:
            # action
            command = kb.read_key()
            # process
            if command == TAKE_SS: 
                COUNT += 1
                image_name_with_path = f"images\ss-{create_current_timestamp()}.{IMAGE_TYPE}"
                image_name = screen_shot(image_name_with_path,True)
                SS_LIST.append(image_name)
                print(f"photo -- {COUNT}")
            elif command == CREATE_DOCUMENT:
                try:
                    if "pdf" in DOC_TYPE:
                        create_pdf(SS_LIST)
                    elif "docx" in DOC_TYPE:
                        create_docx(SS_LIST)
                except:
                    print("facing issue in document creation")
                else:
                    if OUTPUT_PATH:
                        export_files(OUTPUT_PATH,DOC_TYPE)
                    print("document created successfully")
                finally:
                    print(" process ended ")
                break
            elif command == STOP:
                break
            # wait
            # to avoid single keypresses as multiple clicks
            time.sleep(1)
        except Exception:
            print("issue in main function")


if __name__ == "__main__":
    # run SS-TO-PDF tool
    main()