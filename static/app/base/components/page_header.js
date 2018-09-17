import React from 'react';
import PropTypes from 'prop-types'

export default class PageHeader extends React.Component{
  constructor(props) {
    super(props);
  }
  render() {
    let index_page_url = this.props.url.index_page; // {{ url_for('get_index_page') }}
    return (
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <a className="navbar-brand" href={ index_page_url }>NWPC业务监控平台</a>

        <ul className="navbar-nav mr-auto">
          <li className="nav-item active">
            <a className="nav-link" href={ index_page_url }>首页</a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">功能</a>
          </li>
        </ul>

        <form className="form-inline">
          <input className="form-control" type="text" placeholder="Search" />
        </form>

        <ul className="navbar-nav float-right">
          <li className="nav-item">
            <a className="nav-link" href="#">帮助</a>
          </li>
          <li className="nav-item dropdown">
            <a className="nav-link dropdown-toggle" href="#" id="page_header_nav_user_drop_down"
               data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">用户</a>
            <div className="dropdown-menu dropdown-menu-right" aria-labelledby="page_header_nav_user_drop_down">
              <a className="dropdown-item" href="#">主页</a>
              <a className="dropdown-item" href="#">帮助</a>
              <div className="dropdown-divider" />
              <a className="dropdown-item" href="#">设置</a>
              <a className="dropdown-item" href="#">注销</a>
            </div>
          </li>
        </ul>
      </nav>
    );
  }
}

PageHeader.propTypes = {
  url: PropTypes.objectOf(PropTypes.string).isRequired
};


