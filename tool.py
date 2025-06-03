from PIL import ImageGrab
from functools import partial
from reportlab.pdfgen import canvas
import shutil
import keyboard as kb

COUNT = 0
SS_LIST = []
END = False
TAKE_SS = "right ctrl"
CREATE_PDF = "right shift"

def screen_shot(save_path, main_screen = False,show_ss = False):
    ''' '''
    ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
    BBOX = (1920,0,3850,1080) #(L,T,R,B) # or None 
    if main_screen:
        BBOX = None
    snapshot = ImageGrab.grab(bbox = BBOX)
    snapshot.save(save_path)
    if show_ss:
        snapshot.show()
    return save_path

def create_notes(images:list):
    ''' '''
    fileName = 'Notes.pdf'
    documentTitle = 'sample'
    title = 'Findingd'
    # creating a pdf object
    pdf = canvas.Canvas(fileName)
    # setting the title of the document
    pdf.setTitle(documentTitle)
    pdf.drawCentredString(300, 770, title)
    for image in images:
        pdf.drawInlineImage(image, 0,0)
        # drawing a line
        pdf.line(30, 710, 550, 710)
        # shutil.rmtree(image)
    # saving the pdf
    print("notes created")
    pdf.save()



while(not END):
    command = kb.read_key()
    print(command)
    if command == TAKE_SS: 
        COUNT += 1
        image_name = screen_shot(f"ss-{COUNT}.png")
        SS_LIST.append(image_name)
        print(f"photo -- {COUNT}")
    elif command == CREATE_PDF:
        create_notes(SS_LIST)
        print("pdf created system ended")
        break
    elif "0" in command.lower():
        END = True
        break

'''
enter
up
ctrl
space
backspace
right ctrl
right shift
backspace
'''