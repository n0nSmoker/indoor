import React from 'react';
import { NavLink } from 'react-router-dom';
import Divider from '@material-ui/core/Divider';
import Hidden from '@material-ui/core/Hidden';
import { default as DrawerComponent } from '@material-ui/core/Drawer';
import Typography from '@material-ui/core/Typography';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import GroupIcon from '@material-ui/icons/Group';
import MovieIcon from '@material-ui/icons/Movie';
import VideoLibraryIcon from '@material-ui/icons/VideoLibrary';

import useStyles from './styles';


export default function AppDrawer({ mobileOpen, handleDrawerToggle }) {
  const classes = useStyles();
  let props = {
    classes: {
      paper: classes.paper,
    },
    children: (
      <>
        <Typography className={classes.logo}
          variant="h5"
          align="center"
        >
          InDoor
        </Typography>
        <Divider className={classes.divider} />
        <List>
          <NavLink
            to="/users/"
            className={classes.navLink}
          >
            <ListItem button>
              <ListItemIcon>
                <GroupIcon className={classes.listIcon} />
              </ListItemIcon>
              <ListItemText primary="Пользователи" />
            </ListItem>
          </NavLink>
          <NavLink
            to="/publishers/"
            className={classes.navLink}
          >
            <ListItem button>
              <ListItemIcon>
                <MovieIcon className={classes.listIcon} />
              </ListItemIcon>
              <ListItemText primary="Рекламодатели" />
            </ListItem>
          </NavLink>
          <NavLink
            to="/content/"
            className={classes.navLink}
          >
            <ListItem button>
              <ListItemIcon>
                <VideoLibraryIcon className={classes.listIcon} />
              </ListItemIcon>
              <ListItemText primary="Контент" />
            </ListItem>
          </NavLink>
        </List>
        <Typography
          variant="subtitle2"
          className={classes.version}
        >
          {VERSION}
        </Typography>
      </>
    ),
  };
  return (
    <nav className={classes.container}>
      <Hidden smUp>
        <DrawerComponent
          variant='temporary'
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          {...props}
        />
      </Hidden>
      <Hidden xsDown>
        <DrawerComponent
          variant="permanent"
          open
          {...props}
        />
      </Hidden>
    </nav>
  );
}
