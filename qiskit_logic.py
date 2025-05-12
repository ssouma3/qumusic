from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from qiskit_aer import Aer
from qiskit.circuit.library import UGate
import math
from math import pi
import tkinter as tk

##############################################################################
## Measurement (Qiskit logic) Button #########################################    
##############################################################################
def Button1_clicked(event, var_btn_mode, var_btn, bln_ini, slider, slider2, slider_global, EditBox2, EditBox3, bln_drawer,ListBox1):
    var_mode = var_btn_mode.get()  # Get selected mode from GUI

    # Determine number of qubits per note based on the mode
    if var_mode == 0:
        Nqb_half = 1  # Mode 0: 1 qubit per note
    elif var_mode == 1:
        Nqb_half = 2  # Mode 1: 2 qubits per note (pitch + duration)
    elif var_mode == 2:
        Nqb_half = 3  # Mode 2: 3 qubits per note (chord tones)
    elif var_mode == 3:
        Nqb_half = 3  # Mode 3: 3 qubits per note (phase modulation)
    elif var_mode == 4:
        Nqb_half = 2  # Mode 4: 2 qubits per note (quantum game or other logic)

    print("Nqb_half =", Nqb_half)
    Nqb = Nqb_half * 2  # Total number of qubits (assuming 2 channels alternating)
    print("Nqb =", Nqb)

    # Get number of bars and shots from GUI input
    Nbar = int(EditBox2.get())        # Number of musical bars (measures)
    Nnote_shots = int(EditBox3.get()) # Number of shots per measurement

    from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

    # Create quantum and classical registers
    q = QuantumRegister(Nqb, name='q')               # Quantum register
    c = ClassicalRegister(Nqb, name='c')             # Optional: may be unused
    c_music = ClassicalRegister(Nqb_half * Nbar, name='c_music')  # For music-specific measurement

    # Initialize quantum circuit
    qc = QuantumCircuit(q, c_music)

    ##########################################################################
    # Internal function to perform measurement and reset for one bar
    def measure_print(inote):
        if (inote - 1) % 2 == 0:
            n1 = 0
            n2 = Nqb_half
        elif (inote - 1) % 2 == 1:
            n1 = Nqb_half
            n2 = Nqb

        nshift = inote - 1  # bar index shift
        for i in range(n1, n2):
            qc.measure(q[i], c_music[i - n1 + nshift * Nqb_half])  # Measure qubit to classical bit
            qc.reset(q[i])  # Reset qubit for reuse in next step


            
    ############################################################### 
    def gate_single_cx01(q,inote,ith):

        if (inote-1)%2==0: 
            #qc.h(q[0]);
            #qc.barrier(q)        

            #qc.h(q[3]);
            qc.cx(q[0], q[1])
            
            qc.h(q[0]);
            #qc.u1(ith*pi/6,q[0]);
            qc.p(ith*pi/6, q[0])

        
        elif (inote-1)%2==1:

            #qc.h(q[1]);
            #qc.barrier(q)
            
            #qc.h(q[0]);
            qc.cx(q[1], q[0])
            qc.h(q[1]);
            #qc.u1(ith*pi/6,q[1]);
            qc.p(ith*pi/6, q[1])
            
    ############################################################### 
    def gate_single_cx02(q,inote,ith,initbit):
                
        if (inote-1)%2==0: 
            #qc.h(q[0]);
            #qc.barrier(q)
            if (initbit==True):
                qc.x(q[1]);

            #qc.h(q[3]);
            qc.cx(q[0], q[1])
            
            #qc.h(q[0]);
            #qc.u3(-ith*pi/6,0,0,q[0]);
            qc.append(UGate(-ith * pi / 6, 0, 0), [q[0]])
        
        elif (inote-1)%2==1:

            #qc.h(q[1]);
            #qc.barrier(q)
            if (initbit==True):
                qc.x(q[0]);
            
            #qc.h(q[0]);
            qc.cx(q[1], q[0])
            #qc.h(q[1]);
            #qc.u3(-ith*pi/6,0,0,q[1]);
            qc.append(UGate(-ith * pi / 6, 0, 0), [q[1]])
        
    ############################################################### 
    def gate_double_cx01(q,inote,ith,initbit):
        
        if (inote-1)%2==0: 

            print("initbit=",initbit)
            if (initbit==True):
                qc.x(q[1]);               
                qc.x(q[2]);
                

            #qc.h(q[3]);
            qc.cx(q[0], q[1])
            qc.cx(q[1], q[2])
            
            #qc.h(q[0]);
            #qc.u3(-ith*pi/6,0,0,q[0]);
            qc.append(UGate(-ith * pi / 6, 0, 0), [q[0]])
            #qc.u3(-ith*pi/6,0,0,q[1]);
        
            qc.h(q[1]);
        
        elif (inote-1)%2==1:

            #qc.h(q[1]);
            #qc.barrier(q)
            if (initbit==True):
                qc.x(q[0]);
                qc.x(q[3]);
            
            #qc.h(q[0]);
            qc.cx(q[2], q[3])
            qc.cx(q[3], q[0])
            #qc.h(q[1]);
            #qc.u3(-ith*pi/6,0,0,q[2]);
            qc.append(UGate(-ith * pi / 6, 0, 0), [q[2]])
            #qc.u3(-ith*pi/6,0,0,q[3]);
            qc.h(q[3]);
            
    
    ############################################################## 
    def gate_game(q,inote,thA,thB,phA,phB,initbitA,initbitB):
        
        
        if (inote-1)%2==0:   

            
            #Entangler
            qc.cx(q[0], q[1])
            #qc.u3(pi/2,  pi/2, -pi/2,q[0]);
            qc.append(UGate(pi / 2, pi /2 , -pi/2), [q[0]])

            qc.cx(q[0], q[1])
            
            #Move
            #qc.u3(thA,phA,pi,q[0]);
            qc.append(UGate(thA, phA, pi), [q[0]])
            #qc.u3(thB,phB,pi,q[1]);
            qc.append(UGate(thB, phB, pi), [q[1]])

            
            #DisEntangler
            qc.cx(q[0], q[1])
            #qc.u3(pi/2,  -pi/2, pi/2,q[0]);
            qc.append(UGate(pi/2, -pi/2, pi/2), [q[0]])

            qc.cx(q[0], q[1])
            
            #cx to next note
            if (initbitA==1):
                qc.cx(q[0], q[2]);
            if (initbitB==1):
                qc.cx(q[1], q[3]);
            
            
            
            qc.barrier(q)
        
        elif (inote-1)%2==1:            
            
            #Entangler
            qc.cx(q[2], q[3])
            #qc.u3(pi/2,  pi/2, -pi/2,q[2]);
            qc.append(UGate(pi/2, pi/2, -pi/2), [q[2]])

            qc.cx(q[2], q[3])
            
            #Move
            #qc.u3(thA,phA,pi,q[2]);
            #qc.u3(thB,phB,pi,q[3]);
            qc.append(UGate(thA, phA, pi), [q[2]])
            qc.append(UGate(thB, phB, pi), [q[3]])


            #DisEntangler
            qc.cx(q[2], q[3])
            #qc.u3(pi/2,  -pi/2, pi/2,q[2]);
            qc.append(UGate(pi/2, -pi/2, pi/2), [q[2]])
            qc.cx(q[2], q[3])
            
            #cx to next note
            if (initbitA==1):
                qc.cx(q[2], q[0]);
            if (initbitB==1):
                qc.cx(q[3], q[1]);
         
            
            qc.barrier(q)

            
    ############################################################################
    def gate_IM7(q,inote):
        #http://quantum.classcat.com/2018/02/05/qiskit-tutorial-2-4_quantum_info_two_qubit_qrac/

        if (Nqb_half>=3):
            if (inote-1)%2==0: 

                theta = pi * slider_global.get()
                for i in [0, 1, 2]:
                    qc.append(UGate(theta, 0, 0), [q[i]])
    

                
                qc.h(q[0]);
                qc.x(q[1]);
                qc.h(q[2]);
                #qc.barrier(q)



            elif (inote-1)%2==1:
                
                theta = pi * slider_global.get()
                for i in range(3, 6):  # q[3], q[4], q[5]
                    qc.append(UGate(theta, 0, 0), [q[i]])


                qc.h(q[3]);
                qc.x(q[4]);
                qc.h(q[5]);
                #qc.barrier(q)

           #return qProg
        
    def gate_IIm7(q,inote):
        #http://quantum.classcat.com/2018/02/05/qiskit-tutorial-2-4_quantum_info_two_qubit_qrac/

        if (Nqb_half>=3):
            if (inote-1)%2==0: 

                theta = pi * slider_global.get()
                for i in range(3):  # q[0], q[1], q[2]
                    qc.append(UGate(theta, 0, 0), [q[i]])
                
                qc.h(q[0]);
                qc.h(q[2]);
                qc.ccx(q[0],q[2],q[1]);
                
                qc.x(q[0]);
                qc.x(q[2]);
                #qc.barrier(q)



            elif (inote-1)%2==1:
                
                theta = pi * slider_global.get()
                for i in range(3, 6):  # q[3], q[4], q[5]
                    qc.append(UGate(theta, 0, 0), [q[i]])


                qc.h(q[3]);
                qc.h(q[5]);
                qc.ccx(q[3],q[5],q[4]);
                
                qc.x(q[3]);
                qc.x(q[5]);
                #qc.barrier(q)
                

           #return qProg
        
    def gate_IIIm7(q,inote):

        if (Nqb_half>=3):
            if (inote-1)%2==0: 

                theta = pi * slider_global.get()
                for i in range(3):  # i = 0, 1, 2
                    qc.append(UGate(theta, 0, 0), [q[i]])
                
                qc.h(q[0]);
                qc.h(q[1]);
                qc.x(q[2]);
                qc.ccx(q[0],q[1],q[2]);
                qc.ccx(q[0],q[2],q[1]);
                
                #qc.barrier(q)



            elif (inote-1)%2==1:
                
                theta = pi * slider_global.get()
                for i in range(3, 6):  # q[3], q[4], q[5]
                    qc.append(UGate(theta, 0, 0), [q[i]])


                qc.h(q[3]);
                qc.h(q[4]);
                qc.x(q[5]);
                qc.ccx(q[3],q[4],q[5]);
                qc.ccx(q[3],q[5],q[4]);
                
                #qc.barrier(q)
                

           #return qProg
        
    
    def gate_IVM7(q,inote):
        #http://quantum.classcat.com/2018/02/05/qiskit-tutorial-2-4_quantum_info_two_qubit_qrac/

        if (Nqb_half>=3):
            if (inote-1)%2==0: 

                theta = pi * slider_global.get()
                for i in range(3):  # i = 0, 1, 2
                    qc.append(UGate(theta, 0, 0), [q[i]])
                
                
                qc.x(q[0]);
                qc.h(q[1]);
                qc.h(q[2]);
                qc.cx(q[1],q[0]);
                
                #qc.barrier(q)



            elif (inote-1)%2==1:
                
                theta = pi * slider_global.get()
                for i in range(3, 6):  # q[3], q[4], q[5]
                    qc.append(UGate(theta, 0, 0), [q[i]])

                qc.x(q[3]);
                qc.h(q[4]);
                qc.h(q[5]);
                qc.cx(q[4],q[3]);
                
                
                #qc.barrier(q)
                

           #return qProg
        
    def gate_V7(q,inote):
        #http://quantum.classcat.com/2018/02/05/qiskit-tutorial-2-4_quantum_info_two_qubit_qrac/

        if (Nqb_half>=3):
            if (inote-1)%2==0: 

                theta = pi * slider_global.get()
                for i in range(3):  # i = 0, 1, 2
                    qc.append(UGate(theta, 0, 0), [q[i]])
                
                qc.x(q[0]);
                qc.h(q[1]);
                qc.h(q[2]);
                qc.ccx(q[1],q[2],q[0]);
                qc.x(q[1]);
                
                #qc.barrier(q)



            elif (inote-1)%2==1:
                
                theta = pi * slider_global.get()
                for i in range(3, 6):  # q[3], q[4], q[5]
                    qc.append(UGate(theta, 0, 0), [q[i]])

                qc.x(q[3]);
                qc.h(q[4]);
                qc.h(q[5]);
                qc.ccx(q[4],q[5],q[3]);
                qc.x(q[4]);

                
                
                #qc.barrier(q)

    def gate_VIm7(q,inote):
        #http://quantum.classcat.com/2018/02/05/qiskit-tutorial-2-4_quantum_info_two_qubit_qrac/

        if (Nqb_half>=3):
            if (inote-1)%2==0: 

                theta = pi * slider_global.get()
                for i in range(3):  # i = 0, 1, 2
                    qc.append(UGate(theta, 0, 0), [q[i]])
                
                qc.h(q[0]);
                qc.x(q[1]);
                qc.h(q[2]);
                qc.ccx(q[0],q[2],q[1]);
                
                #qc.barrier(q)



            elif (inote-1)%2==1:
                
                theta = pi * slider_global.get()
                for i in range(3, 6):  # q[3], q[4], q[5]
                    qc.append(UGate(theta, 0, 0), [q[i]])

                
                qc.h(q[3]);
                qc.x(q[4]);
                qc.h(q[5]);
                qc.ccx(q[3],q[5],q[4]);

                
                
                #qc.barrier(q)


           #return qProg

    def gate_VIIm7b5(q,inote):
        #http://quantum.classcat.com/2018/02/05/qiskit-tutorial-2-4_quantum_info_two_qubit_qrac/

        if (Nqb_half>=3):
            if (inote-1)%2==0: 

                theta = pi * slider_global.get()
                for i in range(3):  # i = 0, 1, 2
                    qc.append(UGate(theta, 0, 0), [q[i]])
                
                qc.h(q[0]);
                qc.h(q[1]);
                qc.x(q[2]);
                qc.ccx(q[0],q[1],q[2]);
                qc.x(q[1]);
                qc.ccx(q[0],q[2],q[1]);
                qc.ccx(q[1],q[2],q[0]);

                
                #qc.barrier(q)



            elif (inote-1)%2==1:
                
                theta = pi * slider_global.get()
                for i in range(3, 6):  # q[3], q[4], q[5]
                    qc.append(UGate(theta, 0, 0), [q[i]])

                qc.h(q[3]);
                qc.h(q[4]);
                qc.x(q[5]);
                qc.ccx(q[3],q[4],q[5]);
                qc.x(q[4]);
                qc.ccx(q[3],q[5],q[4]);
                qc.ccx(q[4],q[5],q[3]);
                
                #qc.barrier(q)
            

    def gate_phase(q,inote):
        #http://quantum.classcat.com/2018/02/05/qiskit-tutorial-2-4_quantum_info_two_qubit_qrac/

        th_global=slider_global.get();
        
        if (inote==1):
            
            #qc.append(UGate(pi * slider[0].get(), 0, 0), [q[2]])
            #qc.append(UGate(pi * slider[1].get(), 0, 0), [q[5]])

            
            qc.h(q[0]);  # lower degit
            qc.h(q[1]);
            qc.h(q[2]); # upper degit
            qc.h(q[3]);  # lower degit
            qc.h(q[4]);
            qc.h(q[5]); # upper degit
                        
            """
            ### QFT ############
            a=q[2]; # upper degit in input, lower degit in output  
            ap=q[1]
            b=q[0]; # lower degit in input, upper degit in output
            qc.h(a);
            qc.cp(math.pi/2,a,ap);
            qc.cp(math.pi/4,a,b);
            qc.h(ap);
            qc.cp(math.pi/2,ap,b);
            qc.h(b);
            
            ### QFT ############
            a=q[5]; # upper degit in input, lower degit in output
            ap=q[4]
            b=q[3]; # lower degit in input, upper degit in output
            qc.h(a);
            qc.cp(math.pi/2,a,ap);
            qc.cp(math.pi/4,a,b);
            qc.h(ap);
            qc.cp(math.pi/2,ap,b);
            qc.h(b);
            """
            
            
            ###Phase ############
            qc.barrier(q)
            th=(slider[0].get() + var_btn[0].get()/4 ) * math.pi;
            qc.p(th*4, q[0])#upper degit
            qc.p(th*2, q[1])
            qc.p(th*1, q[2])
            
            th=(slider[1].get() + var_btn[1].get()/4 ) * math.pi;
            qc.p(th*4, q[3])#upper degit
            qc.p(th*2, q[4])
            qc.p(th*1, q[5]) #lower degit
            
            ###Inverse QFT ############
            qc.barrier(q)
            a=q[0]; # upper degit in input, lower degit in output
            ap=q[1]
            b=q[2]; # lower degit in input, upper degit in output
            qc.h(a);
            qc.cp(-math.pi/2,a,ap);
            qc.cp(-math.pi/4,a,b);
            qc.h(ap);
            qc.cp(-math.pi/2,ap,b);
            qc.h(b);

            
            ###Inter-note Gate #############
            qc.barrier(q)

            
            qc.cp(-th_global*math.pi*8/32,q[0],q[5]);
            qc.cp(-th_global*math.pi*8/16,q[1],q[5]);
            qc.cp(-th_global*math.pi*8/8,q[2],q[5]);
            
            qc.cp(-th_global*math.pi*8/16,q[0],q[4]);
            qc.cp(-th_global*math.pi*8/8,q[1],q[4]);
            qc.cp(-th_global*math.pi*8/4,q[2],q[4]);
            
            qc.cp(-th_global*math.pi*8/8,q[0],q[3]);
            qc.cp(-th_global*math.pi*8/4,q[1],q[3]);
            qc.cp(-th_global*math.pi*8/2,q[2],q[3]);
          
            
            ###Inverse QFT ############
            qc.barrier(q)

            a=q[3];
            ap=q[4]
            b=q[5];
            qc.h(a);
            qc.cp(-math.pi/2,a,ap);
            qc.cp(-math.pi/4,a,b);
            qc.h(ap);
            qc.cp(-math.pi/2,ap,b);
            qc.h(b);


        
        elif (inote>=2):
            
            
            if (inote-1)%2==0: 
                qc.barrier(q)
                
                qc.reset(q[3])
                qc.reset(q[4])
                qc.reset(q[5])
                
                qc.h(q[3]);
                qc.h(q[4]);
                qc.h(q[5]);
                #qc.append(UGate(pi * slider[inote].get(), 0, 0), [q[5]])

                """
                ###QFT ############
                qc.barrier(q)

                a=q[5];
                ap=q[4]
                b=q[3];

                qc.h(a);
                qc.cp(math.pi/2,a,ap);
                qc.cp(math.pi/4,a,b);
                qc.h(ap);
                qc.cp(math.pi/2,ap,b);
                qc.h(b);
                """
            
                
                ###Phase Gate #############
                qc.barrier(q)

                th=(slider[inote+1-1].get() + var_btn[inote+1-1].get()/4 ) * math.pi;
                qc.p(th*4, q[3])
                qc.p(th*2, q[4])
                qc.p(th*1, q[5])
            
               ###Inter-note Gate #############
                qc.barrier(q)
                
                qc.cp(-th_global*math.pi*8/32,q[0],q[5]);
                qc.cp(-th_global*math.pi*8/16,q[1],q[5]);
                qc.cp(-th_global*math.pi*8/8,q[2],q[5]);
            
                qc.cp(-th_global*math.pi*8/16,q[0],q[4]);
                qc.cp(-th_global*math.pi*8/8,q[1],q[4]);
                qc.cp(-th_global*math.pi*8/4,q[2],q[4]);
            
                qc.cp(-th_global*math.pi*8/8,q[0],q[3]);
                qc.cp(-th_global*math.pi*8/4,q[1],q[3]);
                qc.cp(-th_global*math.pi*8/2,q[2],q[3]);
                

                
                
                ###Inverse QFT ############
                qc.barrier(q)

                a=q[3];
                ap=q[4]
                b=q[5];

                qc.h(a);
                qc.cp(-math.pi/2,a,ap);
                qc.cp(-math.pi/4,a,b);
                qc.h(ap);
                qc.cp(-math.pi/2,ap,b);
                qc.h(b);
                
 
            elif (inote-1)%2==1:

                qc.barrier(q)
                
                qc.reset(q[0])
                qc.reset(q[1])
                qc.reset(q[2])
                
                qc.h(q[0]);
                qc.h(q[1]);
                qc.h(q[2]);
                
                #qc.u3(pi*slider[inote+1-1].get(),0,0,q[2]);
                #theta = pi * slider[inote].get()
               # qc.append(UGate(theta, 0, 0), [q[2]])

                """
                ###QFT ############
                qc.barrier(q)

                a=q[2];
                ap=q[1]
                b=q[0];

                qc.h(a);
                qc.cp(math.pi/2,a,ap);
                qc.cp(math.pi/4,a,b);
                qc.h(ap);
                qc.cp(math.pi/2,ap,b);
                qc.h(b);
                """
                
                
                ###Phase Gate #############
                qc.barrier(q)

                th=(slider[inote+1-1].get() + var_btn[inote+1-1].get()/4 ) * math.pi;
                qc.p(th*4, q[0])
                qc.p(th*2, q[1])
                qc.p(th*1, q[2])
            
               ###Inter-note Gate #############
                qc.barrier(q)
                
                qc.cp(-th_global*math.pi*8/32,q[3],q[2]);
                qc.cp(-th_global*math.pi*8/16,q[4],q[2]);
                qc.cp(-th_global*math.pi*8/8,q[5],q[2]);
            
                qc.cp(-th_global*math.pi*8/16,q[3],q[1]);
                qc.cp(-th_global*math.pi*8/8,q[4],q[1]);
                qc.cp(-th_global*math.pi*8/4,q[5],q[1]);
            
                qc.cp(-th_global*math.pi*8/8,q[3],q[0]);
                qc.cp(-th_global*math.pi*8/4,q[4],q[0]);
                qc.cp(-th_global*math.pi*8/2,q[5],q[0]);

                
                                            
                ###Inverse QFT ############
                qc.barrier(q)

                a=q[0];
                ap=q[1]
                b=q[2];

                qc.h(a);
                qc.cp(-math.pi/2,a,ap);
                qc.cp(-math.pi/4,a,b);
                qc.h(ap);
                qc.cp(-math.pi/2,ap,b);
                qc.h(b);
                #qc.barrier(q)
                #qc.x(b)
                #qc.x(q[2]);

        
            #return qProg



    def gate_phase2(q,inote):

        th_global=slider_global.get() * math.pi;
        
        if (inote==1):
            qc.h(q[0]);
            qc.h(q[1]);
            qc.h(q[2]);
            qc.h(q[3]);
            qc.h(q[4]);
            qc.h(q[5]);

            th=slider[0].get() * math.pi;
            qc.p(th*4, q[0])
            qc.p(th*2, q[1])
            qc.p(th*1, q[2])
            
            
            th=slider[1].get() * math.pi;
            qc.p((th+th_global)*4, q[3])
            qc.p((th+th_global)*2, q[4])
            qc.p((th+th_global)*1, q[5])
            
            ###Inverse QFT ############
            a=q[0];
            ap=q[1]
            b=q[2];
            qc.h(a);
            qc.cp(-math.pi/2,a,ap);
            qc.cp(-math.pi/4,a,b);
            qc.h(ap);
            qc.cp(-math.pi/2,ap,b);
            qc.h(b);

            ###Inverse QFT ############
            a=q[3];
            ap=q[4]
            b=q[5];
            qc.h(a);
            qc.cp(-math.pi/2,a,ap);
            qc.cp(-math.pi/4,a,b);
            qc.h(ap);
            qc.cp(-math.pi/2,ap,b);
            qc.h(b);

            
            ###Inter-note Inverse QFT #############
            qc.barrier(q)
            qc.cp(-math.pi/2,q[0],q[3]);
            qc.cp(-math.pi/2,q[1],q[4]);
            qc.cp(-math.pi/2,q[2],q[5]);
            qc.h(q[3]);
            qc.h(q[4]);
            qc.h(q[5]);

            qc.barrier(q)



        
        elif (inote>=2):
            
            
            if (inote-1)%2==0: 
                
                qc.h(q[3]);
                qc.h(q[4]);
                qc.h(q[5]);

                ###Phase Gate #############
                th=slider[inote+1-1].get() * math.pi;
                qc.p((th+th_global*inote)*4,q[3]);
                qc.p((th+th_global*inote)*2,q[4]);
                qc.p((th+th_global*inote)*1,q[5]);

                
                ###Inverse QFT ############
                a=q[3];
                ap=q[4]
                b=q[5];

                qc.h(a);
                qc.cp(-math.pi/2,a,ap);
                qc.cp(-math.pi/4,a,b);
                qc.h(ap);
                qc.cp(-math.pi/2,ap,b);
                qc.h(b);
                #qc.barrier(q)
                #qc.x(b)
                #qc.x(q[2]);

                
               ###Inter-note Gate #############
                qc.barrier(q)
                
                #qc.h(q[0]);
                #qc.h(q[1]);
                #qc.h(q[2]);
        
                qc.cp(-math.pi/2,q[0],q[3]);
                qc.cp(-math.pi/2,q[1],q[4]);
                qc.cp(-math.pi/2,q[2],q[5]);
                
                qc.h(q[3]);
                qc.h(q[4]);
                qc.h(q[5]);

                qc.barrier(q)

                            
                
 
            elif (inote-1)%2==1:


                qc.h(q[0]);
                qc.h(q[1]);
                qc.h(q[2]);

                ###Phase Gate #############
                th=slider[inote+1-1].get() * math.pi;
                qc.p((th+th_global*inote)*4, q[0])
                qc.p((th+th_global*inote)*2, q[1])
                qc.p((th+th_global*inote)*1, q[2])

                ###Inverse QFT ############
                a=q[0];
                ap=q[1]
                b=q[2];

                qc.h(a);
                qc.cp(-math.pi/2,a,ap);
                qc.cp(-math.pi/4,a,b);
                qc.h(ap);
                qc.cp(-math.pi/2,ap,b);
                qc.h(b);
                #qc.barrier(q)
                #qc.x(b)
                #qc.x(q[2]);

               ###Inter-note Gate #############
                qc.barrier(q)
                #qc.h(q[3]);
                #qc.h(q[4]);
                #qc.h(q[5]);
        
                qc.cp(-math.pi/2,q[3],q[0]);
                qc.cp(-math.pi/2,q[4],q[1]);
                qc.cp(-math.pi/2,q[5],q[2]);
                
                qc.h(q[0]);
                qc.h(q[1]);
                qc.h(q[2]);

                qc.barrier(q)

                        
        
    ############################################################### 
    def gate_asignment(q,inote):
        
        var=var_btn[inote-1].get();
        init=bln_ini[inote-1].get();
        #th=slider[inote-1].get() * math.pi;
        
        print("var=",var," ","init=",init);

        if var_mode==0:

            if var==0:
                gate_single_cx02(q,inote,0,init);
            elif var==1:
                gate_single_cx02(q,inote,1,init);
            elif var==2:
                gate_single_cx02(q,inote,2,init);
            elif var==3:
                gate_single_cx02(q,inote,3,init);
            elif var==4:
                gate_single_cx02(q,inote,4,init);
            elif var==5:
                gate_single_cx02(q,inote,5,init);
            elif var==6:
                gate_single_cx02(q,inote,1,init);

                
        elif var_mode==1:

            if var==0:
                gate_double_cx01(q,inote,0,init);
            elif var==1:
                gate_double_cx01(q,inote,1,init);
            elif var==2:
                gate_double_cx01(q,inote,2,init);
            elif var==3:
                gate_double_cx01(q,inote,3,init);
            elif var==4:
                gate_double_cx01(q,inote,4,init);
            elif var==5:
                gate_double_cx01(q,inote,5,init);
                        
        elif var_mode==2:

            if var==0:
                gate_IM7(q,inote);
            elif var==1:
                gate_IIm7(q,inote);
            elif var==2:
                gate_IIIm7(q,inote);
            elif var==3:
                gate_IVM7(q,inote);
            elif var==4:
                gate_V7(q,inote);
            elif var==5:
                gate_VIm7(q,inote);
            elif var==6:
                gate_VIIm7b5(q,inote);
                                               
        elif var_mode==3:

            gate_phase(q,inote);
            #gate_phase2(q,inote);
        
                    
    ############################################################### 
    def gate_asignment_mode4(q,inote):
        
        print("var_mode=", var_mode);
        
        varA=var_btn[(inote-1)*2].get();
        varB=var_btn[(inote-1)*2+1].get();  
        
        thA=slider[(inote-1)*2].get() * math.pi;
        thB=slider[(inote-1)*2+1].get() * math.pi;
        phA=slider2[(inote-1)*2].get() * math.pi;
        phB=slider2[(inote-1)*2+1].get() * math.pi;
        
        
        
        initA=bln_ini[(inote-1)*2].get();
        initB=bln_ini[(inote-1)*2+1].get();
        #th=slider[inote-1].get() * math.pi;
        
        gate_game(q,inote,thA,thB,phA,phB,initA,initB);
        
        print(thA/pi,thB/pi,phA/pi,phB/pi,varA,varB,initA,initB);
        

    ###############################################################        
    ###############################################################        
    
            
    with open("quantum_measurements.dat", "w") as f:
            print(Nqb_half,Nnote_shots//10,Nnote_shots%10, Nbar//10,Nbar%10, var_mode, file=f)        
            
    ######Initial note#################
    if var_mode==0 or var_mode==1:
        qc.h(q[0]);    

    # If the selected mode is not Mode 4, apply standard gate assignment
    if var_mode != 4:
        for inote in range(1, Nbar + 1):  # Loop through each bar (musical measure)
            print("inote =", inote)

            # --- Quantum circuit section for this bar ---
            qc.barrier(q)                   # Insert a barrier before gate operations
            gate_asignment(q, inote)        # Apply gate pattern for current bar
            qc.barrier(q)                   # Insert a barrier before measurement
            measure_print(inote)            # Perform measurement and reset qubits
            # --------------------------------------------

    # If the selected mode is Mode 4 (special handling for quantum game / phase modulation)
    if var_mode == 4:
        for inote in range(1, Nbar + 1):  # Loop through each bar as in other modes
            print(inote)

            # --- Quantum circuit section for Mode 4 ---
            qc.barrier(q)                         # Insert barrier before special gate logic
            gate_asignment_mode4(q, inote)        # Apply Mode 4 specific gate logic
            qc.barrier(q)                         # Insert barrier before measurement
            measure_print(inote)                  # Perform measurement and reset qubits
            # -------------------------------------------


    #job_sim = execute(qc, backend_sim,shots=Nnote_shots)
    #result_sim = job_sim.result()
    #print(result_sim.get_counts(qc))
    #a=result_sim.get_counts(qc)

    
    # See a list of available local simulators
    print("Aer backends: ", Aer.backends())

    # Compile and run the Quantum circuit on a simulator backend
    backend_sim = Aer.get_backend('qasm_simulator')

    backend_sim = AerSimulator()
    job_sim = backend_sim.run(qc, shots=Nnote_shots)
    
    result_sim = job_sim.result()
    counts = result_sim.get_counts()
    print(counts)
    a = counts

    
    with open("quantum_measurements.dat", "a") as f:
        for sp_key in a:
            print(sp_key, file=f)        

    with open("quantum_note_mapping.dat", "w") as f2:
        if var_mode!=4:
            for inote in range(1,Nbar+1,1):
                var=var_btn[inote-1].get()
                print(var, file=f2)        
        if var_mode==4:
            for inote in range(1,2*Nbar+1,1):
                var=var_btn[inote-1].get()
                print(var, file=f2)        

    plot_histogram(a);
    #############################################################################
    
    if bln_drawer.get():
        print('circuit drawer checked--')
        qc.draw(output='mpl', filename='circuit_diagram.png');
    else:
        print('circuit drawer not checked')
    
    #circuit_drawer(qc)
    #np.savetxt("test.dat", result_sim.get_counts(qc), fmt="%.4f" )
    #selectedIndex = tk.ACTIVE
    
    #Delete the listbox
    ListBox1.delete(0,tk.END)
    
    for sp_key in a:
        #ListBox1.insert(tk.END, result_sim.get_counts(qc));
        ListBox1.insert(tk.END, sp_key);

##########################################################################################
##===============================================================================-

