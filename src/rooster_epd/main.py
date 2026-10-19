from typing import Optional

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import app, ui

from bcrypt import gensalt, hashpw, checkpw
from copy import deepcopy
from datetime import datetime, date
from os import remove
from packaging.version import Version
from random import choice
from requests import get
from string import ascii_letters
from subprocess import Popen
from sys import executable
from threading import Thread
from zermelo import Client

from rooster_epd import __version__
from rooster_epd.storage import (PASSWORD_PATH, STORAGE_SECRET_PATH,
                                 load_save, write_save)

VERSION = f'V{__version__}'

unrestricted_page_routes = {'/login'}

# Block all pages except /login if the user isn't logged in
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:
                return RedirectResponse(f'/login?redirect_to={request.url.path}')
        return await call_next(request)

app.add_middleware(AuthMiddleware)

# The login page
@ui.page('/login', title='Rooster-EPD')
def login(redirect_to: str = '/') -> Optional[RedirectResponse]:
    def try_login() -> None:
        # Try to login
        if PASSWORD_PATH.is_file():
            with open(PASSWORD_PATH, 'rb') as file:
                if checkpw(password.value.encode(), file.read()):
                    app.storage.user.update({'authenticated': True})
                    ui.navigate.to(redirect_to)  # go back to where the user wanted to go
                else:
                    password.set_value('')
                    ui.notify('Wachtwoord incorrect', color='negative')
        # Set the password if it hadn't been set yet
        else:
            if password.value:
                with open(PASSWORD_PATH, 'wb') as file:
                    file.write(hashpw(password.value.encode(), gensalt()))

                login_button.set_text('Log in')
                login_button.set_icon('login')
                password.set_value('')
                ui.notify('Wachtwoord ingesteld', color='positive')
            else:
                ui.notify('Geef een wachtwoord', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.card().classes('absolute-center'):
        password = ui.input('Wachtwoord', password=True, password_toggle_button=True).on('keydown.enter', try_login).props('filled dense stack-label')
        login_button = ui.button(on_click=try_login)
        if PASSWORD_PATH.is_file():
            login_button.set_text('Log in')
            login_button.set_icon('login')
        else:
            login_button.set_text('Wachtwoord instellen')
            login_button.set_icon('vpn_key')

    # Dark mode toggle
    dark = ui.dark_mode(app.storage.user.get('dark_mode', True))
    def toggle_dark_mode() -> None:
        dark.toggle()
        app.storage.user.update({'dark_mode': dark.value})

    with ui.page_sticky(x_offset=12, y_offset=12):
        ui.button(icon='contrast', on_click=toggle_dark_mode).props('round size=md')

    # Version label
    with ui.page_sticky(position='bottom-left', x_offset=10, y_offset=5):
        ui.label(VERSION).classes('italic')

# The save file is loaded in main(), before the UI starts
save: dict = {}

# Main app
@ui.page('/', title='Rooster-EPD')
def main_page() -> None:
    def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to('/login')

    def change_password() -> None:
        remove(PASSWORD_PATH)
        logout()

    def save_changes() -> None:
        save['starttime'] = int(begintijd.value.split(':')[0]) * 60 + int(begintijd.value.split(':')[1])
        save['endtime'] = int(eindtijd.value.split(':')[0]) * 60 + int(eindtijd.value.split(':')[1])

        save['notes'][0] = maandag.value
        save['notes'][1] = dinsdag.value
        save['notes'][2] = woensdag.value
        save['notes'][3] = donderdag.value
        save['notes'][4] = vrijdag.value
        save['notes'][5] = zaterdag.value
        save['notes'][6] = zondag.value

        write_save(save)
        ui.notify('Wijzigingen opgeslagen', color='positive')

    # Update dialog
    with ui.dialog() as update_dialog, ui.card().style('max-width: none'):
        # Get the update info
        github_update: dict = get('https://api.github.com/repos/duisterethomas/rooster-epd/releases/latest').json()

        ui.label('Er is een update beschikbaar!').classes('text-xl')
        ui.label(f'{VERSION} -> {github_update["tag_name"]}')
        with ui.card().props('flat bordered'):
            ui.markdown(f'# {github_update["name"]}\n{github_update["body"]}').style()
        ui.label('Wil je naar GitHub gaan om deze update te downloaden?')
        with ui.row():
            ui.button('Nee', on_click=update_dialog.close, color='negative', icon='close')
            ui.button('Ja', on_click=lambda: ui.navigate.to(github_update['html_url'], True), color='positive', icon='launch')

    # Sync button
    @ui.refreshable
    def sync_button_func():
        def sync_thread(specific_date: bool) -> None:
            sync_button.props('loading')
            sync_button.disable()
            # Run the screen refresh from the installed package
            command = [executable, '-m', 'rooster_epd.screen_refresh']
            if specific_date:
                command.append(sync_date.value)
            p = Popen(command)
            p.wait()
            sync_button_func.refresh()

        def sync(specific_date: bool) -> None:
            sync_button.close()
            thread = Thread(target=lambda: sync_thread(specific_date))
            thread.start()

        with ui.dropdown_button('Synchroniseren', on_click=lambda: sync(specific_date=False), icon='sync', split=True) as sync_button:
            sync_date = ui.date(on_change=lambda: sync(specific_date=True)).props('minimal')

    # Link Zermelo dialog
    with ui.dialog() as link_zermelo_dialog, ui.card().style('max-width: none'):
        def link_zermelo():
            save['school'] = schoolnaam.value

            # Get and save a new zermelo token
            try:
                save['token'] = Client(save['school']).authenticate(koppelcode.value)['access_token']
                write_save(save)
                ui.notify('Zermelo gekoppeld', color='positive')
                link_zermelo_dialog.close()
            except ValueError:
                save['token'] = ''
                ui.notify('Zermelo koppelen mislukt', color='negative')

        ui.label('Koppel met Zermelo')
        schoolnaam = ui.input('Schoolnaam', value=save['school']).props('filled dense stack-label')
        koppelcode = ui.input('Koppelcode').props('filled dense stack-label')
        with ui.row():
            ui.button('Annuleren', on_click=link_zermelo_dialog.close, icon='close')
            ui.button('Koppelen', on_click=link_zermelo, icon='link')

    # Sjablonen dialog
    changed_template_names = {}

    @ui.refreshable
    def sjablonen() -> None:
        def delete(template_name) -> None:
            save['templates'].pop(template_name)
            sjablonen.refresh()

        def set_starttime(changes, template) -> None:
            template['startTime'][0] = int(changes.value.split(':')[0])
            template['startTime'][1] = int(changes.value.split(':')[1])

        def set_endtime(changes, template) -> None:
            template['endTime'][0] = int(changes.value.split(':')[0])
            template['endTime'][1] = int(changes.value.split(':')[1])

        def set_subjects(changes, template) -> None:
            template['subjects'] = changes.value

        def set_locations(changes, template) -> None:
            template['locations'] = changes.value

        def set_timeslotname(changes, template) -> None:
            template['timeSlotName'] = changes.value

        def set_name(changes, template_name) -> None:
            if changes.value:
                changed_template_names[template_name] = changes.value

        for template_name in sorted(save['templates'].keys()):
            template = save['templates'][template_name]

            with ui.card():
                with ui.row():
                    with ui.column():
                        with ui.input('Begin tijd', on_change=lambda changes, templt=template: set_starttime(changes, templt), value='%02d:%02d' % (template['startTime'][0], template['startTime'][1])).props('readonly size=4 filled dense stack-label') as begintijd:
                            with ui.menu().props('no-parent-event') as menu:
                                ui.time().bind_value(begintijd).props('format24h')
                            with begintijd.add_slot('append'):
                                ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')

                        with ui.input('Eind tijd', on_change=lambda changes, templt=template: set_endtime(changes, templt), value='%02d:%02d' % (template['endTime'][0], template['endTime'][1])).props('readonly size=4 filled dense stack-label') as eindtijd:
                            with ui.menu().props('no-parent-event') as menu:
                                ui.time().bind_value(eindtijd).props('format24h')
                            with eindtijd.add_slot('append'):
                                ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')

                    with ui.column():
                        ui.input('Onderwerp(en)', on_change=lambda changes, templt=template: set_subjects(changes, templt), value=template['subjects']).props('filled dense stack-label')
                        ui.input('Locatie(s)', on_change=lambda changes, templt=template: set_locations(changes, templt), value=template['locations']).props('filled dense stack-label')

                    ui.input('Lesuur', on_change=lambda changes, templt=template: set_timeslotname(changes, templt), value=template['timeSlotName']).props('size=3 filled dense stack-label')

                    with ui.column():
                        ui.input('Naam', on_change=lambda changes, templt_name=template_name: set_name(changes, templt_name), value=template_name, validation={'Vul een naam in': lambda value: len(value) != 0}).props('filled dense stack-label')
                        ui.button('Verwijder', on_click=lambda _, templt_name=template_name: delete(templt_name), color='negative', icon='delete')

    def add_template() -> None:
        name = "New"
        count = 0

        while name in save['templates']:
            count += 1
            name = f"New{count}"

        save['templates'][name] = {'startTime': [0, 0],
                                   'endTime': [0, 0],
                                   'subjects': '',
                                   'locations': '',
                                   'timeSlotName': ''}
        sjablonen.refresh()

    # Edit templates dialog
    with ui.dialog() as edit_templates_dialog, ui.card().style('max-width: none'):
        def done_pressed() -> None:
            for changed_name in changed_template_names.keys():
                save['templates'][changed_template_names[changed_name]] = deepcopy(save['templates'][changed_name])
                save['templates'].pop(changed_name)
            changed_template_names.clear()
            sjablonen.refresh()
            template_list.refresh()
            edit_templates_dialog.close()

        with ui.row():
            ui.button('Sjabloon toevoegen', on_click=add_template, icon='add')
            ui.button('Klaar', on_click=done_pressed, icon='done')

        sjablonen()

    # Afspraken card
    @ui.refreshable
    def afspraken() -> None:
        save['appointments'].sort(key=lambda d: datetime(d['date'][0], d['date'][1], d['date'][2], d['startTime'][0], d['startTime'][1]).timestamp())

        def delete(appointment):
            save['appointments'].remove(appointment)
            afspraken.refresh()

        def set_starttime(changes, appointment):
            appointment['startTime'][0] = int(changes.value.split(':')[0])
            appointment['startTime'][1] = int(changes.value.split(':')[1])

        def set_endtime(changes, appointment):
            appointment['endTime'][0] = int(changes.value.split(':')[0])
            appointment['endTime'][1] = int(changes.value.split(':')[1])

        def set_subjects(changes, appointment):
            appointment['subjects'] = changes.value

        def set_locations(changes, appointment):
            appointment['locations'] = changes.value

        def set_timeslotname(changes, appointment):
            appointment['timeSlotName'] = changes.value

        def set_date(changes, appointment):
            appointment['date'][0] = int(changes.value.split('-')[0])
            appointment['date'][1] = int(changes.value.split('-')[1])
            appointment['date'][2] = int(changes.value.split('-')[2])

        for appointment in save['appointments']:
            with ui.card():
                with ui.row():
                    with ui.column():
                        with ui.input('Begin tijd', on_change=lambda changes, appointmnt=appointment: set_starttime(changes, appointmnt), value='%02d:%02d' % (appointment['startTime'][0], appointment['startTime'][1])).props('readonly size=4 filled dense stack-label') as begintijd:
                            with ui.menu().props('no-parent-event') as menu:
                                ui.time().bind_value(begintijd).props('format24h')
                            with begintijd.add_slot('append'):
                                ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')

                        with ui.input('Eind tijd', on_change=lambda changes, appointmnt=appointment: set_endtime(changes, appointmnt), value='%02d:%02d' % (appointment['endTime'][0], appointment['endTime'][1])).props('readonly size=4 filled dense stack-label') as eindtijd:
                            with ui.menu().props('no-parent-event') as menu:
                                ui.time().bind_value(eindtijd).props('format24h')
                            with eindtijd.add_slot('append'):
                                ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')

                    with ui.column():
                        ui.input('Onderwerp(en)', on_change=lambda changes, appointmnt=appointment: set_subjects(changes, appointmnt), value=appointment['subjects']).props('filled dense stack-label')
                        ui.input('Locatie(s)', on_change=lambda changes, appointmnt=appointment: set_locations(changes, appointmnt), value=appointment['locations']).props('filled dense stack-label')

                    ui.input('Lesuur', on_change=lambda changes, appointmnt=appointment: set_timeslotname(changes, appointmnt), value=appointment['timeSlotName']).props('size=3 filled dense stack-label')

                    with ui.column():
                        with ui.input('Datum', on_change=lambda changes, appointmnt=appointment: set_date(changes, appointmnt), value='%d-%02d-%02d' % (appointment['date'][0], appointment['date'][1], appointment['date'][2])).props('readonly size=9 filled dense stack-label') as datum:
                            with ui.menu().props('no-parent-event') as menu:
                                ui.date().bind_value(datum)
                            with datum.add_slot('append'):
                                ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
                        ui.button('Verwijder', on_click=lambda _, appointmnt=appointment: delete(appointmnt), color='negative', icon='delete')

    def add_appointment(template: dict | None = None) -> None:
        today = date.today()
        if template:
            save['appointments'].append({'date': [today.year, today.month, today.day],
                                         'startTime': template['startTime'],
                                         'endTime': template['endTime'],
                                         'subjects': template['subjects'],
                                         'locations': template['locations'],
                                         'timeSlotName': template['timeSlotName']})
        else:
            save['appointments'].append({'date': [today.year, today.month, today.day],
                                         'startTime': [0, 0],
                                         'endTime': [0, 0],
                                         'subjects': '',
                                         'locations': '',
                                         'timeSlotName': ''})
        afspraken.refresh()

    @ui.refreshable
    def template_list() -> None:
        for template_name in sorted(save['templates'].keys()):
            ui.button(template_name, on_click=lambda _, templt_name=template_name: add_appointment(save['templates'][templt_name])).classes('w-full').props('flat')

    # Main ui
    with ui.row():
        with ui.column():
            # Acties
            with ui.card():
                ui.label('Acties')
                sync_button_func()
                ui.button('Koppel met Zermelo', on_click=link_zermelo_dialog.open, icon='link')
                ui.button('Wijzigingen opslaan', on_click=save_changes, color='positive', icon='save')
                with ui.dropdown_button('Log uit', on_click=logout, color='negative', icon='logout', split=True):
                    ui.button('Wachtwoord wijzigen', on_click=change_password, color='negative', icon='lock_reset').props('flat')

            # Tijden instellen
            with ui.card():
                with ui.row():
                    hour, minutes = divmod(save['starttime'], 60)
                    with ui.input('Begin tijd', value='%02d:%02d' % (hour, minutes)).props('readonly size=4 filled dense stack-label') as begintijd:
                        with ui.menu().props('no-parent-event') as menu:
                            ui.time().bind_value(begintijd).props('format24h')
                        with begintijd.add_slot('append'):
                            ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')

                    hour, minutes = divmod(save['endtime'], 60)
                    with ui.input('Eind tijd', value='%02d:%02d' % (hour, minutes)).props('readonly size=4 filled dense stack-label') as eindtijd:
                        with ui.menu().props('no-parent-event') as menu:
                            ui.time().bind_value(eindtijd).props('format24h')
                        with eindtijd.add_slot('append'):
                            ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')

        # Wekelijkse dag notities
        with ui.card():
            ui.label('Wekelijkse dag notities')
            maandag = ui.input('Maandag', value=save['notes'][0]).props('filled dense stack-label')
            dinsdag = ui.input('Dinsdag', value=save['notes'][1]).props('filled dense stack-label')
            woensdag = ui.input('Woensdag', value=save['notes'][2]).props('filled dense stack-label')
            donderdag = ui.input('Donderdag', value=save['notes'][3]).props('filled dense stack-label')
            vrijdag = ui.input('Vrijdag', value=save['notes'][4]).props('filled dense stack-label')
            zaterdag = ui.input('Zaterdag', value=save['notes'][5]).props('filled dense stack-label')
            zondag = ui.input('Zondag', value=save['notes'][6]).props('filled dense stack-label')

        # Eigen afspraken
        with ui.card():
            ui.label('Afspraken')
            with ui.row():
                with ui.dropdown_button('Afspraak toevoegen', on_click=lambda: add_appointment(), icon='event', split=True, auto_close=True) as afspraak_toevoegen:
                    with ui.column().classes('gap-0'):
                        ui.button('Slablonen bewerken', on_click=edit_templates_dialog.open, icon='edit').classes('w-full').props('flat')
                        template_list()
                ui.button('Sorteer', on_click=afspraken.refresh, icon='sort')
            afspraken()

    # Dark mode toggle
    dark = ui.dark_mode(app.storage.user.get('dark_mode', True))
    def toggle_dark_mode() -> None:
        dark.toggle()
        app.storage.user.update({'dark_mode': dark.value})

    with ui.page_sticky(x_offset=12, y_offset=12):
        ui.button(icon='contrast', on_click=toggle_dark_mode).props('round size=md')

    # Version label
    with ui.page_sticky(position='bottom-left', x_offset=10, y_offset=5):
        ui.label(VERSION).classes('italic')

    # Check for updates
    if Version(VERSION[1:]) < Version(get('https://api.github.com/repos/duisterethomas/rooster-epd/releases/latest').json()['tag_name'][1:]):
        update_dialog.open()

def main() -> None:
    # Load the save file into the dict the pages use
    save.update(load_save())

    # Create random storage secret if it isn't created yet
    if not STORAGE_SECRET_PATH.is_file():
        with open(STORAGE_SECRET_PATH, 'w') as file:
            file.write(''.join(choice(ascii_letters) for i in range(64)))

    # Run the ui
    with open(STORAGE_SECRET_PATH, 'r') as file:
        storage_secret = file.read()

    ui.run(language='nl', storage_secret=storage_secret, reload=False, show=False, port=80)

if __name__ == "__main__":
    main()
