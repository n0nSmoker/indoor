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
    [theme.breakpoints.up('sm')]: {
      display: 'none',
    },
  },
  addButton: {
    marginLeft: theme.spacing(3),
    fontWeight: 'bold',
  },
  grow: {
    flexGrow: 1,
  },
  search: {
    width: 270,
    marginRight: theme.spacing(3),
  },
  searchInputRoot: {
    padding: `0 ${theme.spacing(1)}px`,
  },
  searchInput: {
    padding: `${theme.spacing(1)}px ${theme.spacing(2)}px`
  },
  searchClose: {
    cursor: 'pointer',
  },
}));


export default HeaderStyles;
