import sublime
import sublime_plugin

mode_commands = {
    'enter_insert_mode': 'insert',
    'exit_insert_mode': 'command',
    'enter_visual_mode': 'visual',
    'enter_visual_line_mode': 'visual_line',
    'exit_visual_mode': 'command'
}


class VintageColor(sublime_plugin.EventListener):
    def __init__(self):
        self.current_mode = 'command'

    def on_post_text_command(self, view, command_name, args):
        # Update mode
        mode = mode_commands[command_name] if command_name in mode_commands else None

        inserted_without_cmd = not view.settings().get('inverse_caret_state')
        if mode is None and inserted_without_cmd and self.current_mode != 'insert':
            mode = 'insert'

        if mode is None:
            return

        self.current_mode = mode

        # Update theme
        plugin_settings = sublime.load_settings('VintageColor.sublime-settings')
        theme = plugin_settings.get('{}_theme'.format(mode))

        if theme:
            view.settings().set('color_scheme', theme)
        else:
            view.settings().erase('color_scheme')

        # Highlight line
        if mode == 'insert' :
            highlight_line = plugin_settings.get('insert_highlight_line')
            view.settings().set('highlight_line', highlight_line)
        else:
            view.settings().erase('highlight_line')
