
# Reference Architecture

```text
Internet
   |
Edge Router
   |
Enterprise Firewall/NAT
   |
   +----------------------+----------------------+
   |                      |                      |
User VLAN 10         Server VLAN 20         Management 99
10.0.10.0/24         10.0.20.0/24          10.0.99.0/24
   |                      |
ws-23                app-01 / file-01
10.0.10.23           10.0.20.40
                          |
                     OT Firewall A
                          |
                      OT DMZ 30
                      10.0.30.0/24
                          |
                     OT Firewall B
                          |
                  Supervisory LAN 40
                      10.0.40.0/24
                          |
                       PLC / IED
```

CORP contains VLANs 10 and 20. OT contains VLANs 30 and 40. MGMT contains
VLAN 99. Only app-01 may initiate HTTPS to the OT historian in VLAN 30.
