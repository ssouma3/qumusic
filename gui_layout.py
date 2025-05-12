import tkinter as tk
from tkinter import Scale, Listbox, Label

def setup_gui(
    root,
    Button1_clicked,
    Button2_clicked,
    stop_button_clicked,
    save_gui_state_dialog,
    load_gui_state_dialog,
    reset_gui_state
):
    # Create labels, buttons, sliders, etc.


    # Create the main root window
    #root = tk.Tk()
    #root.title("Quantum Gate Circuit Music Generator")
    #root.geometry("1200x600")
    # Set window size and background color
    # root.configure(width=640, height=480, bg='SlateGray4')
    #root.configure(width=640, height=480, bg='SlateBlue3')


    #########################################################################
    #### Mode select buttons ################################################
    #########################################################################

    # Checkbox control variable for enabling circuit drawing
    bln_drawer = tk.BooleanVar()
    bln_drawer.set(False)

    # Checkbox for toggling circuit diagram output
    chk = tk.Checkbutton(variable=bln_drawer, text='Use circuit_drawer')
    chk.place(x=370, y=140)

    # Position adjustment for mode radio buttons
    xshift = -190
    yshift = -90

    # Variable to store selected mode (0–4)
    var_btn_mode = tk.IntVar()
    var_btn_mode.set(0)  # Default to Mode 0

    # Array to hold radio button widgets for mode selection
    rdo_mode = [0, 0, 0, 0, 0]
    button_width = 42 

    # Mode 0: Single note (1 qubit)
    rdo_mode[0] = tk.Radiobutton(root, value=0, variable=var_btn_mode,
        text='Mode 1: Single note (Nbit_note = 1)', width=button_width, anchor='w')
    rdo_mode[0].place(x=200 + xshift, y=100 + yshift)

    # Mode 1: Single note with variable duration (2 qubits)
    rdo_mode[1] = tk.Radiobutton(root, value=1, variable=var_btn_mode,
        text='Mode 2: Single note ~ variable duration (Nbit_note = 2)', width=button_width, anchor='w')
    rdo_mode[1].place(x=200 + xshift, y=120 + yshift)

    # Mode 2: Diatonic chord tone selection (3 qubits)
    rdo_mode[2] = tk.Radiobutton(root, value=2, variable=var_btn_mode,
        text='Mode 3: Diatonic chord tone (Nbit_note = 3)', width=button_width, anchor='w')
    rdo_mode[2].place(x=200 + xshift, y=140 + yshift)

    # Mode 3: Phase modulation using 3 qubits
    rdo_mode[3] = tk.Radiobutton(root, value=3, variable=var_btn_mode,
        text='Mode 4: Phase modulation (Nbit_note = 3)', width=button_width, anchor='w')
    rdo_mode[3].place(x=200 + xshift, y=160 + yshift)

    # Mode 4: Quantum game mechanics (2 qubits)
    rdo_mode[4] = tk.Radiobutton(root, value=4, variable=var_btn_mode,
        text='Mode 5: Quantum Game (Nbit_note = 2)', width=button_width, anchor='w')
    rdo_mode[4].place(x=200 + xshift, y=180 + yshift)


    #########################################################################
    #### Nnote and  Nshots Edit Box #########################################
    #########################################################################
    yspace=30
    ### Label #####################################
    Label2 = tk.Label(text='Nnotes') # (Total qubit : Nnote*Nbit_note)
    #Label2.grid(row=1, column=0, padx=5, pady=5)
    Label2.place(x=10, y=140+yspace*0)

    EditBox2 = tk.Entry(width=5)
    EditBox2.insert(tk.END,"4")
    #EditBox2.grid(row=1, column=1, padx=5, pady=5)
    EditBox2.place(x=80, y=140+yspace*0)
    ###############################################
    ### Label #####################################
    Label3 = tk.Label(text='Nshots')
    #Label3.grid(row=2, column=0, padx=5, pady=5)
    Label3.place(x=10, y=140+yspace*1)

    EditBox3 = tk.Entry(width=5)
    EditBox3.insert(tk.END,"1")
    #EditBox3.grid(row=2, column=1, padx=5, pady=5)
    EditBox3.place(x=80, y=140+yspace*1)



    #########################################################################
    #### Measurement and Playback button ####################################
    #########################################################################
    # Vertical spacing between components
    yspace = 30

    # === Measurement Button ===
    Button1 = tk.Button(
        text='Measurement',        # Button label
        width=20,                  # Button width (in character units)
        relief='raised',           # 3D effect for button border
        cursor='hand2',            # Cursor changes to hand icon on hover
        bg='lightblue',            # Background color
        activebackground='skyblue'  # Background color when clicked
    )
    #Button1.bind("<Button-1>", Button1_clicked)   # Bind to quantum circuit execution
    Button1.place(x=200, y=140 + yspace * 0)      # Place at specified coordinates

    # === Playback Button with Tempo Label ===
    Button2 = tk.Button(
        text='Playback [Tempo:               ]',  # Tempo editable via separate entry box
        width=20,
        relief='raised',
        cursor='hand2',
        bg='lightblue',
        activebackground='skyblue'
    )
    Button2.bind("<Button-1>", Button2_clicked)   # Bind to music playback function
    Button2.place(x=200, y=140 + yspace * 1)


    #########################################################################
    ##### 'Stop Playback' button to interrupt music playback ################
    #########################################################################
    Button_stop = tk.Button(
        text='Stop Playback',           # Label shown on the button
        width=20,                       # Width of the button in text units
        relief='raised',                # 3D-style border to make it stand out
        cursor='hand2',                 # Cursor changes to hand when hovering
        bg='lightcoral',                # Normal background color
        activebackground='red'          # Background color when clicked
    )
    # Bind the button click event to the stop handler
    Button_stop.bind("<Button-1>", stop_button_clicked)
    # Place the button at a specified position in the window
    Button_stop.place(x=200, y=200)  # Adjust coordinates as needed



    # === Tempo Entry Box ===
    EditBox4 = tk.Entry(width=5)                 # Small input box for BPM (beats per minute)
    EditBox4.insert(tk.END, " 120 ")            # Default value = 120 BPM
    EditBox4.place(x=303, y=143 + yspace * 1)   # Positioned next to playback button


    #########################################################################
    ## Labels for Mapping Between Buttons/Sliders and Gate Operations #######
    #########################################################################
    # === Create a Frame to hold the table ===
    label_frame = tk.Frame(root, bg="white", width=600, height=230)
    label_frame.place(x=590, y=5)  # Adjust the overall table position

    # === Add title label ===
    title_label = tk.Label(label_frame, 
                        text="Mapping Between Buttons/Sliders and Gate Operations", 
                        bg="white", fg="black", font=("Arial", 10, "bold"))
    title_label.place(x=80, y=0)

    # === Label text organized per column ===
    label_table = [
        ["", "Gate 1", "Gate 2", "Gate 3", "Gate 4", "Gate 5", 
        "Gate 6", "Gate 7", "Gate 8", "Switch 1", "Slider A", "Slider B", "Slider C"],
        ["Mode 1,2", "C/F#", "G/Db", "D/Ab", "A/Eb", "E/Bb", "B/F", "-", "-", "Inverter", "-", "-", "-"],
        ["Mode 3", "I",    "II",  "III",   "IV",    "V",  "VI",   "VII",  "-", "--", "-", "-", "-"],
        ["Mode 4", "none",  "F", "C",   "G",  "D", "A",  "E", "B", "-", "noise", "-", "Inter-note phase"],
        ["Mode 5", "C/F#", "G/Db", "D/Ab",  "A/Eb", "E/Bb", "B/F", "-", "-", "-", 
        "Phase θ in U3(θ,φ,π)", "Phase φ in U3(θ,φ,π)", "-"]
    ]
    # === Font and layout settings ===
    font_setting = ("Arial", 9)
    line_height = 15         # Space between rows
    start_y = 20             # Initial vertical position of labels
    # === Define x-coordinates for each column within the frame ===
    x_positions = [10, 110, 210, 310, 410]
    # === Create and place each label ===
    for col, x in enumerate(x_positions):
        for row, text in enumerate(label_table[col]):
            tk.Label(label_frame, text=text, bg="white", fg="black", font=font_setting,
                    anchor="w", width=16).place(x=x, y=start_y + row * line_height)


    #########################################################################
    ################ Gate Radio Buttons #####################################
    #########################################################################
    # Initialize lists for widget control variables and widgets
    var_btn = [tk.IntVar(value=0) for _ in range(38)]       # Variables for radio buttons (gate selection)
    rdo = [None] * 331                                       # Radio button widget holders
    bln_ini = [tk.BooleanVar(value=False) for _ in range(112)]  # Boolean variables for checkboxes (initialized to True)
    chk_ini = [None] * 112                                   # Checkbox widget holders

    # Layout configuration
    start_x = 70                    # Initial X-coordinate for placement
    step_x = 35                     # Horizontal spacing between columns
    start_y = 240                   # Initial Y-coordinate for top row
    radio_values = list(range(8))  # Values for radio buttons: Gate00 to Gate07
    radio_spacing = 30             # Vertical spacing between each radio button

    # --- Place number labels (1 to 32) above each column ---
    for i in range(32):
        x = start_x + i * step_x
        gate_label = tk.Label(root, text=str(i + 1))  # Label with gate index (1-based)
        gate_label.place(x=x, y=start_y)

    # --- Create and place radio buttons and checkboxes for each column ---
    for i in range(32):
        x = start_x + i * step_x
        for j, val in enumerate(radio_values):
            idx = i * len(radio_values) + j  # Calculate index in rdo list
            y = start_y + 20 + j * radio_spacing
            rdo[idx] = tk.Radiobutton(root, value=val, variable=var_btn[i], text='')  # Create radio button
            rdo[idx].place(x=x, y=y)  # Place radio button at calculated position

        # Place checkbox just below the last radio button
        chk_ini[i] = tk.Checkbutton(root, variable=bln_ini[i], text='')
        chk_ini[i].place(x=x, y=start_y + 20 + len(radio_values) * radio_spacing)

    ##### Gate Labels ############################################# 
    gate_labels = [
        "Gate 1", "Gate 2", "Gate 3", "Gate 4",
        "Gate 5", "Gate 6", "Gate 7", "Gate 8", "Switch 1"
    ]

    start_y = 262
    line_height = 30
    for i, text in enumerate(gate_labels):
        label = tk.Label(text=text)
        label.place(x=10, y=start_y + i * line_height)


    #########################################################################
    #### Sliders ############################################################
    #########################################################################
    slider = [0] * 32
    slider2 = [0] * 32

    start_y = 530

    # --- Slider A: θ (angle) ---
    for i in range(32):
        slider[i] = Scale(root, from_=0, to=1, resolution=0.05, tickinterval=0.01,
                          font=("", 7), width=10)
        slider[i].place(x=55 + 35 * i, y=start_y)

    # --- Slider B: φ (phase) ---
    for i in range(32):
        slider2[i] = Scale(root, from_=0, to=1, resolution=0.05, tickinterval=0.01,
                           font=("", 7), width=10)
        slider2[i].place(x=55 + 35 * i, y=start_y + 100)

    # --- Global Slider C ---
    slider_global = Scale(root, from_=-2, to=2, resolution=0.05,
                          font=("", 7), tickinterval=0.01, width=10)
    slider_global.place(x=55 + 35 * 33 - 20, y=start_y + 50)

    # --- Labels for Sliders ---
    slider_labels = ["Slider A", "Slider B"]
    label_start_y = 550
    line_height = 100

    for i, text in enumerate(slider_labels):
        label = Label(root, text=text)
        label.place(x=10, y=label_start_y + i * line_height)

    label_slider_common = Label(root, text='Slider C')
    label_slider_common.place(x=55 + 35 * 33 - 20, y=label_start_y)

    #########################################################################
    #### Measurement Result Display Window (ListBox) ########################
    #########################################################################

    # A ListBox to display measurement results from Qiskit execution
    ListBox1 = tk.Listbox(width=200, height=10)
    ListBox1.place(x=10, y=start_y + 220)
    #ListBox1.insert(tk.END, "aaa")  # (Example) insert dummy result



    #########################################################################
    ##### Save and Load  ####################################################
    #########################################################################
    # --- Save Button with arguments ---
    Button_save = tk.Button(
        text='Save GUI State',
        width=15,
        bg="lightgreen",
        command=lambda: save_gui_state_dialog(
            var_btn, bln_ini, slider, slider2, slider_global,
            EditBox2, EditBox3, EditBox4, var_btn_mode
        )
    )
    Button_save.place(x=400, y=20)

    # --- Load Button with arguments ---
    Button_load = tk.Button(
        text='Load GUI State',
        width=15,
        bg="lightyellow",
        command=lambda: load_gui_state_dialog(
            var_btn, bln_ini, slider, slider2, slider_global,
            EditBox2, EditBox3, EditBox4, var_btn_mode
        )
    )
    Button_load.place(x=400, y=60)

    Button_reset = tk.Button(
        text='Reset GUI',
        width=15,
        relief='raised',
        cursor='hand2',
        bg='lightgray',
        activebackground='gainsboro',
        #command=reset_gui_state  
        command=lambda: reset_gui_state(var_btn, bln_ini, slider, slider2, slider_global, EditBox2, EditBox3, EditBox4, var_btn_mode)
    )
    Button_reset.place(x=400, y=100)  #


    # --- Return references ---
    return {
        "var_btn_mode": var_btn_mode,
        "EditBox2": EditBox2,  # Nnotes
        "EditBox3": EditBox3,   # Nshots
        "EditBox4": EditBox4,   #Tempo
        "Button1": Button1,
        "Button2": Button2,
        "Button_reset":Button_reset,
        "var_btn": var_btn,
        "bln_ini": bln_ini, 
        "slider": slider,
        "slider2": slider2,
        "slider_global": slider_global,
        "bln_drawer": bln_drawer,
        "ListBox1": ListBox1 
    }


