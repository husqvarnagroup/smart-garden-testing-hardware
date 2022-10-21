# BNW Lemonbeat Dongle Design Goals

## Inspiration

The schematic is inspired by / copied from the schematic for the
[nRF52840 Dongle](https://www.nordicsemi.com/Products/Development-hardware/nrf52840-dongle)
hardware design files (v2.1.1) and the
[4467CPCE10D868 (aka Si4467 DK) design files](https://www.silabs.com/documents/public/schematic-files/4467CPCE10D868.zip).


## Design Goals and Planned Features

The BNW Lemonbeat dongle is planned as a tool for interaction with
Lemonbeat devices using the Zephyr stack. As such, it should support
the following features:

- nRF52840 MCU as main processor
- Si4467 transceiver with SMA connector for Lemonbeat communication
- (optionally) Bluetooth PCB antenna or u.FL connector (or similar)

### Design for Manufacturability

The design is meant to be manufactured by an EMS such as JLCPCB. Thus
some components will be chosen based on availability and
manufacturability.

### Non-Goals and Non-Features

The dongle is not intended as a replacement for the nRF52840 DK. The
following features are thus out of scope:

- on-board programmer (such as Black Magic Probe)
- on-board flash
- access to all GPIOs
- additional LEDs and buttons
