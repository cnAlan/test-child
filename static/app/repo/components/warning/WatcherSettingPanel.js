import React from 'react';
import PropTypes from 'prop-types'

import WatcherList from './WatcherList'

export default class WatcherSettingPanel extends React.Component{
  constructor(props) {
    super(props);
  }

  render() {
    const { id, owner, repo, suggested_user_list } = this.props;
    return (
      <div>
        <h4 id={id}>人员设置</h4>
        <p>{owner}小组成员</p>

        <WatcherList
          type={this.props.type}
          watcher_list = {suggested_user_list}
          owner={owner}
          repo={repo}
          unwatch_click_handler={this.props.unwatch_click_handler}
          watch_click_handler={this.props.watch_click_handler}
        />

        <div className="row">
          <div className="col-md-6">

          </div>
          <div className="col-md-6">

          </div>
        </div>
        <div>
          <h5>其他用户</h5>
          <p>建设中</p>
        </div>
      </div>
    );
  }
}

WatcherSettingPanel.propTypes = {
  id: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  suggested_user_list: PropTypes.arrayOf(PropTypes.shape({
    owner_name: PropTypes.string.isRequired,
    is_watching: PropTypes.bool.isRequired,
    warn_watch: PropTypes.shape({
      start_date_time: PropTypes.string,
      end_date_time: PropTypes.string
    })
  })).isRequired,
  owner: PropTypes.string.isRequired,
  repo: PropTypes.string.isRequired,
  watch_click_handler: PropTypes.func.isRequired,
  unwatch_click_handler: PropTypes.func.isRequired
};