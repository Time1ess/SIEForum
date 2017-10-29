/* jshint ignore:start */
import React from 'react';
import Pager from 'misago/components/users/problems/pager';
import ProblemsList from 'misago/components/users/problems/problems-list';

export default function(props) {
  return (
    <div>
      <ProblemsList
        cols={4}
        isReady={true}
        showStatus={true}
        problems={props.problems}
      />
      <Pager {...props} />
    </div>
  );
}