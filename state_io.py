#######################################################
import json
import tkinter as tk
from tkinter import filedialog

def save_gui_state_dialog(var_btn, bln_ini, slider, slider2, slider_global,
                    EditBox2, EditBox3, EditBox4, var_btn_mode):
    # Open a save file dialog to choose where to save the GUI state
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",  # Default file extension
        filetypes=[("JSON files", "*.json")],  # File type filter
        title="Save GUI State"  # Dialog window title
    )
    if not file_path:
        return  # Exit if the user cancels the dialog

    # Collect current GUI state into a dictionary
    data = {
        "radio_values": [v.get() for v in var_btn],         # Selected radio button values
        "check_values": [v.get() for v in bln_ini],         # Checkbutton states (True/False)
        "sliders1": [s.get() for s in slider],              # Slider A values
        "sliders2": [s.get() for s in slider2],             # Slider B values
        "slider_global": slider_global.get(),               # Global slider (Slider C)
        "tempo": EditBox4.get(),                            # Tempo input value
        "mode": var_btn_mode.get(),                         # Selected mode (radio)
        "nbar": EditBox2.get(),                             # Number of bars
        "nshot": EditBox3.get()                             # Number of shots
    }

    # Write the data to a JSON file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"GUI state saved to {file_path}")



def load_gui_state_dialog(var_btn, bln_ini, slider, slider2, slider_global,
                    EditBox2, EditBox3, EditBox4, var_btn_mode):
    # Open a file dialog to choose a saved GUI state file (JSON format)
    file_path = filedialog.askopenfilename(
        defaultextension=".json",                    # Default file extension
        filetypes=[("JSON files", "*.json")],        # Only allow JSON files
        title="Load GUI State"                       # Dialog window title
    )
    if not file_path:
        return  # Exit if the user cancels the dialog

    # Load the selected JSON file
    with open(file_path, "r") as f:
        data = json.load(f)

    # Restore radio button values
    for i, val in enumerate(data.get("radio_values", [])):
        if i < len(var_btn):
            var_btn[i].set(val)

    # Restore checkbox states
    for i, val in enumerate(data.get("check_values", [])):
        if i < len(bln_ini):
            bln_ini[i].set(val)

    # Restore slider values (Slider A)
    for i, val in enumerate(data.get("sliders1", [])):
        if i < len(slider):
            slider[i].set(val)

    # Restore slider values (Slider B)
    for i, val in enumerate(data.get("sliders2", [])):
        if i < len(slider2):
            slider2[i].set(val)

    # Restore global slider (Slider C)
    slider_global.set(data.get("slider_global", 0))

    # Restore selected mode (radio button group)
    var_btn_mode.set(data.get("mode", 0))

    # Restore tempo field
    EditBox4.delete(0, tk.END)
    EditBox4.insert(0, data.get("tempo", "120"))

    # Restore number of bars (Nbar)
    EditBox2.delete(0, tk.END)
    EditBox2.insert(0, data.get("nbar", "4"))

    # Restore number of shots (Nshots)
    EditBox3.delete(0, tk.END)
    EditBox3.insert(0, data.get("nshot", "1"))

    print(f"GUI state loaded from {file_path}")


# state_io.py にて
def reset_gui_state(var_btn, bln_ini, slider, slider2, slider_global,
                    EditBox2, EditBox3, EditBox4, var_btn_mode):
    for var in var_btn:
        var.set(0)
    for chk in bln_ini:
        chk.set(False)
    for s in slider:
        s.set(0.0)
    for s in slider2:
        s.set(0.0)
    slider_global.set(0.0)

    EditBox2.delete(0, tk.END)
    EditBox2.insert(0, "4")

    EditBox3.delete(0, tk.END)
    EditBox3.insert(0, "1")

    EditBox4.delete(0, tk.END)
    EditBox4.insert(0, "120")

    var_btn_mode.set(0)

    print("GUI state has been reset to default.")



