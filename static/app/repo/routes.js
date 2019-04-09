import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import RepoApp from './containers/RepoApp'
import RepoStatusApp from './containers/RepoStatusApp'
import RepoSettingsApp from './containers/RepoSettingsApp'
import RepoWarningApp from './containers/RepoWarningApp'

import DingTalkWarningApp from './containers/warning/ding_talk_warning_app'
import WeixinWarningApp from './containers/warning/weixin_warning_app'

export default (
    <Route path="/:owner/:repo" component={RepoApp}>
        <IndexRoute component={RepoStatusApp} />
        <Route path="status" component={RepoStatusApp} />
        <Route path="warning" component={RepoWarningApp} >
            <IndexRoute component={DingTalkWarningApp} />
            <Route path="ding_talk" component={DingTalkWarningApp} />
            <Route path="weixin" component={WeixinWarningApp} />
        </Route>
        <Route path="settings" component={RepoSettingsApp} />
    </Route>
)
