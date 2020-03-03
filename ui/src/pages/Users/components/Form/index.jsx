import React from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';

import FormDialog from 'components/FormDialog';
import ServerSelect from 'components/ServerSelect';
import { USERS_ROLE_ADMIN, USERS_ROLE_MANAGER } from 'pages/Users/consts';
import { rolesOptions } from 'pages/Users/helpers';


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
      ...(data.publisher ? { publisher_id: data.publisher.id } : {}),
    }
    : {
      role: USERS_ROLE_MANAGER,
    };
  const [formData, setFormData] = React.useState(initialFormData);

  const handleChange = ({ target: { name, value }}) => {
    const newFormData = {...formData, [name]: value};
    if (name === 'role' && value === USERS_ROLE_ADMIN) {
      delete newFormData.publisher_id;
    }
    setFormData(newFormData);
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
          autoComplete="off"
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
        {formData.role !== USERS_ROLE_ADMIN &&
          <ServerSelect
            name="publisher_id"
            initialValue={isEdit ? data.publisher : null}
            onChange={handleChange}
            path='publishers'
            valueKey='id'
            labelKey='name'
            label='Рекламодатель'
          />}
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
