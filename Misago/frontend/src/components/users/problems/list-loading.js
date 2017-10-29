import React from 'react';
import ProblemsList from 'misago/components/users/problems/problems-list' // jshint ignore:line

export default class extends React.Component {
  shouldComponentUpdate() {
    return false;
  }

  render() {
    /* jshint ignore:start */
    return (
      <div>
        <ProblemsList
          cols={4}
          isReady={false}
        />
      </div>
    );
    /* jshint ignore:end */
  }
}
