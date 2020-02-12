import React from 'react';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Button from '@material-ui/core/Button';
import MenuIcon from '@material-ui/icons/Menu';
import AppBar from '@material-ui/core/AppBar';

import requests from '../../lib/requests';

import useStyles from './styles';


export default function ({ handleDrawerToggle }) {
  const classes = useStyles();
  return (
    <AppBar position="fixed" className={classes.appBar}>
      <Toolbar>
        <IconButton
          onClick={handleDrawerToggle}
          className={classes.menuButton}
        >
          <MenuIcon />
        </IconButton>
        <Button
          color="primary"
          onClick={
            () => requests.post('/users/logout/').then(
              () => window.location = '/'
            )
          }
        >
          Выйти
        </Button>
      </Toolbar>
    </AppBar>
  );
}
