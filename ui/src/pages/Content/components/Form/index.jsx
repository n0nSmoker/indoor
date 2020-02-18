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
      file: data.airtime,
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

  const handleChangeFile = ({ target: { files, name } }) => {
    setFormData({
      ...formData,
      [name]: files[0]
    });
  };

  const isValid = () => {
    return !!(isEdit ? true : formData.file)
  };

  return (
    <FormDialog
      open
      title={
        isEdit
          ? `Редактирование контента ${data.name}`
          : 'Создание контента'
      }
      handleClose={handleClose}
      handleSubmit={() => handleSubmit(formData)}
      isValid={isValid()}
    >
      <form className={classes.form} encType='multipart/form-data'>
        <TextField
          fullWidth
          name="file"
          type="file"
          onChange={handleChangeFile}
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
