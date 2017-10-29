import React from 'react';
import PageLead from 'misago/components/page-lead' // jshint ignore:line
import List from 'misago/components/users/problems/list' // jshint ignore:line
import ListLoading from 'misago/components/users/problems/list-loading' // jshint ignore:line
import misago from 'misago/index';
//import { hydrate } from 'misago/reducers/users';
import polls from 'misago/services/polls';
//import store from 'misago/services/store';
import title from 'misago/services/page-title';

export default class extends React.Component {
  constructor(props) {
    super(props);
    if (misago.has('PROBLEMS')) {
      this.initWithPreloadedData(misago.pop('PROBLEMS'));
    } else {
      this.initWithoutPreloadedData();
    }

    this.startPolling(props.params.page || 1);
  }

  initWithPreloadedData(data) {
    this.state = Object.assign(data, {
      isLoaded: true
    });
  }

  initWithoutPreloadedData() {
    this.state = {
      isLoaded: false
    };
  }

  startPolling(page) {
    polls.start({
      poll: 'problems',
      url: misago.get('PROBLEMS_API'),
      data: {
        page: page
      },
      frequency: 90 * 1000,
      update: this.update
    });
  }

  /* jshint ignore:start */
  update = (data) => {
    data.isLoaded = true;
    this.setState(data);
  };
  /* jshint ignore:end */

  componentDidMount() {
    title.set({
      title: this.props.route.extra.name,
      page: this.props.params.page || null,
      parent: gettext("Users")
    });
  }

  componentWillUnmount() {
    polls.stop('problems');
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.params.page !== nextProps.params.page) {
      title.set({
        title: this.props.route.extra.name,
        page: nextProps.params.page || null,
        parent: gettext("Available Problems")
      });

      this.setState({
        isLoaded: false
      });

      polls.stop('problems');
      this.startPolling(nextProps.params.page);
    }
  }

  getComponent() {
    if (this.state.isLoaded) {
      if (this.state.count > 0) {
        /* jshint ignore:start */
        let baseUrl = misago.get('PROBLEMS_URL');
        return <List baseUrl={baseUrl}
                     users={this.props.users}
                     {...this.state} />;
        /* jshint ignore:end */
      } else {
        /* jshint ignore:start */
        return <p className="lead">
          {gettext("There are no problems yet.")}
        </p>;
        /* jshint ignore:end */
      }
    } else {
      /* jshint ignore:start */
      return <ListLoading />;
      /* jshint ignore:end */
    }
  }

  render() {
    /* jshint ignore:start */
    return <div>
      <div className="container">
        {this.getComponent()}
      </div>
    </div>;
    /* jshint ignore:end */
  }
}