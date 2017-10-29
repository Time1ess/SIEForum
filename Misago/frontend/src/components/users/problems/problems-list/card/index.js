// jshint ignore:start
import React from 'react';
import Avatar from 'misago/components/avatar';
import Stats from './stats';
import UserTitle from './user-title';

export default function({ showStatus, problem }) {
  let className = 'panel user-card';

  return (
    <div className={className}>
      <div className="panel-body">
        <div className="row">
          <div className="col-xs-3 user-card-left">
            <div className="user-card-small-avatar">
            </div>
          </div>
          <div className="col-xs-9 col-sm-12 user-card-body">
            <div className="user-card-username">
              <a href={problem.url}>
                {problem.thread_title}
              </a>
            </div>
            <div className="user-card-title">
              <a href={problem.starter.url}>
                {gettext("Starter")}:{problem.starter.name}
              </a>
            </div>

            <div className="user-card-stats">
                {gettext("Participants")}:{problem.solutions}
              <a href={problem.ranking_url}>
                {gettext("View Rankings")}
              </a>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}