import React from 'react';
import ListEmpty from 'misago/components/users/rankings/list-empty'; // jshint ignore:line
import ListPreview from 'misago/components/users/rankings/list-preview'; // jshint ignore:line
import ListReady from 'misago/components/users/rankings/list-ready'; // jshint ignore:line
import misago from 'misago/index';
import { hydrate } from 'misago/reducers/users';
import polls from 'misago/services/polls';
import store from 'misago/services/store';
import title from 'misago/services/page-title';

export default class extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoaded: true,
    };
    if (misago.has('USERS')) {
        this.initWithPreloadedData(misago.pop('USERS'));
    } else {
        this.initWithoutPreloadedData();
    }

    this.startPolling();
  }

  initWithPreloadedData(data) {
    this.state = {
      isLoaded: true,

      participants: data.participants,
      count: data.count
    };

    store.dispatch(hydrate(data.results));
  }

  initWithoutPreloadedData() {
    this.state = {
      isLoaded: false
    };
  }

  startPolling() {
    polls.start({
      poll: 'rankings',
      url: misago.get('RANKINGS_API'),
      data: {
        PROBLEM_UID: 1
      },
      frequency: 90 * 1000,
      update: this.update
    });
  }

  /* jshint ignore:start */
  update = (data) => {
    store.dispatch(hydrate(data.results));

    this.setState({
      isLoaded: true,

      participants: data.participants,
      count: data.count
    });
  };
  /* jshint ignore:end */

  componentDidMount() {
    title.set({
      title: this.props.route.extra.name,
      parent: gettext("Users")
    });
  }

  componentWillUnmount() {
    polls.stop('rankings');
  }

  render() {
    if (this.state.isLoaded) {
      if (this.state.count > 0) {
        /* jshint ignore:start */
        return <ListReady users={this.props.users}
                          participants={this.state.participants}
                          count={this.state.count} />;
        /* jshint ignore:end */
      } else {
        /* jshint ignore:start */
        return <ListEmpty />;
        /* jshint ignore:end */
      }
    } else {
      /* jshint ignore:start */
      return <ListPreview />;
      /* jshint ignore:end */
    }
  }
}