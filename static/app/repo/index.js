import React from 'react'
import { render } from 'react-dom'

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import '../css/main.css';

import Root from './containers/Root'

import {store, history} from './store'

render(
    <Root store={store} history={history} />,
    document.getElementById('repo-app')
);