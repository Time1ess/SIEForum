// jshint ignore:start
import React from 'react';
import Card from './card';
import Preview from './preview';


export default function({ cols, isReady, showStatus, problems }) {
  let colClassName = 'col-xs-12 col-sm-4';
  if (cols === 4) {
    colClassName += ' col-md-3';
  }
  if (!isReady) {
    return (
      <Preview
        colClassName={colClassName}
        cols={cols}
      />
    );
  }
  return (
    <div className="users-cards-list ui-ready">
      <div className="row">
        {problems.map((problem) => {
          return (
            <div
              className={colClassName}
              key={problem.id}
            >
              <Card
                showStatus={showStatus}
                problem={problem}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
}
