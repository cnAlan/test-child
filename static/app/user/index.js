import React from 'react'
import { render } from 'react-dom'

import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'

import { browserHistory } from 'react-router'
import { syncHistoryWithStore } from 'react-router-redux'

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import '../css/main.css';


import userAppReducer from './reducers'

import Root from './containers/Root'

let store = createStore(userAppReducer,
  applyMiddleware(
    thunkMiddleware
  )
);

const history = syncHistoryWithStore(browserHistory, store);

render(
  <Root store={store} history={history} />,
  document.getElementById('user-app')
);