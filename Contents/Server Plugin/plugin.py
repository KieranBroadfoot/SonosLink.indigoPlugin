#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2015, Kieran J. Broadfoot. All rights reserved.
# http://kieranbroadfoot.com
#

################################################################################
# Imports
################################################################################
import sys
import os
import time
import re

################################################################################
class Plugin(indigo.PluginBase):

    ########################################
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs): 
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.defaultRadio = pluginPrefs.get("sonosRadio", "x-sonosapi-stream:s24940?sid=254&flags=32")
        self.sonosPlugin = indigo.server.getPlugin("com.ssi.indigoplugin.Sonos")
        self.initStates()
        indigo.devices.subscribeToChanges()
        
    def initStates(self):
        for player in indigo.devices.iter("com.ssi.indigoplugin.Sonos.ZonePlayer"):
            # for each player let's set the c-bus channels accordingly
            channel = self.getAssociatedGroup(player)
            if player.states["ZP_STATE"] == "PLAYING":
                self.updateChannel(channel, int(player.states["ZP_VOLUME"]))
            if player.states["ZP_STATE"] == "PAUSED" or player.states["ZP_STATE"] == "STOPPED":
                self.updateChannel(channel, 0)

    def getAssociatedGroup(self, device):
        channelAddr = device.globalProps["com.indigodomo.indigoserver"].get("cbus", None)
        for group in indigo.devices.iter("uk.co.l1fe.indigoplugin.C-Bus"):
            if group.address == channelAddr:
                return group

    def updateChannel(self, channel, brightness):
        if brightness <= 95:
            indigo.dimmer.setBrightness(channel, brightness)
        
    def deviceUpdated(self, old, new):
        if new.model == "Sonos Zone Player":
            channel = self.getAssociatedGroup(new)
            if new.states["ZP_STATE"] == "PLAYING":
                vol = int(new.states["ZP_VOLUME"])
                if channel.brightness != vol and abs(channel.brightness-vol) > 5:
                    self.updateChannel(channel, int(new.states["ZP_VOLUME"]))
                    return
            if new.states["ZP_STATE"] == "PAUSED" or new.states["ZP_STATE"] == "STOPPED":
                if channel.brightness != 0:
                    self.updateChannel(channel, 0)
                    return

    def updateSonos(self, action, dev):
        if not action.props.get("sonosZone",""):
            indigo.server.log("SonosLink Update: No zone ID provided.")
            return
        player = indigo.devices[action.props.get("sonosZone","")]
        channel = self.getAssociatedGroup(player)
        if player.states["ZP_STATE"] == "PLAYING":
            if channel.brightness == 0:
                if ',' in player.states['ZonePlayerUUIDsInGroup']:
                    # if zone is playing and brightness is 0 and currently linked then unlink
                    self.sonosPlugin.executeAction("actionZP_setStandalone", deviceId=player.id)
                    return
                else:
                    # if zone is playing and brightness is 0 then pause
                    self.sonosPlugin.executeAction("actionPause", deviceId=player.id)
                    return
            else:
                # if zone is playing then set volume
                self.sonosPlugin.executeAction("actionVolume", deviceId=player.id, props={'setting':channel.brightness})
                return
        if player.states["ZP_STATE"] == "PAUSED":
            # if player is paused then we can presume a queue is present and hence should be started again
            # need to handle special case for line-in.  if the line-in is currently set then this is the same behaviour as stopped
            self.sonosPlugin.executeAction("actionPlay", deviceId=player.id)
            self.sonosPlugin.executeAction("actionVolume", deviceId=player.id, props={'setting':channel.brightness})
            return
        if player.states["ZP_STATE"] == "STOPPED":
            found = 0
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos.ZonePlayer"):
                if dev.states["ZP_STATE"] == "PLAYING":
                    # if zone is not playing but somewhere else is then link
                    found = 1
                    self.sonosPlugin.executeAction("actionZP_addPlayerToZone", deviceId=dev.id, props={'setting':player.id})
                    return
            if found == 0:
                # if zone is not playing and no-where else is then start radio
                self.sonosPlugin.executeAction("actionZP_RT_FavStation", deviceId=player.id, props={'setting':self.defaultRadio})
                return

    def sonosZoneList(self, filter="", valuesDict=None, typeId="", targetId=0):
        zones = []
        for player in indigo.devices.iter("com.ssi.indigoplugin.Sonos.ZonePlayer"):
            zones.append([player.name, player.name])
        return sorted(zones, key=lambda x: x[1])