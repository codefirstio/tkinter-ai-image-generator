import customtkinter as ctk    # customtkinter  5.2.2
import tkinter                 # tk             0.1.0
import os
import openai                  # openai         0.28.0  '\_(@@)_/'
from PIL import Image, ImageTk # pillow         10.2.0
import requests, io            # requests       2.31.0

def generate():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable not found.")
    api_key(api_key=api_key)
    print("OPENAI_API_KEY!!!")
    """
    user_prompt = prompt_entry.get("0.0", tkinter.END)
    user_prompt += "in style: " + style_dropdown.get()

    response = openai.Image.create(
        prompt=user_prompt,
        n=int(number_slider.get()),
        size="512x512")
    
    image_urls = []
    for i in range(len(response['data'])):
        image_urls.append(response['data'][i]['url'])
    print(image_urls)
    
    images = []
    for url in image_urls:
        response = requests.get(url)
        image = image.open(io.BytesIO(response.content))
        photo_image = ImageTk.PhotoImage(image)
        images.append(photo_image)
    
    def update_image(index=0):
        canvas.image = images[index]
        canvas.create_image(0, 0, anchor="nw", image=images[index])
        index = (index + 1) % len(images)
        canvas.after(3000, update_image, index)

    update_image()

root = ctk.CTk()
root.title("AI Image Generator")

ctk.set_appearance_mode("dark")

input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)

prompt_label = ctk.CTkLabel(input_frame, text="Prompt")
prompt_label.grid(row=0, column=0, padx=10, pady=10)
prompt_entry = ctk.CTkTextbox(input_frame, height=10)
prompt_entry.grid(row=0, column=1, padx=10, pady=10)

style_ladel = ctk.CTkLabel(input_frame, text="Style")
style_ladel.grid(row=1, column=0, padx=10, pady=10)
style_dropdown = ctk.CTkComboBox(input_frame, values=["Realistic", "Cartoon", "3D Illustration", "Flat Art"])
style_dropdown.grid(row=1, column=1, padx=10, pady=10)

number_label = ctk.CTkLabel(input_frame, text="# Images")
number_label.grid(row=2, column=0)
number_slider = ctk.CTkSlider(input_frame, from_=1, to=10, number_of_steps=9)
number_slider.grid(row=2, column=1)

generate_button = ctk.CTkButton(input_frame, text="Generate", command=generate)
generate_button.grid(row=3, column=0, columnspan=2, sticky="news", padx=10, pady=10)

canvas = tkinter.Canvas(root, width=512, height=512)
canvas.pack(side="left")

root.mainloop()
