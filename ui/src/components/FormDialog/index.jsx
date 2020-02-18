import React from 'react';
import PropTypes from 'prop-types';
import Slide from '@material-ui/core/Slide';
import Dialog from '@material-ui/core/Dialog';
import Button from '@material-ui/core/Button';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogActions from '@material-ui/core/DialogActions';
import { makeStyles } from '@material-ui/core/styles';


const Transition = React.forwardRef(
  (props, ref) => <Slide direction="up" ref={ref} {...props} />
);

const useStyles = makeStyles(theme => ({
  content: {
    paddingBottom: theme.spacing(4),
  }
}));

export default function Form({ open, title, handleClose, handleSubmit, children, isValid }) {
  const classes = useStyles();
  return (
    <Dialog
      fullWidth
      maxWidth="sm"
      open={open}
      onClose={handleClose}
      TransitionComponent={Transition}
    >
      <DialogTitle>
        {title}
      </DialogTitle>
      <DialogContent dividers className={classes.content}>
        {children}
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>
          Отмена
        </Button>
        <Button
          disabled={!isValid}
          onClick={handleSubmit}
          color="primary"
        >
          Сохранить
        </Button>
      </DialogActions>
    </Dialog>
  );
}

Form.propTypes = {
  open: PropTypes.bool,
  title: PropTypes.string,
  handleClose: PropTypes.func,
  handleSubmit: PropTypes.func,
  children: PropTypes.node,
  isValid: PropTypes.bool,
};
