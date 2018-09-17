import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import UserApp from './containers/user/UserApp'

export default (
    <Route path="/:user" component={UserApp}>
    </Route>
)