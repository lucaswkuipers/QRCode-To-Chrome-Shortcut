# 1- Get link from qrcode
# 2- Create shortcut from link 
# 3- Repeat for every qrcode in subfolders

# Importing required modules
import cv2
from pyzbar.pyzbar import decodegit
import os

# Returns link from given qr code image filename
def getLink(filename):

    image = cv2.imread(filename)

    alpha = 1.5 # Contrast control (1.0-3.0)

    # Adjusts image contrast to 1.5 from original
    adjusted = cv2.convertScaleAbs(image, alpha=alpha)

    barcode = decode(adjusted)[0]
     
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)

    link = barcode.data.decode('ascii')

    print(f'Link read sucessfully for {filename}')
    print('Link:', link)
    
    return link

# Creates python file (with given name) that runs cmd command to open chrome at given link
def createShortcut(filepath, link):

    filepath = filepath[:-3]

    f = open(f"{filepath}py", "w")
    f.write("import os;")
    f.write(f'os.system(\'cmd /c \"start chrome {link}\"\')')
    f.close()      

def main():
    for subdir, dirs, files in os.walk('.'):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith(".png"):
                
                createShortcut(filepath, getLink(filepath))
    print('All shortcuts created!')
        
if __name__ == '__main__':
    main()