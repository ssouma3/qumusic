import pygame.midi     # Module for MIDI-based sound playback (notes, instruments, etc.)
import time            # Standard Python module for time-related functions (e.g., delays)
import threading       # Module for running tasks in parallel using threads (e.g., non-blocking playback)


##############################################################################
##  Playback Button ##########################################################
##############################################################################
def Button2_clicked(event,EditBox4):
    global stop_playback
    stop_playback = False  # Reset the stop flag before starting playback

    tempo_str = EditBox4.get()
    try:
        tempo = int(tempo_str)  # Get tempo from input box and convert to integer
    except ValueError:
        print("Tempo must be an integer!")  # Handle invalid input
        return

    # Start the playback in a separate thread to keep the GUI responsive
    threading.Thread(target=play_sequence_from_files, args=(tempo,), daemon=True).start()


##############################################################################
##  play_sequence_from_files #################################################
##############################################################################
def play_sequence_from_files(tempo):
    import pygame.midi
    import time

    global stop_playback
    stop_playback = False  # Reset the stop flag at the beginning of playback

    try:
        # === Initialize MIDI system ===
        pygame.midi.init()
        player = pygame.midi.Output(0)  # Use default MIDI output device
        instrument = 0  # Acoustic Grand Piano (MIDI program 0)
        player.set_instrument(instrument)

        sec_per_beat = 60 / tempo  # Convert tempo (BPM) to seconds per beat

        # === Define pitch mappings ===
        base_notes = [60, 67, 62, 69, 64, 71]  # Base note degrees: C, G, D, A, E, B
        tritone_shift = 6  # Shift used to add a tritone (e.g., for bit = 1)

        # Degree (3-bit) to MIDI note mapping used in var_mode 2 and 3
        degree_to_note = {
            0: None,  # Silence
            1: 65,    # F
            2: 60,    # C
            3: 67,    # G
            4: 62,    # D
            5: 69,    # A
            6: 64,    # E
            7: 71     # B
        }

        # === Load note index list from file ===
        with open("quantum_note_mapping.dat") as f1:
            note_list = [int(line.strip()) for line in f1]

        # === Load bitstrings from file (circuit measurement results) ===
        with open("quantum_measurements.dat") as f2:
            lines = [line.strip() for line in f2]
            header = lines[0].split()       # First line contains metadata (e.g. var_mode)
            var_mode = int(header[-1])      # Use last value in header as mode selector
            bit_strings = lines[1:]         # Remaining lines are bitstrings per shot

        print(f"[INFO] var_mode = {var_mode}")

        if var_mode == 0:
            # Mode 0: Single-bit pitch control (1 bit per note)
            for i, bits in enumerate(bit_strings):
                if stop_playback:
                    break  # Stop if flag is set
                    
                bits = bits[::-1]  # Reverse to match time order: rightmost bit is the earliest note
                for j in range(len(bits)):
                    var = note_list[j % len(note_list)]  # Get the degree index from note_list
                    note = base_notes[var % len(base_notes)]  # Map degree to base MIDI note
                    if bits[j] == '1':
                        note += tritone_shift  # Apply tritone shift (up 6 semitones) for bit '1'
                    player.note_on(note, 100)  # Play note with velocity 100
                    #time.sleep(duration)
                    time.sleep(sec_per_beat)   # Wait for note duration
                    player.note_off(note, 100)  # Stop the note
        
        elif var_mode == 1:
            # Mode 1: Two-bit encoding (duration and pitch per note)
            for i, bits in enumerate(bit_strings):
                if stop_playback:
                    break  # Stop if flag is set
        
                bits = bits[::-1]  # Reverse to match time order        
                for j in range(0, len(bits), 2):
                    if j + 1 >= len(bits):
                        continue  # Skip incomplete bit pairs at the end
                    var = note_list[j // 2 % len(note_list)]  # Get degree for this note
                    base = base_notes[var % len(base_notes)]  # Get base note
                    dur_bit, pitch_bit = bits[j], bits[j+1]  # Split into duration and pitch bits
                    duration = sec_per_beat if dur_bit == '0' else sec_per_beat * 2  # Note duration
                    note = base + (tritone_shift if pitch_bit == '1' else 0)  # Shift pitch if needed
                    player.note_on(note, 100)
                    time.sleep(duration)
                    player.note_off(note, 100)
        
        elif var_mode in [2, 3]:
            # Mode 2 and 3: Three-bit pitch control (e.g., for diatonic degrees or binary-coded notes)
            for bits in bit_strings:
                if stop_playback:
                    break  # Stop if flag is set

                bits = bits[::-1]  # Reverse to match time order
                for j in range(0, len(bits), 3):
                    triplet = bits[j:j+3]  # Take 3-bit chunks
                    if len(triplet) < 3:
                        continue  # Skip incomplete triplets
                    deg = int(triplet, 2)  # Convert binary string to integer
                    note = degree_to_note.get(deg)  # Map degree index to MIDI note
                    if note is None:
                        continue  # Skip if not a valid mapping (e.g., 000 for rest)
                    player.note_on(note, 100)
                    #time.sleep(duration)
                    time.sleep(sec_per_beat)
                    player.note_off(note, 100)


        else:
            print(f"[WARN] Unsupported var_mode: {var_mode}")

    finally:
        player.close()
        pygame.midi.quit()


##############################################################################
##  Stop Button  #############################################################
##############################################################################
def stop_button_clicked(event):
    """
    Callback function for the 'Stop Playback' button.
    This sets the global flag 'stop_playback' to True,
    which can be used to interrupt ongoing music playback.
    """
    global stop_playback
    stop_playback = True



