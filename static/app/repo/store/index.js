import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'

import { browserHistory } from 'react-router'
import { syncHistoryWithStore } from 'react-router-redux'

import repoAppReducer from '../reducers'

export let store = createStore(repoAppReducer,
    applyMiddleware(
        thunkMiddleware
    )
);

export const history = syncHistoryWithStore(browserHistory, store);