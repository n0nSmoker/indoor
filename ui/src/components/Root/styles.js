import { makeStyles } from '@material-ui/core/styles';


const RootStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    height: '100vh',
    overflow: 'hidden',
  },
  pageContainer: {
    flexGrow: 1,
    padding: theme.spacing(3),
    marginTop: 64,
  },
  pageContent: {
    height: `calc(100vh - 64px - ${theme.spacing(6)}px)`,
    overflow: 'auto',
    position: 'relative',
  },
}));


export default RootStyles;
