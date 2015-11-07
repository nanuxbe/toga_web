class ProfilePage(Page):
    user_details = UserInfo()
    tabs = TabCollection()
    tabs2 = TabCollection()

    class Meta:
        template_name="profile.html"


class UserInfo(DetailComponent, TemplateView):
    endpoint = 'api-user-info'
    verb = 'GET'
    template_name = 'userinfo.html'

    list_display = [
        {
            'field': 'picture',
            'widget': 'widget-img',
        }, {
            'field': 'full_name'
        }, {
            'field': 'username'
        }
    ]

    def get_endpoint_full_url(self, **kwargs):
        kwargs['username'] = self.request.kwargs['username']
        return super(UserInfo, self).get_endpoint_full_url(**kwargs)


class TabCollection(ComponentCollection, TemplateView):
    components = [
        ContributionsTab,
        RepositoriesTab,
        QctivityTab,
    ]
    template_name = 'tabs.html'


class TabComponent(ComponentCollection, TemplateView):
    template_name = 'tab.html'


class ContributionsTab(TabComponent):
    components = [
        PopularRepoList,
        ContributedToList,
        ConttributionsList,
    ]


class PopularRepoList(ListComponent):
    endpoint = 'popular_repo'
    actions = [
        Action('details', 'repo', params=['slug']),
    ]
    list_display = [
        {
            'field': 'is_fork',
            'widget': 'widget-fork',G
        }, {
            'field': 'path'
        }, {
            'field': 'stars',
            'widget': 'widget-star',
        }
    ]


class ContributedToList(ListComponent):
    endpoint = 'contributed_to_repo'
    actions = [
        Action('details', 'GET', 'repo', params=['slug']),
    ]


class ConttributionsList(ListComponent):
    endpoint = 'contributions'

