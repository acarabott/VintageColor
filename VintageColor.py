import sublime
import sublime_plugin


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

        mode = ('insert' if command_name == 'enter_insert_mode' else
                'command' if (command_name == 'exit_insert_mode' or
                              command_name == 'exit_visual_mode') else
                'visual' if command_name == 'enter_visual_mode' else
                'visual_line' if command_name == 'enter_visual_line_mode' else
                None)

        if command_name == 'enter_insert_mode':
            mode = 'insert'
        elif command_name in ['exit_insert_mode', 'exit_visual_mode']:
            mode = 'command'
        elif command_name == 'enter_visual_mode':
            mode = 'visual'
        elif command_name == 'enter_visual_line_mode':
            mode = 'visual_line'

        plugin_settings = sublime.load_settings('VintageColor.sublime-settings')
        global_settings = sublime.load_settings("Preferences.sublime-settings")

        # update color scheme
        if mode == 'command':
            theme = global_settings.get("color_scheme")
        else:
            theme = plugin_settings.get('{}_theme'.format(mode))

        view.settings().set('color_scheme', theme)

        # highlight line
        highlight_line = global_settings.get("highlight_line")

        if mode == 'insert' :
            settings_highlight = plugin_settings.get('insert_highlight_line')
            highlight_line = highlight_line or settings_highlight

        view.settings().set("highlight_line", highlight_line)
