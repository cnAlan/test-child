import React from 'react';
import PropTypes from 'prop-types'

export default class WatcherList extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      checked_users: []
    };
  }

  handleUnWatchClick(owner, repo, user, event) {
    let users = [user];
    this.props.unwatch_click_handler(owner, repo, users)
  }

  handleWatchClick(owner, repo, user, event) {
    let users = [user];
    this.props.watch_click_handler(owner, repo, users)
  }

  handleAllCheckClick() {
    const { watcher_list } = this.props;
    let user_list = [];
    watcher_list.forEach( function(item, index, array) {
      user_list.push(item.owner_name);
    });
    this.setState({ checked_users: user_list});
  }

  handleAllUnCheckClick() {
    this.setState( { checked_users: [] });
  }

  handleCheckboxChange(user, event) {
    let flag = event.target.checked;
    if(flag) {
      let user_index = this.state.checked_users.indexOf(user);
      if (user_index === -1) {
        let new_checked_users = this.state.checked_users;
        new_checked_users.push(user);
        this.setState({checked_users: new_checked_users});
      }
    }
    else{
      let user_index = this.state.checked_users.indexOf(user);
      if (user_index!==-1) {
        let new_checked_users = this.state.checked_users;
        new_checked_users.splice(user_index, 1);
        this.setState( { checked_users: new_checked_users});
      }
    }
  }

  handleCheckedWatchClick(event){
    const { owner, repo } = this.props;
    this.props.watch_click_handler(owner, repo, this.state.checked_users);
  }

  handleCheckedUnWatchClick(event){
    const { owner, repo } = this.props;
    this.props.unwatch_click_handler(owner, repo, this.state.checked_users);
  }

  render() {
    const {owner, repo} = this.props;
    let watcher_list = this.props.watcher_list;

    return (
      <div>
        <ul className="list-group">
          {watcher_list.map((an_user, index) =>
            <li className="list-group-item" key={an_user.owner_name}>
              <label>
                <input type="checkbox" value={an_user.owner_name}
                       onChange={this.handleCheckboxChange.bind(this, an_user.owner_name)}
                       checked={ this.state.checked_users.indexOf(an_user.owner_name) !== -1 }
                />
                &nbsp;
                <a href={ '/' + an_user.owner_name }>{an_user.owner_name}</a>
              </label>
              {
                an_user.is_watching?
                  (<button className="btn btn-danger btn-sm active float-right"
                           onClick={this.handleUnWatchClick.bind(this, owner, repo, an_user.owner_name)}>
                    取消
                  </button>) :
                  (<button className="btn btn-primary btn-sm float-right"
                           onClick={this.handleWatchClick.bind(this, owner, repo, an_user.owner_name)}>
                    关注
                  </button>)
              }
            </li>
          )}
          <li className="list-group-item">
            <button type="button" className="btn btn-light btn-sm" onClick={this.handleAllCheckClick.bind(this)}>
              全选
            </button>
            <button type="button" className="btn btn-light btn-sm" onClick={this.handleAllUnCheckClick.bind(this)}>
              取消全选
            </button>
            <button className="btn btn-light btn-sm float-right" onClick={this.handleCheckedUnWatchClick.bind(this)}>
              取消
            </button>
            <button className="btn btn-light btn-sm float-right" onClick={this.handleCheckedWatchClick.bind(this)}>
              关注
            </button>
          </li>
        </ul>
      </div>
    );
  }
}

WatcherList.propTypes = {
  type: PropTypes.string.isRequired,

  watcher_list: PropTypes.arrayOf(PropTypes.shape({
    owner_name: PropTypes.string.isRequired,
    is_watching:PropTypes.bool.isRequired,
    warn_watch: PropTypes.shape({
      start_date_time: PropTypes.string,
      end_date_time: PropTypes.string
    })
  })).isRequired,

  owner: PropTypes.string.isRequired,
  repo: PropTypes.string.isRequired,

  /**
   * 取消某个项目的关注时调用的函数
   *  unwatch_click_handler(owner, repo, users)
   */
  unwatch_click_handler: PropTypes.func.isRequired,

  /**
   * 关注某个项目时调用的函数
   *  unwatch_click_handler(owner, repo, users)
   */
  watch_click_handler: PropTypes.func.isRequired
};