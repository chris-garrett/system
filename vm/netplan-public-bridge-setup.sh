# netplan-public-bridge-setup.sh
#!/bin/sh

USR=chris
GWAY=192.168.0.1
DNS="192.168.0.1, 8.8.8.8, 8.8.4.4, 1.1.1.1"
NOW=`date +%Y-%m-%dT%H-%M-%S`
BCK=../__backup__/$NOW

mkdir -p $BCK

#
# Must be root!
# 
USER=${EUID:-`id -u`}
if [ $USER -ne 0 ]; then
   echo "This script must be run as root" 
   exit 1
fi


#
# Move NetworkManager out of the way
# 
if [ -f /etc/netplan/01-network-manager-all.yaml ]; then
  mv /etc/netplan/01-network-manager-all.yaml /etc/netplan/01-network-manager-all.yaml.$NOW
fi

#
# Disabling netfilter for performance
# 
if [ -f /etc/sysctl.d/bridge.conf ]; then
  cp /etc/sysctl.d/bridge.conf $BCK/etc-sysctl.d-bridge.conf
fi

cat > /etc/sysctl.d/bridge.conf <<- EOM
net.bridge.bridge-nf-call-ip6tables=0
net.bridge.bridge-nf-call-iptables=0
net.bridge.bridge-nf-call-arptables=0
EOM

if [ -f /etc/sysctl.d/bridge.conf ]; then
  cp /etc/udev/rules.d/99-bridge.rules $BCK/etc-udev-rules.d-99-bridge.rules
fi
cat > /etc/udev/rules.d/99-bridge.rules <<- EOM
ACTION=="add", SUBSYSTEM=="module", KERNEL=="br_netfilter", RUN+="/sbin/sysctl -p /etc/sysctl.d/bridge.conf"
EOM

#
# Nuke default
#
if virsh net-info default > /dev/null 2>&1
then
  virsh net-destroy default
  virsh net-undefine default
fi

#
# Setup bridge (br0)
#
if [ -f /etc/netplan/00-installer-config.yaml ]; then
  cp /etc/netplan/00-installer-config.yaml $BCK/etc-netplan-00-installer-config.yaml
fi

cat > /etc/netplan/00-installer-config.yaml <<- EOM
network:
  version: 2
  renderer: networkd

  ethernets:
    enp38s0:
      dhcp4: false
      dhcp6: false
      addresses: [192.168.0.5/24]
      routes:
      - to: default
        via: $GWAY
        metric: 100
        on-link: true   
      nameservers:
        addresses: [$DNS]

    enp39s0:
      dhcp4: false
      dhcp6: false

  bridges:
    br0:
      interfaces: [ enp39s0 ]
      addresses: [ 192.168.0.6/24 ]
      routes:
      - to: default
        via: $GWAY
        metric: 200
        on-link: true      
      mtu: 1500
      nameservers:
        addresses: [ $DNS ]
      parameters:
        stp: true
        forward-delay: 4
      dhcp4: no
      dhcp6: no
EOM
chmod 600 /etc/netplan/*.yaml

sudo netplan apply

#
# Register bridge with virtmgr
#
cat > public-bridge.xml <<- EOM
<network>
  <name>public-bridge</name>
  <forward mode="bridge"/>
  <bridge name="br0"/>
</network>
EOM

if virsh net-info public-bridge > /dev/null 2>&1
then
  virsh net-destroy public-bridge
  virsh net-undefine public-bridge
fi

virsh net-define public-bridge.xml
virsh net-autostart public-bridge
virsh net-start public-bridge
rm public-bridge.xml

#
# To use this with qemu using qemu-bridge-helper:
# 
#     -netdev bridge,id=net0,br=br0,"helper=/usr/lib/qemu/qemu-bridge-helper" \
#     -device e1000-82545em,netdev=net0,id=net0,mac=52:54:00:c9:18:27 \
#
mkdir -p /etc/qemu

cat > /etc/qemu/bridge.conf <<- EOM
allow public-bridge
EOM
chown -R -vc root:kvm /etc/qemu
chmod -vc 0770 /etc/qemu
chmod -vc 0640 /etc/qemu/*

# its possible this will need to be reapplied after updates
chmod -vc u+s /usr/lib/qemu/qemu-bridge-helper

# add user to kvm so you dont have to sudo
usermod -a -G kvm `id $USR -un`


chown -R $USR:$USR $BCK

