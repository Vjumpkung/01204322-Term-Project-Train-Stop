def do_connect(SSID, PASSWORD):
    import network

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
        print()
    print("Wifi Connected")
    print("network config:", sta_if.ifconfig())


# put it into boot.py (by import wifi_connect)
