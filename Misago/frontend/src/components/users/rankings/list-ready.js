import React from 'react';
import ListItem from 'misago/components/users/rankings/list-item'; // jshint ignore:line

export default class extends React.Component {
  getLeadMessage() {
    let message = ngettext(
        "Top %(count)s in %(participants)s submitter.",
        "Top %(count)s in %(participants)s submitters.",
        this.props.count);
    return interpolate(message, {
      count: this.props.count,
      participants: this.props.participants
    }, true);
  }

  render() {
    /* jshint ignore:start */
    return <div className="active-posters-list">
      <div className="container">
        <p className="lead">
          {this.getLeadMessage()}
        </p>

        <div className="active-posters ui-ready">
          <ul className="list-group">
            {this.props.users.map((user, i) => {
              return <ListItem user={user}
                               rank={user.rank}
                               counter={i + 1}
                               key={user.id} />;
            })}
          </ul>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}