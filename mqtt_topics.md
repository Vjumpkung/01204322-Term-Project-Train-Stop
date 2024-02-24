# MQTT Topics

## Lookouts

continual report (period of 250 ms or less)

- publishers
  - sensor boards (process values from sensors and publish continually)
- subscribers
  - control board (subscribe and save locally for control logic)
  - web ui (subscribe and save locally for display)

### Topics

- crossing1/lookouts/west/far
- crossing1/lookouts/west/near
- crossing1/lookouts/east/near
- crossing1/lookouts/east/far

### Values

- "0" => not detected
- "1" => detected

## State

spontaneous report

- publishers
  - control board (save locally for control logic and publish on change)
- subscribers
  - web ui (subscribe and save locally for display)

### Topics

- crossing1/state

### Values

- "0", => no train
- "eb0", "eb1", "eb2", "eb3", "eb4", "eb5", => train going east
- "wb0", "wb1", "wb2", "wb3", "wb4", "wb5" => train going west

## Gates

spontaneous command

- publishers
  - control board (save locally for display and publish on auto/manual gate control command)
  - web ui (save locally for display and publish on manual gate control command)
- subscribers
  - gate boards (subscribe and save locally for servo, buzzer, and LED control)
  - control board (subscribe and save locally for display)
  - web ui (subscribe and save locally for display)

### Topics

- crossing1/gates/north
- crossing1/gates/south

### Values

- "0" => close
- "1" => open

## Mode

spontaneous command

- publishers
  - control board (save locally for control logic, display and publish on manual mode change command)
  - web ui (save locally for manual gate control, display and publish on manual mode change command)
- subscribers
  - control board (subscribe and save locally for control logic and display)
  - web ui (subscribe and save locally for manual gate control and display)

### Topics

- crossing1/mode

### Values

- "A" => Auto
- "M" => Manual
