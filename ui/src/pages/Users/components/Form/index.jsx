import React from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';

import FormDialog from '../../../../components/FormDialog';

import { rolesOptions } from '../../helpers';


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
      email: data.email,
      role: data.role,
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
    return Boolean(formData.name && formData.email && (isEdit || formData.password))
  };

  return (
    <FormDialog
      open
      title={
        isEdit
          ? `Редактирование пользователя ${data.name}`
          : 'Создание пользователя'
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
          name="email"
          label="Email"
          value={formData.email || ""}
          onChange={handleChange}
          variant="outlined"
          margin="dense"
        />
        <TextField
          fullWidth
          name="password"
          label="Пароль"
          type="password"
          value={formData.password || ""}
          onChange={handleChange}
          variant="outlined"
          margin="dense"
        />
        <TextField
          fullWidth
          select
          name="role"
          label="Роль"
          value={formData.role}
          onChange={handleChange}
          variant="outlined"
          margin="dense"
          SelectProps={{
            native: true,
          }}
        >
          {rolesOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </TextField>
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
