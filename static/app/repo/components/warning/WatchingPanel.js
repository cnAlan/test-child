import React from 'react';
import PropTypes from 'prop-types'

import WatcherList from './WatcherList'

export default class WatchingPanel extends React.Component{
  constructor(props) {
    super(props);
  }

  handleUnWatchClick(owner, repo, user, event) {
    this.props.unwatch_click_handler(owner, repo, user)
  }

  render() {
    const {owner, repo} = this.props;
    let watching_user_list = this.props.watching_user_list;

    return (
      <div>
        <h4>推送列表</h4>
        <WatcherList
          type={this.props.type}
          watcher_list = {watching_user_list}
          owner={owner}
          repo={repo}
          unwatch_click_handler={this.props.unwatch_click_handler}
          watch_click_handler={this.props.watch_click_handler}
        />
      </div>
    );
  }
}

WatchingPanel.propTypes = {
  type: PropTypes.string.isRequired,
  watching_user_list: PropTypes.arrayOf(PropTypes.shape({
    owner_name: PropTypes.string.isRequired,
    is_watching:PropTypes.bool.isRequired,
    warn_watch: PropTypes.shape({
      start_date_time: PropTypes.string,
      end_date_time: PropTypes.string
    })
  })).isRequired,
  owner: PropTypes.string.isRequired,
  repo: PropTypes.string.isRequired,
  unwatch_click_handler: PropTypes.func.isRequired,
  watch_click_handler: PropTypes.func.isRequired
};