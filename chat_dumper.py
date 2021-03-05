# The MIT License (MIT)
#
# Copyright © 2021 Anton Egorov
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the “Software”),
# to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall 
# be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
# THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from telethon.sync import TelegramClient
from os import path

if not path.exists('api.txt'):
    api_id = input('api_id from my.telegram.org: ')
    api_hash = input('api_hash from my.telegram.org: ')
    with open('api.txt', 'w', encoding='utf-8') as file:
        file.write(f'{api_id}\n{api_hash}')
else:
    with open('api.txt', encoding='utf-8') as file:
        api_id, api_hash = file.read().split('\n')


with TelegramClient('chatdumper', api_id, api_hash) as client, open('participants.txt', 'w', encoding='utf-8') as file:
    client.start()
    admins = []
    participants = []
    client.get_dialogs()
    for p in client.iter_participants('Москва на РОИ-2021'):
        cur = p.first_name
        if p.last_name:
            cur += f' {p.last_name}'
        if p.username:
            cur += f' @{p.username}'
        if hasattr(p.participant, 'admin_rights'):
            admins.append(cur)
        else:
            participants.append(cur)
    for adm in sorted(admins):
        print('[admin]', adm, file=file)
    file.write('\n')
    for memb in sorted(participants):
        print(memb, file=file)
