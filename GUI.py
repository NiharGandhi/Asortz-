import tkinter
import customtkinter
from tkinter import filedialog
import dlib
import cv2
import os


detector = dlib.get_frontal_face_detector()


class User_Interface:
    #   Modes: system (default), light, dark
    customtkinter.set_appearance_mode("dark")
    # Themes: blue (default), dark-blue, green
    customtkinter.set_default_color_theme("dark-blue")

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.title('Asortz')
    app.geometry("400x240")

    def choose_folder():
        input_fold = filedialog.askdirectory(title="Choose input folder")
        output_folder = filedialog.askdirectory(title='Choose Output Folder')
        # output_folder = os.path.abspath(output_folder)
        output_folder += '/'
        print('out', output_folder)

        def save(img, name, bbox, width=180, height=227):
            x, y, w, h = bbox
            imgCrop = img[y:h, x:w]
            imgCrop = cv2.resize(imgCrop, (width, height))
            cv2.imwrite(name + '.jpg', imgCrop)

        def faces(pics):
            loc = os.path.basename(pics)
            print('str', loc)
            loc = loc.split('.')
            print('loc', loc)
            loc = loc[0]
            print('lst', loc)
            print(loc)
            new_output_folder = os.path.join(output_folder, loc)
            new_output_folder += '/'
            print('new:', new_output_folder)
            if not os.path.exists(new_output_folder):
                os.makedirs(new_output_folder)
            print(new_output_folder)
            frame = cv2.imread(pics)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            fit = 50
            for counter, face in enumerate(faces):
                print(counter)
                x1, y1 = face.left(), face.top()
                x2, y2 = face.right(), face.bottom()
                save(frame, new_output_folder + str(counter),
                     (x1 - fit, y1 - fit, x2 + fit, y2 + fit))
            frame = cv2.resize(frame, (800, 800))
            print('done saving')

        def process_folder(folder_path):
            print('ANALYSING', folder_path)
            # Loop through all files in the folder
            for filename in os.listdir(folder_path):
                print('list', os.listdir(folder_path))
                print(filename)
                # if not filename.endswith('.jpg') and not filename.endswith('.jpeg') and not filename.endswith('.png'):
                #     print('If Loop')  
                #     continue
                # else:
                print('ELSE LOOP')
                image_path = os.path.join(folder_path, filename)

                faces(image_path)

        process_folder(input_fold)

    # Use CTkButton instead of tkinter Button
    button = customtkinter.CTkButton(
        master=app, text="Start Process", command=choose_folder)
    button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    app.mainloop()
