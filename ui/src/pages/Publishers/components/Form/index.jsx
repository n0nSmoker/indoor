import React from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';

import FormDialog from '../../../../components/FormDialog';


const useStyles = makeStyles(theme => ({
  form: {
    '& > div:not(:last-child)': {
      marginBottom: theme.spacing(2),
    },
  }
}));


export default function Form({ data, handleClose, handleSubmit }) {
  const classes = useStyles();
  const isEdit = data && data.id;
  const initialFormData = isEdit
    ? {
      name: data.name,
      airtime: data.airtime,
      comment: data.comment,
    }
    : {};
  const [formData, setFormData] = React.useState(initialFormData);

  const handleChange = ({ target }) => {
    setFormData({
      ...formData,
      [target.name]: target.value
    });
  };

  const isValid = () => {
    return !!(formData.name && formData.airtime)
  };

  return (
    <FormDialog
      open
      title={
        isEdit
          ? `Редактирование рекламодателя ${data.name}`
          : 'Создание рекламодателя'
      }
      handleClose={handleClose}
      handleSubmit={() => handleSubmit(formData)}
      isValid={isValid()}
    >
      <form className={classes.form}>
        <TextField
          fullWidth
          name="name"
          label="Имя"
          value={formData.name || ""}
          onChange={handleChange}
          variant="outlined"
          margin="dense"
        />
        <TextField
          fullWidth
          name="airtime"
          label="Эфирное время"
          type="number"
          value={formData.airtime || ""}
          onChange={handleChange}
          inputProps={{
            min: '0.1',
            max: '100',
            step: '0.1',
          }}
          variant="outlined"
          margin="dense"
        />
        <TextField
          fullWidth
          name="comment"
          label="Комментарий"
          value={formData.comment || ""}
          onChange={handleChange}
          variant="outlined"
          margin="dense"
        />
      </form>
    </FormDialog>
  );
}

Form.propTypes = {
  open: PropTypes.bool,
  data: PropTypes.object,
  handleClose: PropTypes.func,
  handleSubmit: PropTypes.func,
};
