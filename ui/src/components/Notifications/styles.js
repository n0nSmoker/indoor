import green from '@material-ui/core/colors/green';
import blue from '@material-ui/core/colors/blue';
import amber from '@material-ui/core/colors/amber';


export default theme => ({
  success: {
    backgroundColor: green[500],
  },
  error: {
    backgroundColor: theme.palette.error.dark,
  },
  info: {
    backgroundColor: blue[500],
  },
  warning: {
    backgroundColor: amber[500],
  },
  message: {
    whiteSpace: 'pre',
  },
});
