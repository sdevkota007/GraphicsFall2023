import tkinter as tk

class Slider:
    def __init__(self, root, label_text, min_value, max_value, initial_value, resolution=0.01):
        self.root = root
        self.label = tk.Label(self.root, text=label_text)
        self.label.pack(padx=10, pady=5, anchor="w")
        # Create a Tkinter Scale widget (slider)
        self.slider = tk.Scale(self.root, from_=min_value, to=max_value, orient="horizontal", resolution=resolution)
        self.slider.set(initial_value)  # Set the initial scale value
        self.slider.pack()

    def get_value(self):
        # Get the slider value
        value = self.slider.get()
        self.root.update_idletasks()
        self.root.update()
        return value


class SimpleGUI:
    def __init__(self, title):
        # Create a Tkinter root window for the slider
        self.root = tk.Tk()
        self.root.title(title)

    def add_slider(self, label_text, min_value, max_value, initial_value, resolution=0.01):
        slider = Slider(self.root, label_text, min_value, max_value, initial_value, resolution)
        return slider



if __name__ == '__main__':
    gui = SimpleGUI("Test GUI")
    slider = gui.add_slider("Test Slider", 0, 1, 0.5)

    # careful with this loop, it will run forever. You will get an error if you try to close the window. Ignore it for now.
    while True:
        print(slider.get_value())
