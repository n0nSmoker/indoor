import React from 'react';
import { ThemeProvider } from '@material-ui/core';
import CssBaseline from '@material-ui/core/CssBaseline';

import Header from '../Header';
import Drawer from '../Drawer';

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
