#!/usr/bin/env python3
# coding: utf-8
#
# Copyright (c) 2021 Gardena GmbH

"""SciKit-RF model for an N-port symmetrical resistive power splitter."""

import sys
import math
import skrf as rf
from matplotlib import pyplot

if len(sys.argv) <= 1:
    print(f"usage: {sys.argv[0]} <N> [error in %]")
    sys.exit(1)

N = int(sys.argv[1])
if len(sys.argv) >= 3:
    error = float(sys.argv[2])
else:
    error = 0

Z0 = 50
R = Z0 * (N - 1) / (N + 1)
R_ = R + error / 100 * R
loss = 10 * math.log10(1 / N**2)
print("N=%d, R=%.2fΩ, ideal loss=%.2f dB" % (N, R, loss))
if error != 0:
    print("error=%.1f%%, R_=%.2fΩ" % (error, R_))


NUM_RESISTORS = N + 1
NUM_PORTS = 2
NUM_TERMINATORS = NUM_RESISTORS - NUM_PORTS

freq = rf.Frequency(start=0.1, stop=3, unit='GHz', npoints=1001)
m = rf.media.DefinedGammaZ0(frequency=freq, z0=Z0)
resistors = [m.resistor(R_, name=f"R{i+1}") for i in range(NUM_RESISTORS)]
terminators = [m.resistor(Z0, name=f"R{i+1+NUM_RESISTORS}") for i in range(NUM_TERMINATORS)]
ports = [rf.Circuit.Port(freq, name=f"Port{i+1}", z0=Z0) for i in range(NUM_PORTS)]
grounds = [rf.Circuit.Ground(freq, name=f'GND[{i+1}]') for i in range(NUM_TERMINATORS)]


connections = [
    # central connection of power splitter resistors
    [(r, 0) for r in resistors],
    # connections of terminated resistors to terminators
    *[[(resistors[i], 1), (terminators[i], 0)] for i in range(NUM_TERMINATORS)],
    # connection of terminators to ground
    *[[(terminators[i], 1), (grounds[i], 0)] for i in range(NUM_TERMINATORS)],
    # connection of unterminated resistors to ports
    *[[(ports[i], 0), (resistors[i+NUM_TERMINATORS], 1)] for i in range(NUM_PORTS)]
]

circuit = rf.Circuit(connections)
network = circuit.network

print("S12[865 MHz] = %.2f dB" % network['865MHz'].s_db[0][0][1])


# circuit.plot_graph(network_labels=True, network_fontsize=15,
#                    port_labels=True, port_fontsize=15,
#                    edge_labels=True, edge_fontsize=10)

pyplot.figure()
network.plot_s_db()
# network.plot_s_db(n=0, m=1)

# pyplot.figure()
# network.plot_s_smith(draw_labels=True)
# rf.plotting.add_markers_to_lines()

pyplot.show()
