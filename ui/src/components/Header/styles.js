import { makeStyles } from '@material-ui/core/styles';


const HeaderStyles = makeStyles(theme => ({
  appBar: {
    backgroundColor: 'white',
    [theme.breakpoints.up('sm')]: {
      width: `calc(100% - 200px)`,
      marginLeft: 200,
    },
    color: 'black',
    '& > div': {
      justifyContent: 'flex-end',
    },
  },
  menuButton: {
    marginRight: 'auto',
    [theme.breakpoints.up('sm')]: {
      display: 'none',
    },
  },
}));


export default HeaderStyles;
