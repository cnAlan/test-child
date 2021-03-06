import React from 'react';
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'
import routes from '../routes'
import { Router } from 'react-router'

export default class Root extends React.Component {
    render () {
        const { store, history } = this.props;
        return (
            <Provider store={store}>
                <div>
                    <Router history={history} routes={routes} />
                </div>
            </Provider>
        )
    }
}

Root.propTypes = {
  store: PropTypes.object.isRequired,
  history: PropTypes.object.isRequired
};
