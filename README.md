SonosLink.indigoPlugin
======================

Custom plugin to link/mirror Sonos Devices with C-Bus groups.  This provides control of Sonos from DLT switches.

Requirements
------------

This plugin requires:

* C-Bus Plugin >= 0.0.5
* Sonos Plugin >= 0.8.13
* Global Property Manager Plugin >= 1.0.0

The plugin currently presumes every Zone Player in your system has an associated C-Bus group available to be linked.

Setup
-----

### Sonos -> C-Bus

For each Sonos ZonePlayer use the Global Property Manager to define a custom attribute named "cbus" with a value of the C-Bus group address.  The plugin will automatically sync the c-bus group to Sonos once these properties are in place.

### C-Bus to Sonos

A trigger per Sonos zone is required to link user initiated changes in C-Bus to Sonos.  Each trigger should be configured as follows:

* Trigger: C-Bus Event - Group Manually Changed - Group: group_name, Change: Any
* Conditions: Always
* Action: SonosLink - Match Sonos to C-Bus Group - Zone: zone_name

Behaviour
---------

When a group is manually changed in C-Bus the plugin will update Sonos.  The behaviours are as follows:
 
* Zone paused and C-Bus set > 0 - Play
* Zone playing and C-Bus set to 0 - Pause
* Zone playing/linked and C-Bus set to 0 - Unlink Zone
* Zone playing and C-Bus ramped up/down - Volume Change
* Zone stopped, Queue not empty and C-Bus set > 0 - Play Local Queue 
* Zone stopped, Other Zone playing and C-Bus set > 0 - Link to Zone
* Zone stopped, No other zones playing and C-Bus set > 0 - Play Default Radio
