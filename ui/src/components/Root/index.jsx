import React from 'react';
import { ThemeProvider } from '@material-ui/core';
import CssBaseline from '@material-ui/core/CssBaseline';

import Header from 'components/Header';
import Drawer from 'components/Drawer';
import Notifications from 'components/Notifications';

import useStyles from './styles';
import theme from './theme';


function Root({ children }) {
  const classes = useStyles();
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Notifications />
      <div className={classes.root}>
        <Header handleDrawerToggle={handleDrawerToggle} />
        <Drawer
          classes={classes}
          mobileOpen={mobileOpen}
          handleDrawerToggle={handleDrawerToggle}
        />
        <main className={classes.pageContainer}>
          <div className={classes.pageContent}>
            {children}
          </div>
        </main>
      </div>
    </ThemeProvider>
  );
}

export default Root;
