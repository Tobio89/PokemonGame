import os
import shutil
import time

# os.chdir('.\\utilities\\imageReorderTool\\input')
fileLoc = (os.path.dirname(os.path.abspath(__file__)))
input_folder = os.path.join(fileLoc, 'input')
os.chdir(input_folder)

workingDirectory = os.getcwd()

listOfImageFiles = [img for img in os.listdir() if os.path.splitext(img)[1] in ('.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG')]


for n in range(len(listOfImageFiles)):
    
    image = listOfImageFiles[n]
    imageExtension = os.path.splitext(image)[1]

    newFileName = f'{str(n).zfill(3)}{imageExtension}'

    oldFileNameWithPath = os.path.join(workingDirectory, image)
    newFileNameWithPath = os.path.join(workingDirectory, newFileName)

    print(f'Renaming {image} to: {newFileName}')

    shutil.move(oldFileNameWithPath, newFileNameWithPath)

print('Done.')
time.sleep(3)


