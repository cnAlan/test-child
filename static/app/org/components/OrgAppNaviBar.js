import React from 'react';
import PropTypes from 'prop-types'
import { Link } from 'react-router'

export default class OrgAppNaviBar extends React.Component{
  constructor(props) {
    super(props);
  }

  render() {
    let owner = this.props.owner;

    let { router } = this.context;

    let people_is_active = router.isActive({ pathname:'/orgs/' + owner + '/people'} );
    let warning_is_active = router.isActive({ pathname:'/orgs/' + owner + '/warning'} );
    let settings_is_active = router.isActive({ pathname:'/orgs/' + owner + '/settings'} );

    let sub_page_active_flag = false;
    if (people_is_active || warning_is_active || settings_is_active) {
      sub_page_active_flag = true;
    }

    let repo_is_active = true;
    if (sub_page_active_flag) {
      repo_is_active = false;
    }

    return (
      <section className="app-navi-bar">
        <ul className="nav nav-tabs">
          <li className='nav-item' >
            <Link className={ repo_is_active?'active nav-link':'nav-link' } to={{ pathname:'/' + owner }} >项目</Link>
          </li>
          <li className='nav-item' >
            <Link className={ people_is_active?'active nav-link':'nav-link' } to={{ pathname:'/orgs/' + owner + '/people' }} >人员</Link>
          </li>
          <li className='nav-item'>
            <Link className={ warning_is_active?'active nav-link':'nav-link' } to={{ pathname:'/orgs/' + owner + '/warning' }} >报警</Link>
          </li>
          <li className='nav-item'>
            <Link className={ settings_is_active?'active nav-link':'nav-link' } to={{ pathname:'/orgs/' + owner + '/settings' }} >设置</Link>
          </li>
        </ul>
      </section>
    );
  }
}

OrgAppNaviBar.propTypes = {
  owner: PropTypes.string.isRequired
};

OrgAppNaviBar.contextTypes = {
  router: PropTypes.object.isRequired
};
