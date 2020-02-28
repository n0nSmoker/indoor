import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { ThemeProvider } from '@material-ui/core';
import CssBaseline from '@material-ui/core/CssBaseline';
import { withStyles } from '@material-ui/core/styles';

import Header from 'components/Header';
import Drawer from 'components/Drawer';
import Loader from 'components/Loader';
import Notifications from 'components/Notifications';

import { fetchCurrentUser as fetchCurrentUserAction } from './actions';
import styles from './styles';
import theme from './theme';


class Root extends React.Component {
  state = {mobileOpen: false};

  componentDidMount() {
    const { fetchCurrentUser } = this.props;
    fetchCurrentUser();
  }

  handleDrawerToggle = () => {
    this.setState(state => ({
      mobileOpen: !state.mobileOpen,
    }));
  };

  render () {
    const { mobileOpen } = this.state;
    const { classes, children, isLoading, currentUser } = this.props;
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Notifications />
        {isLoading
          ? <Loader size={50} thickness={5} />
          : (
            <div className={classes.root}>
              {/* TODO: combine header and drawer components */}
              <Header handleDrawerToggle={this.handleDrawerToggle} currentUser={currentUser} />
              <Drawer
                classes={classes}
                mobileOpen={mobileOpen}
                handleDrawerToggle={this.handleDrawerToggle}
                currentUser={currentUser}
              />
              <main className={classes.pageContainer}>
                <div className={classes.pageContent}>
                  {children}
                </div>
              </main>
            </div>
          )}
      </ThemeProvider>
    );
  }
}

Root.propTypes = {
  classes: PropTypes.object,
  children: PropTypes.node,
  isLoading: PropTypes.bool,
  currentUser: PropTypes.object,
  fetchCurrentUser: PropTypes.func,
};

const mapStateToProps = ({ rootReducer }) => ({ ...rootReducer });

const mapDispatchToProps = {
  fetchCurrentUser: fetchCurrentUserAction,
};

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(Root));
