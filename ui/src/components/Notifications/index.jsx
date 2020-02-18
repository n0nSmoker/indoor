import React from 'react';
import PropTypes from 'prop-types';
import cn from 'classnames';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import Snackbar from '@material-ui/core/Snackbar';
import SnackbarContent from '@material-ui/core/SnackbarContent';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';

import { closeAction } from './actions';
import styles from './styles';


function Notifications({ open, message, duration, variant, close, classes }) {
  return (
    <Snackbar
      anchorOrigin={{
        vertical: 'top',
        horizontal: 'right',
      }}
      open={open}
      autoHideDuration={duration}
      onClose={close}
    >
      <SnackbarContent
        className={cn(classes.message, classes[variant || 'info'])}
        message={message}
        action={
          <IconButton size="small" color="inherit" onClick={close}>
            <CloseIcon fontSize="small" />
          </IconButton>
        }
      />
    </Snackbar>
  );
}

Notifications.propTypes = {
  open: PropTypes.bool,
  message: PropTypes.string,
  duration: PropTypes.number,
  variant: PropTypes.string,
  close: PropTypes.func,
  classes: PropTypes.object,
};

const mapStateToProps = ({ notificationReducer }) => ({ ...notificationReducer });

const mapDispatchToProps = {
  close: closeAction,
};

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(Notifications));
