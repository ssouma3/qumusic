# ====== Standard tkinter modules ======
import tkinter as tk
from tkinter import Scale, Listbox, Label

# ====== Import custom GUI layout module ======
from gui_layout import setup_gui  # Function to initialize all GUI components

# ====== Import Qiskit-related quantum logic ======
from qiskit_logic import Button1_clicked  # Handles quantum circuit construction and execution

# ====== Import sound playback logic ======
from sound_playback import (
    Button2_clicked,             # Handles playback button click (starts music playback)
    play_sequence_from_files,   # Core function for playing MIDI notes based on Qiskit results
    stop_button_clicked         # Handles stop button to interrupt music playback
)

# ====== Import GUI state saving/loading logic ======
from state_io import (
    save_gui_state_dialog,      # Opens save dialog and writes current GUI state to JSON
    load_gui_state_dialog,      # Opens load dialog and loads GUI state from JSON
    reset_gui_state             # Resets all GUI widgets to their default state
)


# ====== Global flag ======
stop_playback = False  # Used by sound_playback (must remain global)

# ====== Main window setup ======
root = tk.Tk()
root.geometry("1600x900")
#root.geometry("1200x600")
root.title("Quantum Gate Circuit Music Generator")
root.configure(width=640, height=480, bg='SlateBlue3')


# ====== Setup all widgets, layout, and bindings ======
# Initialize the entire GUI and retrieve references to interactive components
gui_elements = setup_gui(
    root,
    Button1_clicked=Button1_clicked,         # Function to call when "Measurement" button is clicked
    Button2_clicked=Button2_clicked,         # Function to call when "Playback" button is clicked
    stop_button_clicked=stop_button_clicked, # Function to call when "Stop" button is clicked
    save_gui_state_dialog=save_gui_state_dialog,   # Save GUI state to file
    load_gui_state_dialog=load_gui_state_dialog,   # Load GUI state from file
    reset_gui_state=reset_gui_state                # Reset GUI state to default
)

# ====== Retrieve references to all key widgets and control variables ======
var_btn_mode   = gui_elements["var_btn_mode"]   # Mode selection radio button variable
EditBox2       = gui_elements["EditBox2"]       # Nnotes input field
EditBox3       = gui_elements["EditBox3"]       # Nshots input field
EditBox4       = gui_elements["EditBox4"]       # Tempo input field
Button1        = gui_elements["Button1"]        # "Measurement" button widget
Button2        = gui_elements["Button2"]        # "Playback" button widget
Button_reset   = gui_elements["Button_reset"]   # "Reset GUI" button widget
var_btn        = gui_elements["var_btn"]        # List of gate-setting IntVar (radio buttons)
bln_ini        = gui_elements["bln_ini"]        # List of BooleanVars for checkbox initialization
slider         = gui_elements["slider"]         # Slider A: theta parameter sliders
slider2        = gui_elements["slider2"]        # Slider B: phi parameter sliders
slider_global  = gui_elements["slider_global"]  # Slider C: global modulation
bln_drawer     = gui_elements["bln_drawer"]     # BooleanVar for circuit_drawer toggle
ListBox1       = gui_elements["ListBox1"]       # Output ListBox to show measurement results

# ====== Bind event handlers to buttons ======
# When the "Measurement" button is clicked, call the Button1_clicked handler
# Pass necessary input widgets and variables as arguments
Button1.bind(
    "<Button-1>",
    lambda event: Button1_clicked(
        event,
        var_btn_mode,
        var_btn,
        bln_ini,
        slider,
        slider2,
        slider_global,
        EditBox2,
        EditBox3,
        bln_drawer,
        ListBox1
    )
)

# When the "Playback" button is clicked, trigger the sound playback logic
Button2.bind("<Button-1>", lambda event: Button2_clicked(event, EditBox4))


# ====== Start the Tkinter main event loop ======
# Keeps the GUI window responsive and listens for user interaction
if __name__ == "__main__":
    root.mainloop()


