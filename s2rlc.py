import skrf as rf
import numpy as np
import math
import pandas as pd
import os
import argparse

def S2RLC(file_path, result_path):

    network = rf.Network(file_path)
    S = network.s
    Y = network.y
    Z = network.z
    Nport = network.nports
    Nf = len(network.f)
    port_names = network.port_names
    network_freq = network.f

    L_eff = np.zeros((Nport, Nf))
    C_eff = np.zeros((Nport, Nf))
    R_eff = np.zeros((Nport, Nf))

    for i in range(Nf):
        freq = network.f[i]
        jw = 2 * math.pi * freq

        # calculate the resistance from Y = 1 / (R + jwL)
        # R = re(1/Y(1, 1)) Ohms
        Yf = np.reshape(Y[i], (Nport, Nport))
        Yf_data = 1 / np.diagonal(Yf)
        R_eff[:,i] = Yf_data.real

        # # calculate the inductance from Y = 1 / (R + jwL)
        # # L = im(1/Y(1, 1)) / (2*pi*F) * 1e9 nH
        L_eff[:,i] = Yf_data.imag / jw * 1e9

        # # calculate the capacitance from Z = 1 / (G + jwC)
        # # C = im(1/Z(1, 1)) / (2*pi*F) * 1e12 pF
        Zf = np.reshape(Z[i], (Nport, Nport))
        Zf_data = 1 / np.diagonal(Zf)
        C_eff[:,i] = Zf_data.imag / jw * 1e12


    R_df = pd.DataFrame(R_eff.T, index=network_freq, columns=port_names)
    L_df = pd.DataFrame(L_eff.T, index=network_freq, columns=port_names)
    C_df = pd.DataFrame(C_eff.T, index=network_freq, columns=port_names)

    # if not os.path.exists(result_directory):
    #     os.mkdir(result_directory)


    writer = pd.ExcelWriter(result_path)

    R_df.to_excel(writer, sheet_name="ESR-Ohm")
    L_df.to_excel(writer, sheet_name="ESL-nH")
    C_df.to_excel(writer, sheet_name="ESC-pF")
    writer.save()
    # R_df.to_csv(os.path.join(result_directory, "esr.csv"))
    # L_df.to_csv(os.path.join(result_directory, "esl.csv"))
    # C_df.to_csv(os.path.join(result_directory, "esc.csv"))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert S parameter to RLC")

    parser.add_argument("-s", dest="sparameter", help="touchstone file path")
    parser.add_argument("-r", dest="result", help="result folder path")
    args = parser.parse_args()

    S2RLC(args.sparameter, args.result)

    # S2RLC("demo.s22p", "./results.xlsx")
