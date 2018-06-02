import sublime
import sublime_plugin

settings = sublime.load_settings('VintageColor.sublime-settings')


class VintageColor(sublime_plugin.EventListener):
    def on_post_text_command(self, view, command_name, args):
        mode_commands = [
            'enter_insert_mode',
            'exit_insert_mode',
            'enter_visual_mode',
            'enter_visual_line_mode',
            'exit_visual_mode'
        ]

        if command_name not in mode_commands:
            return

        is_insert_mode = command_name == 'enter_insert_mode'
        is_command_mode = (command_name == 'exit_insert_mode' or
                           command_name == 'exit_visual_mode')
        is_visual_mode = command_name == 'enter_visual_mode'
        is_visual_line_mode = command_name == 'enter_visual_line_mode'

        mode = ('insert' if is_insert_mode else
                'command' if is_command_mode else
                'visual' if is_visual_mode else
                'visual_line' if is_visual_line_mode else None)

        if mode is None:
            return

        theme = settings.get('{}_theme'.format(mode))
        view.settings().set('color_scheme', theme)

        highlight_line = settings.get("highlight_line")

        if mode == 'insert' or mode == 'command':
            settings_highlight = settings.get('{}_highlight_line'.format(mode))
            highlight_line = highlight_line or settings_highlight

        view.settings().set("highlight_line", highlight_line)
