﻿from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
import Live


class Eq8Manager(ControlSurfaceComponent):
    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        self._last_selected_track = self.song().view.selected_track
        self.song().view.add_selected_track_listener(self.on_selected_track_changed)

    def eq_loader(self):
        for device in list(self.song().view.selected_track.devices):
            if device.name == "VMX Equalizer":
                return
        for child in self.application().browser.audio_effects.iter_children:
            if child.name == "EQ Eight":
                self.application().browser.load_item(child)
                break
        device = self.song().view.selected_track.devices[-1]
        if device.name == "EQ Eight":
            pass
            Live.Base.log(device.name)
            device.name = "VMX Equalizer"
            for parameter in device.parameters:
                if "Filter On" in parameter.name:
                    parameter.value = 1.0
                if "Filter Type" in parameter.name:
                    if 0 < int(parameter.name[0]) < 8:
                        parameter.value = 3
                    elif int(parameter.name[0]) == 8:
                        parameter.value = 5
                if "Frequency A" in parameter.name:
                    parameter.value = (int(parameter.name[0]) - 1) / 7

    def eq_unloader(self, track=None):
        Live.Base.log("eq_unloader is track none: " + str(track is None))
        if track is None:
            track = self.song().view.selected_track
        for i, device in enumerate(list(track.devices)):
            if device.name == "VMX Equalizer" and [parameter.value == 1.0 for parameter in device.parameters if "Filter On A" in parameter.name] == [True] * 8 and [round(parameter.value, 1) == round((int(parameter.name[0]) - 1) / 7, 1) for parameter in device.parameters if "Frequency A" in parameter.name] == [True] * 8:
                track.delete_device(i)

    def on_selected_track_changed(self):
        Live.Base.log(self._last_selected_track.name)
        Live.Base.log(str(self._last_selected_track in self.song().tracks))
        if self.song().view.selected_track != self._last_selected_track:  # and "equalizer" in self.menu_manager.current_menus:
            for track in self.song().tracks:
                if track == self._last_selected_track:
                    self.eq_unloader(track)
            self._last_selected_track = self.song().view.selected_track
            self.eq_loader()
