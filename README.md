SonosLink.indigoPlugin
======================

Custom plugin to link/mirror Sonos Devices with C-Bus groups for [Indigo Domotics Indigo 7](http://www.indigodomo.com).  This provides control of Sonos from DLT switches.

Requirements
------------

This plugin requires:

* Indigo >= 7.0
* C-Bus Plugin >= 1.0
* Sonos Plugin >= 0.8.13
* Global Property Manager Plugin >= 1.0.2

Setup
-----

For each Sonos ZonePlayer use the Global Property Manager to define a custom attribute named "cbus" with a value of the C-Bus group address.  The plugin will automatically sync the c-bus group to Sonos once these properties are in place.  As of v1.0 this plugin has been integrated with my C-Bus plugin using Indigo broadcasts and therefore any previous actions to link C-Bus to Sonos are deprecated.

Behaviour
---------

When a group is manually changed on a C-Bus switch the plugin will update Sonos.  The behaviours are as follows:
 
* Zone paused and C-Bus set > 0 - Play
* Zone playing and C-Bus set to 0 - Pause
* Zone playing/linked and C-Bus set to 0 - Unlink Zone
* Zone playing and C-Bus ramped up/down - Volume Change
* Zone stopped, Queue not empty and C-Bus set > 0 - Play Local Queue 
* Zone stopped, Other Zone playing and C-Bus set > 0 - Link to Zone
* Zone stopped, No other zones playing and C-Bus set > 0 - Play Default Radio
