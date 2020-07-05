"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'armv2.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'armv2.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for armv2.
    """
    columns = 2
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.ModelList(
            title=('Главная страница'),
            models=['main.models.*', ],
        ))
        self.children.append(modules.ModelList(
            title=('Новости'),
            models=['news.models.*', ],
        ))
        self.children.append(modules.ModelList(
            title=('Направления'),
            models=['directions.models.*', ],
        ))
        self.children.append(modules.ModelList(
            title=('Медиа'),
            models=['mediafiles.models.*', ],
        ))
        self.children.append(modules.ModelList(
            title=('Федерация'),
            models=['federation.models.*', ],
        ))
        self.children.append(modules.ModelList(
            title=('События'),
            models=['events.models.*', ],
        ))
        # self.children.append(modules.ModelList(
        #     title=('Игроки и команды'),
        #     models=['information.models.*', ],
        # ))
        # self.children.append(modules.ModelList(
        #     title=('Соревнования'),
        #     models=['tournaments.models.*', ],
        # ))
        self.children.append(modules.ModelList(
            title=('TEST POSTGRE'),
            models=['nextsearch.models.*', ],
        ))




        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))




class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for armv2.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
