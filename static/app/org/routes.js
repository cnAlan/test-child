import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import OrgApp from './containers/OrgApp'
import OrgReposApp from './containers/OrgReposApp'
import OrgPeopleApp from './containers/OrgPeopleApp'
import OrgWarningApp from './containers/OrgWarningApp'
import OrgSettingsApp from './containers/OrgSettingsApp'
import DingTalkWarningApp from './containers/warning/DingTalkWarningApp'

export default (
  <Route path="/:owner" component={OrgApp}>
    <IndexRoute component={OrgReposApp} />
    <Route path="/orgs/:owner/repos" component={OrgReposApp} />
    <Route path="/orgs/:owner/people" component={OrgPeopleApp} />
    <Route path="/orgs/:owner/warning" component={OrgWarningApp} >
      <IndexRoute component={DingTalkWarningApp} />
      <Route path="ding_talk" component={DingTalkWarningApp} />
    </Route>
    <Route path="/orgs/:owner/settings" component={OrgSettingsApp} />
  </Route>
)