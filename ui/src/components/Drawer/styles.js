import { makeStyles } from '@material-ui/core/styles';


const drawerWidth = 200;
const DrawerStyles = makeStyles(theme => ({
  container: {
    [theme.breakpoints.up('sm')]: {
      width: drawerWidth,
      flexShrink: 0,
    },
    position: 'relative',
  },
  logo: {
    fontWeight: 'bold',
    lineHeight: '64px',
  },
  listIcon: {
    color: 'white',
  },
  divider: {
    backgroundColor: 'rgba(255, 255, 255, 0.5)',
  },
  navLink: {
    color: 'white',
    textDecoration: 'none',
    '&.active > div': {
      borderLeftColor: 'white',
      borderLeftWidth: 3,
      borderLeftStyle: 'solid',
      backgroundColor: 'rgba(255, 255, 255, 0.1)',
    },
  },
  version: {
    position: 'absolute',
    left: theme.spacing(1),
    bottom: theme.spacing(1),
    fontWeight: 'bold',
  },
  paper: {
    width: drawerWidth,
    backgroundColor: theme.palette.primary.main,
    color: 'white',
  },
}));

export default DrawerStyles;
