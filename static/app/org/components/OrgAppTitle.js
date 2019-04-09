import React from 'react';
import PropTypes from 'prop-types'

import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faChessKing from '@fortawesome/fontawesome-free-solid/faChessKing'

export default class OrgAppTitle extends React.Component{
  constructor(props) {
    super(props);
  }
  render() {
    let owner = this.props.owner;
    return (
      <section className="row">
        <h1>
          <FontAwesomeIcon icon={faChessKing} />
          <a href={ '/' + owner }>{ owner }</a>
        </h1>
      </section>
    );
  }
}

OrgAppTitle.propTypes = {
  owner: PropTypes.string.isRequired
};
