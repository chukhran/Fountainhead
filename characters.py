import sublime
import sublime_plugin
import re
import os
import codecs
# import sys
# import platform
# from .sublime_helper import *
try:
    from . import scopes
except (ImportError, ValueError):
    import scopes
try:
    from .sublime_helper import SublimeHelper
except (ImportError, ValueError):
    from sublime_helper import SublimeHelper

fountain_scope = scopes.fountain_scope
action_scope = scopes.action_scope
boneyard_scope = scopes.boneyard_scope
dialogue_scope = scopes.dialogue_scope
lyrics_scope = scopes.lyrics_scope
character_scope = scopes.character_scope
parenthetical_scope = scopes.parenthetical_scope
note_scope = scopes.note_scope
scene_scope = scopes.scene_scope
character_list_scope = scopes.character_list_scope
section_scope = scopes.section_scope
synopses_scope = scopes.synopses_scope
pagebreak_scope = scopes.pagebreak_scope
title_page_scope = scopes.title_page_scope
center_scope = scopes.center_scope
transition_scope = scopes.transition_scope

user = ''
# user_os = platform.system()


class Characters(sublime_plugin.EventListener):

    characters = []
    person = ''
    # lower_characters = []
    # camel_characters = []
    current_character = ''
    previous_line = 0
    current_line = 0
    filename = ''

    def modified_character(self, view):
        if view.settings().get('syntax') == 'Packages/Fountainhead/Fountainhead.tmLanguage':
        # if 'Fountainhead.tmLanguage' in view.settings().get('syntax'):
            # if sublime.load_settings('Fountainhead.sublime-settings').get('characters', True):
            if view.settings().get('characters', True):
                if self.characters == []:
                    self.on_activated(view)
                view.set_status('CharacterList', '')
                if view.rowcol(view.sel()[0].end())[0] != self.current_line:
                    self.previous_line = self.current_line
                    self.current_line = view.rowcol(view.sel()[0].end())[0]
                    # if view.scope_name(view.text_point(self.previous_line, 0)) == 'text.fountain dialogue entity.name.class ':
                    # if view.scope_name(view.text_point(self.previous_line, 0)) == 'text.fountain dialogue entity.name.class ':
                    if view.scope_name(view.text_point(self.previous_line, 0)) == fountain_scope + dialogue_scope + character_scope:
                        # get character name from line
                        s = SublimeHelper()
                        self.current_character = view.substr(view.line(view.text_point(self.previous_line, 0)))
                        character = s.line_string(view)
                        name = self.current_character.split(' (O.S.)')[0]
                        name = name.split(' (V.O.)')[0]
                        name = name.split(' (OS)')[0]
                        name = name.split(' (VO)')[0]
                        name = name.split(" (CONT'D)")[0]
                        name = name.split(' (ЗК)')[0]
                        name = name.split(' (З.К.)')[0]
                        name = name.split(' (ЗА КАДРОМ)')[0]
                        name = name.split(' (ВПЗ)')[0]
                        name = name.split(' (В.П.З.)')[0]
                        name = name.split(' (ППЗ)')[0]
                        name = name.split(' (П.П.З.)')[0]
                        if name[0] == ' ' or name[0] == '\t':
                            name = re.split(r'^\s*', name)[1]
                        if name not in self.characters and name != '' and name is not None:
                            self.characters.append(name)
                            self.characters = sorted(self.characters)
                            ShowCharactersCommand.characters = self.characters
                            # Create Fountainhead directory if it doesn't exist
                            packages_directory = sublime.packages_path() + '/User/Fountainhead/'
                            if not os.path.exists(packages_directory):
                                os.mkdir(packages_directory)
                            completions_file = packages_directory + 'Characters.sublime-completions'
                            # if user_os == 'Windows':
                                # print("Sorry, not supported at this time.")
                            # elif user_os == 'Darwin':

                            completions = codecs.open(completions_file, 'w', 'utf8')
                            # completions.write('{\n\t\t"scope": "text.fountain - comment - string - dialogue - entity.other.attribute-name - entity.other.inherited-class - foreground - meta.diff - entity.name.function - entity.name.tag - entity.name.class - variable.parameter",\n\n\t\t"completions":\n\t\t[')
                            completions.write('{\n\t\t"scope": ' + '"' + fountain_scope + '- ' + boneyard_scope + '- ' + action_scope + '- ' + dialogue_scope + '- ' + lyrics_scope + '- ' + character_scope + '- ' + parenthetical_scope + '- ' + note_scope + '- ' + scene_scope + '- ' + section_scope + '- ' + synopses_scope + '- ' + pagebreak_scope + '- ' + title_page_scope + '- ' + center_scope + '- ' + transition_scope[0:-1] + '",\n\n\t\t"completions":\n\t\t[')
                            length = len(self.characters)
                            character_counter = 0
                            for character in self.characters:
                                if character_counter < length - 1:
                                    completions.write('"%s",' % character)
                                    character_counter += 1
                                else:
                                    completions.write('"%s"' % character)
                            completions.write(']\n}')
                            completions.close()

                            # Not needed since characters are no longer converted to lowercase
                            # if name[0] != '@':
                            #     if name.lower() not in self.lower_characters:
                            #         self.lower_characters.append(name.lower())
                            #         self.lower_characters = sorted(self.lower_characters)
                            #         completions = codecs.open(completions_file, 'w', 'utf8')
                            #         completions.write('{\n\t\t"scope": "text.fountain - comment - string - entity.other.attribute-name - entity.other.inherited-class - foreground - meta.diff - entity.name.function - entity.name.tag - entity.name.class - variable.parameter",\n\n\t\t"completions":\n\t\t[')
                            #         length = len(self.lower_characters)
                            #         character_counter = 0
                            #         for character in self.lower_characters:
                            #             if character_counter < length - 1:
                            #                 completions.write('"%s",' % character)
                            #                 character_counter += 1
                            #             else:
                            #                 completions.write('"%s"' % character)
                            #         completions.write(']\n}')
                            #         completions.close()
                            # elif name[0] == '@':
                            #     if name not in self.lower_characters:
                            #         self.lower_characters.append(name)
                            #         self.lower_characters = sorted(self.lower_characters)
                            #         completions = codecs.open(completions_file, 'w', 'utf8')
                            #         completions.write('{\n\t\t"scope": "text.fountain - comment - string - entity.other.attribute-name - entity.other.inherited-class - foreground - meta.diff - entity.name.function - entity.name.tag - entity.name.class - variable.parameter",\n\n\t\t"completions":\n\t\t[')
                            #         length = len(self.lower_characters)
                            #         character_counter = 0
                            #         for character in self.lower_characters:
                            #             if character_counter < length - 1:
                            #                 completions.write('"%s",' % character)
                            #                 character_counter += 1
                            #             else:
                            #                 completions.write('"%s"' % character)
                            #         completions.write(']\n}')
                            #         completions.close()

                            # Clear out character list message
                            view.set_status('CharacterList',
                                            '')

    def on_modified_async(self, view):
        if int(sublime.version()) >= 3000:
            self.modified_character(view)

    def on_modified(self, view):
        if int(sublime.version()) < 3000:
            self.modified_character(view)

    def on_activated(self, view):
        if view.settings().get('syntax') == 'Packages/Fountainhead/Fountainhead.tmLanguage':
        # s = view.settings().get('syntax')
        # while s is None:
        #     s = view.settings().get('syntax')
        # if 'Fountainhead.tmLanguage' in s:
            # if sublime.load_settings('Fountainhead.sublime-settings').get('characters', True):
            if view.settings().get('characters', True):
                if self.filename == view.file_name() and len(self.characters) > 0:
                    pass
                    # print(view.file_name())
                else:
                    view.set_status('CharacterList',
                                    'FINDING CHARACTERS...')
                    self.characters = []
                    # self.lower_characters = []
                    counter = 0
                    self.filename = view.file_name()
                    try:
                        while counter >= 0:
                            # character = view.substr(view.find_by_selector('text.fountain dialogue entity.name.class ')[counter])
                            character = view.substr(view.find_by_selector(fountain_scope + dialogue_scope + character_scope)[counter])
                            name = character.split(' (O.S.)')[0]
                            name = name.split(' (V.O.)')[0]
                            name = name.split(' (OS)')[0]
                            name = name.split(' (VO)')[0]
                            name = name.split(" (CONT'D)")[0]
                            name = name.split(' (ЗК)')[0]
                            name = name.split(' (З.К.)')[0]
                            name = name.split(' (ЗА КАДРОМ)')[0]
                            name = name.split(' (ВПЗ)')[0]
                            name = name.split(' (В.П.З.)')[0]
                            name = name.split(' (ППЗ)')[0]
                            name = name.split(' (П.П.З.)')[0]
                            if name[0] == ' ' or name[0] == '\t':
                                name = (re.split(r'^\s*', name))[1]
                            if name not in self.characters and name != '' and name is not None:
                                self.characters.append(name)
                            counter += 1
                    except IndexError:
                        pass

                    # for character in self.characters:
                    #     if character[0] != '@':
                    #         self.lower_characters.append(character.lower())
                    #     if character[0] == '@':
                    #         self.lower_characters.append(character)
                    # self.lower_characters = sorted(self.lower_characters)

                    self.characters = sorted(self.characters)
                    # proc_env = os.environ.copy()
                    # encoding = sys.getfilesystemencoding()
                    # for k, v in proc_env.items():
                    #     proc_env[k] = os.path.expandvars(v).encode(encoding)
                    # user = (proc_env['HOME']).decode(encoding='UTF-8')
                    # completions = open(user + '/Library/Application Support/Sublime Text 3/Packages/Fountainhead/Characters.sublime-completions', 'w')
                    # packages_directory = sublime.packages_path()
                    # completions_file = packages_directory + '/Fountainhead/Characters.sublime-completions'
                    # Create Fountainhead directory if it doesn't exist
                    packages_directory = sublime.packages_path() + '/User/Fountainhead/'
                    if not os.path.exists(packages_directory):
                        os.mkdir(packages_directory)
                    completions_file = packages_directory + 'Characters.sublime-completions'
                    completions = codecs.open(completions_file, 'w', 'utf8')
                    # completions.write('{\n\t\t"scope": "text.fountain - comment - string - dialogue - entity.other.attribute-name - entity.other.inherited-class - foreground - meta.diff - entity.name.function - entity.name.tag - entity.name.class - variable.parameter",\n\n\t\t"completions":\n\t\t[')
                    completions.write('{\n\t\t"scope": ' + '"' + fountain_scope + '- ' + boneyard_scope + '- ' + action_scope + '- ' + dialogue_scope + '- ' + lyrics_scope + '- ' + character_scope + '- ' + parenthetical_scope + '- ' + note_scope + '- ' + scene_scope + '- ' + section_scope + '- ' + synopses_scope + '- ' + pagebreak_scope + '- ' + title_page_scope + '- ' + center_scope + '- ' + transition_scope[0:-1] + '",\n\n\t\t"completions":\n\t\t[')
                    # length = len(self.lower_characters)
                    length = len(self.characters)
                    character_counter = 0
                    # for character in self.lower_characters:
                    for character in self.characters:
                        if character_counter < length - 1:
                            completions.write('"%s",' % character)
                            character_counter += 1
                        else:
                            completions.write('"%s"' % character)
                    completions.write(']\n}')
                    completions.close()
                    # Print confirmation message
                    view.set_status('CharacterList',
                                    'CHARACTERS FOUND!')

                    # ShowCharactersCommand.unsorted_characters = self.characters
                    ShowCharactersCommand.characters = self.characters


class UpdateCharacterListCommand(sublime_plugin.TextCommand):

    characters = []
    filename = ''

    def run(self, edit):
        self.characters = []
        c = Characters()
        c.on_activated(self.view)


class ShowCharactersCommand(sublime_plugin.TextCommand):

    person = ''
    # unsorted_characters = []
    # sorted_characters = []
    characters = []

    def run(self, edit):
        # if sublime.load_settings('Fountainhead.sublime-settings').get('characters', True) and int(sublime.version()) >= 3000:
        if self.view.settings().get('characters', True) and int(sublime.version()) >= 3000:
            # self.sorted_characters = sorted(self.unsorted_characters)
            # self.view.show_popup_menu(self.sorted_characters, self.on_done)
            self.view.show_popup_menu(self.characters, self.on_done)

            self.view.run_command('insert', {"characters": self.person})

    def on_done(self, index):
        if index == -1:
            self.person = ''
        else:
            # self.person = self.sorted_characters[index]
            self.person = self.characters[index]
