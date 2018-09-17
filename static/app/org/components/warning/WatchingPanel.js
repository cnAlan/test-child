import React from 'react';
import PropTypes from 'prop-types'

import WatcherList from './WatcherList'

export default class WatchingPanel extends React.Component{
  constructor(props) {
    super(props);
  }

  render() {
    const {owner, repo_count} = this.props;
    let watching_user_list = this.props.watching_user_list;

    return (
      <div>
        <h4>推送列表</h4>
        <WatcherList
          type={this.props.type}
          watcher_list = {watching_user_list}
          owner={owner}
          repo_count={repo_count}
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
    watching_repo_count: PropTypes.number
  })).isRequired,
  owner: PropTypes.string.isRequired,
  repo_count: PropTypes.number,
  unwatch_click_handler: PropTypes.func.isRequired,
  watch_click_handler: PropTypes.func.isRequired
};