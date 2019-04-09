import React from 'react';
import PropTypes from 'prop-types'
import { Link } from 'react-router'
import classNames from 'classnames'

export default class RepoAppNaviBar extends React.Component{
  constructor(props) {
    super(props);
  }

  render() {
    let owner = this.props.owner;
    let repo = this.props.repo;

    let { router } = this.context;

    let settings_is_active = router.isActive({ pathname:'/' + owner + '/' + repo + '/settings'} );
    let warning_is_active = router.isActive({ pathname:'/' + owner + '/' + repo + '/warning'} );

    let sub_page_active_flag = false;
    if (settings_is_active || warning_is_active) {
      sub_page_active_flag = true;
    }

    let status_is_active = true;
    if (sub_page_active_flag) {
      status_is_active = false;
    }

    return (
      <section className="app-navi-bar">
        <ul className="nav nav-tabs">
          <li className='nav-item' >
            <Link className={classNames({active: status_is_active, 'nav-link': true})}
              to={{ pathname:'/' + owner + '/' + repo + '/' }} >状态</Link>
          </li>
          <li className='nav-item' >
            <Link className={classNames({active: warning_is_active, 'nav-link': true})}
                  to={{ pathname:'/' + owner + '/' + repo + '/warning' }} >报警</Link>
          </li>
          <li className='nav-item' >
            <Link  className={classNames({active: settings_is_active, 'nav-link': true})}
                   to={{ pathname:'/' + owner + '/' + repo + '/settings' }} >设置</Link>
          </li>
        </ul>
      </section>
    );
  }
}

RepoAppNaviBar.propTypes = {
  owner: PropTypes.string.isRequired,
  repo: PropTypes.string.isRequired
};

RepoAppNaviBar.contextTypes = {
  router: PropTypes.object.isRequired
};
