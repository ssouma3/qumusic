# Quantum Gate Circuit Music Generator

This project is a graphical tool for generating music using quantum circuits.
It was originally developed as part of the **IPA FY2018 MITOU "Unexplored" Target Program** in the *Quantum Gate Computing* category, supported by the Ministry of Economy, Trade and Industry (METI), Japan.

See the official project introduction here:  
👉 [IPA 2018 Unexplored Quantum Gate Projects](https://www.ipa.go.jp/jinzai/mitou/target/2018/gate/seika-quantum-gate.html)


## Features

- Build quantum circuits interactively using a GUI
- Generate musical notes based on quantum measurement results
- Multiple modes (1-qubit, 2-qubit, chord mode, etc.)
- Real-time MIDI playback using `pygame.midi`
- Educational and creative: combines quantum logic and music

👉 For a more detailed manual and ongoing updates, please visit the project website:  
[https://www.quantum-creation.jp](https://www.quantum-creation.jp)

## Installation

It is recommended to use **Python 3.10 or later**.
You can recreate the environment using the provided YAML file:

```bash
conda env create -f qgcmg_v1.0.yml
conda activate quantum-music-mitou-win
```

Or install manually:

```bash
pip install -r requirements.txt
```

## How to Run

To launch the GUI:

```bash
python main.py
```

## Project Structure

```
.
├── main.py             # Entry point: GUI and application logic
├── gui_layout.py       # GUI layout definition
├── qiskit_logic.py     # Quantum circuit creation and simulation
├── sound_playback.py   # Sound generation and MIDI playback
├── state_io.py         # State saving/loading
├── qgcmg_v1.0.yml      # Conda environment file
├── requirements.txt    # Python dependencies
└── README.md           # This documentation file
```

## Related Publication

The theoretical background behind the algorithm and this implementation is described in detail in:

Souma, S. (2022). *Exploring the Application of Gate-Type Quantum Computational Algorithm for Music Creation and Performance*.  
In: Miranda, E.R. (eds) **Quantum Computer Music**, Springer, Cham.  
[Chapter 5, Quantum Computer Music (Springer Link)](https://link.springer.com/chapter/10.1007/978-3-031-13909-3_5)

## License

This software is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

## Author

Satofumi Souma  
Email: satofumi.souma@gmail.com
