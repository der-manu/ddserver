'''
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of ddserver.

ddserver is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

ddserver is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with ddserver. If not, see <http://www.gnu.org/licenses/>.
'''

import bottle

from ddserver.web import route

from ddserver.utils.deps import require

from ddserver.interface.user import authorized_admin

from ddserver.interface import validation
from ddserver.interface.validation import validate



@route('/admin/suffixes', method = 'GET')
@authorized_admin()
@require(db = 'ddserver.db:Database',
         templates = 'ddserver.interface.template:TemplateManager')
def get_suffixes(user,
                 db,
                 templates):
  ''' Display a list of suffixes and a form to add new ones. '''

  with db.cursor() as cur:
    cur.execute('''
      SELECT *
      FROM `suffixes`
    ''')
    suffixes = cur.fetchall()

  return templates['suffixes.html'](suffixes = suffixes)



@route('/admin/suffixes/add', method = 'POST')
@authorized_admin()
@validate('/admin/suffixes',
          suffix_name = validation.ValidSuffix(min = 1, max = 255))
@require(db = 'ddserver.db:Database',
         messages = 'ddserver.interface.message:MessageManager')
def post_suffix_add(user,
                    data,
                    db,
                    messages):
  ''' Add a new suffix. '''

  with db.cursor() as cur:
    cur.execute('''
      SELECT *
      FROM `suffixes`
      WHERE `name` = %(name)s
    ''', {'name': data.suffix_name})

    if cur.rowcount > 0:
      messages.error('Suffix with same name already exists')
      bottle.redirect('/admin/suffixes')

    cur.execute('''
      INSERT
      INTO `suffixes`
      SET `name` = %(name)s
    ''', {'name': data.suffix_name})

  messages.success('Ok, done.')

  bottle.redirect('/admin/suffixes')



@route('/admin/suffixes/delete', method = 'POST')
@authorized_admin()
@validate('/admin/suffixes',
          suffix_id = validation.Int(not_empty = True))
@require(db = 'ddserver.db:Database',
         messages = 'ddserver.interface.message:MessageManager')
def post_suffix_delete(user,
                       data,
                       db,
                       messages):
  ''' Delete a suffix. '''

  with db.cursor() as cur:
    cur.execute('''
      DELETE
      FROM `suffixes`
      WHERE id = %(suffix_id)s
    ''', {'suffix_id': data.suffix_id})

  messages.success('Ok, done.')

  bottle.redirect('/admin/suffixes')
