#!/bin/bash
# Enter ipmi ip address, username, and password
IPADDR=192.168.1.x
USER=root
PASSWORD=calvin
#IPMIBASE="ipmitool -I lanplus -H $IPADDR -U $USER -P $PASSWORD raw 0x30 0x30"
IPMIBASE="ipmitool raw 0x30 0x30"

# Define the fan curve as an array of temperature/fan speed pairs
# The fan speed values should be in decimal format (0-100)
FAN_CURVE=( [0]=15 [35]=25 [40]=35 [50]=40 [55]=50 [80]=64 )

# Enable manual fan control
$IPMIBASE 0x01 0x00

# Set the IPMI tool command to adjust the fan speed
FAN_CMD="$IPMIBASE 0x02 0xff"

# Initialize the fan speed to 0
FAN_SPEED=0

# Initialize the CPU temperature to 0
CPU_TEMP=0

# Loop indefinitely to monitor CPU temperatures
while true
do
  # Read the CPU temperature using lm-sensors
  NEW_CPU_TEMP=$(sensors | grep 'Package id 0:' | awk '{print $4}' | cut -c 2- | awk '{printf "%.0f\n", $1}')

  # Print the CPU temperature to the console if it has changed
  #if [ $NEW_CPU_TEMP -ne $CPU_TEMP ]
  if [ -n "$NEW_CPU_TEMP" ] && [ "$NEW_CPU_TEMP" -ne "$CPU_TEMP" ]; then
  then
    echo "CPU Temperature: $NEW_CPU_TEMP°C"
    CPU_TEMP=$NEW_CPU_TEMP
  fi

  # Find the fan speed corresponding to the current temperature
  for TEMP in "${!FAN_CURVE[@]}"
  do
    if [ $CPU_TEMP -ge $TEMP ]
    then
      NEW_FAN_SPEED=${FAN_CURVE[$TEMP]}
    else
      break
    fi
  done

  # Set the fan speed using IPMI tool if it has changed
  if [ $NEW_FAN_SPEED -ne $FAN_SPEED ]
  then
    echo "Setting fan speed to $NEW_FAN_SPEED"
    $FAN_CMD $NEW_FAN_SPEED
    FAN_SPEED=$NEW_FAN_SPEED
  fi

  # Wait for 5 seconds before checking the temperature again
  sleep 5
done
