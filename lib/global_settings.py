#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.global_settings.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     10 Jun 2022, (6:52 PM)

    Copyright:
        Copyright (C) 2021 Josh Sunnex

        This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
        Public License as published by the Free Software Foundation, version 3.

        This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
        implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
        for more details.

        You should have received a copy of the GNU General Public License along with this program.
        If not, see <https://www.gnu.org/licenses/>.

"""


class GlobalSettings:

    def __init__(self, settings):
        self.settings = settings

    @staticmethod
    def options():
        # Global and main config options
        return {
            "main_options":           {
                "mode":                  "basic",
                "max_muxing_queue_size": 2048,
            },
            "encoder_selection":      {
                "video_codec":   "hevc",
                "video_encoder": "libx265",
            },
            "advanced_input_options": {
                "main_options":     "",
                "advanced_options": "-strict -2\n"
                                    "-max_muxing_queue_size 2048\n",
                "custom_options":   "-preset slow\n"
                                    "-tune film\n"
                                    "-global_quality 23\n"
                                    "-look_ahead 1\n",
            },
            "output_settings":        {
                "keep_container": True,
                "dest_container": "mkv",
            },
            "filter_settings":        {
                "apply_smart_filters":     False,
                "autocrop_black_bars":     False,
                "apply_custom_filters":    False,
                "custom_software_filters": "",
            },
        }

    def __set_default_option(self, select_options, key, default_option=None):
        """
        Sets the default option if the currently set option is not available

        :param select_options:
        :param key:
        :return:
        """
        available_options = []
        for option in select_options:
            available_options.append(option.get('value'))
            if not default_option:
                default_option = option.get('value')
        if self.settings.get_setting(key) not in available_options:
            self.settings.set_setting(key, default_option)

    def get_mode_form_settings(self):
        return {
            "label":          "Config mode",
            "input_type":     "select",
            "select_options": [
                {
                    'value': "basic",
                    'label': "Basic (Not sure what I am doing. Configure most of it for me.)",
                },
                {
                    'value': "standard",
                    'label': "Standard (I know how to transcode some video. Let me tweak some settings.)",
                },
            ],
        }
        # TODO: Enable advanced options
        # {
        #     'value': "advanced",
        #     'label': "Advanced - Dont tell me what to do, I write FFmpeg commands in my sleep",
        # },

    def get_max_muxing_queue_size_form_settings(self):
        values = {
            "label":          "Max input stream packet buffer",
            "input_type":     "slider",
            "slider_options": {
                "min": 1024,
                "max": 10240,
            },
        }
        if self.settings.get_setting('mode') not in ['standard', 'advanced']:
            values["display"] = 'hidden'
        return values

    def get_video_codec_form_settings(self):
        return {
            "label":          "Video Codec",
            "input_type":     "select",
            "select_options": [
                {
                    'value': "h264",
                    'label': "H264",
                },
                {
                    'value': "hevc",
                    'label': "HEVC/H265",
                },
            ],
        }

    def get_video_encoder_form_settings(self):
        values = {
            "label":          "Video Encoder",
            "input_type":     "select",
            "select_options": [],
        }
        if self.settings.get_setting('video_codec') == 'hevc':
            # TODO: Only enable VAAPI for Linux
            values['select_options'] = [
                {
                    'value': "libx265",
                    'label': "CPU - libx265",
                },
                {
                    'value': "hevc_qsv",
                    'label': "QSV - hevc_qsv",
                },
                {
                    'value': "hevc_vaapi",
                    'label': "VAAPI - hevc_vaapi",
                },
            ]
        elif self.settings.get_setting('video_codec') == 'h264':
            # TODO: Add support for VAAPI (requires some tweaking of standard values)
            # TODO: Enable libx264
            values['select_options'] = [
                {
                    'value': "libx264",
                    'label': "CPU - libx264",
                },
                {
                    'value': "h264_qsv",
                    'label': "QSV - h264_qsv",
                },
            ]
        self.__set_default_option(values['select_options'], 'video_encoder')
        return values

    def get_main_options_form_settings(self):
        values = {
            "label":      "Write your own custom main options",
            "input_type": "textarea",
        }
        if self.settings.get_setting('mode') not in ['advanced']:
            values["display"] = 'hidden'
        return values

    def get_advanced_options_form_settings(self):
        values = {
            "label":      "Write your own custom advanced options",
            "input_type": "textarea",
        }
        if self.settings.get_setting('mode') not in ['advanced']:
            values["display"] = 'hidden'
        return values

    def get_custom_options_form_settings(self):
        values = {
            "label":      "Write your own custom video options",
            "input_type": "textarea",
        }
        if self.settings.get_setting('mode') not in ['advanced']:
            values["display"] = 'hidden'
        return values

    def get_keep_container_form_settings(self):
        return {
            "label": "Keep the same container",
        }

    def get_dest_container_form_settings(self):
        values = {
            "label":          "Set the output container",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    'value': "mkv",
                    'label': ".mkv - Matroska",
                },
                {
                    'value': "mp4",
                    'label': ".mp4 - MP4 (MPEG-4 Part 14)",
                },
            ],
        }
        if self.settings.get_setting('keep_container'):
            values["display"] = 'hidden'
        return values

    def get_apply_smart_filters_form_settings(self):
        values = {
            "label":   "Enable plugin smart video filters",
            "tooltip": "Provides some pre-configured FFmpeg filtergraphs",
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = 'hidden'
        return values

    def get_autocrop_black_bars_form_settings(self):
        values = {
            "label":       "Autocrop black bars",
            "description": "Runs FFmpeg 'cropdetect' on the file to auto-detect the crop size.\n"
                           "This detected crop size is then applied during video transcode as a 'crop' filter.",
            "sub_setting": True,
        }
        if not self.settings.get_setting('apply_smart_filters'):
            values["display"] = 'hidden'
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = 'hidden'
        return values

    def get_apply_custom_filters_form_settings(self):
        values = {
            "label":   "Enable custom video filters",
            "tooltip": "Provides text input for adding custom FFmpeg filtergraphs",
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = 'hidden'
        return values

    def get_custom_software_filters_form_settings(self):
        values = {
            "label":       "Custom video filters",
            "description": "Video filters and filter chains - https://trac.ffmpeg.org/wiki/FilteringGuide",
            "tooltip":     "Separate each filter chain by a linebreak",
            "sub_setting": True,
            "input_type":  "textarea",
        }
        if not self.settings.get_setting('apply_custom_filters'):
            values["display"] = 'hidden'
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = 'hidden'
        return values
