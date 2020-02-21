import React from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';

import FormDialog from '../../../../components/FormDialog';

import { statusOptions } from '../../helpers';


const useStyles = makeStyles(theme => ({
  form: {
    '& > div:not(:last-child)': {
      marginBottom: theme.spacing(2),
    },
  }
}));


export default function Form({ data, citiesData, cityId, locationsData, handleClose, handleSubmit, handleChangeCity }) {
  const classes = useStyles();
  const isEdit = data && data.id;
  const initialFormData = isEdit
    ? {
      location_id: data.location ? data.location.id : '',
      comment: data.comment,
      status: data.status,
    }
    : {};
  const [formData, setFormData] = React.useState(initialFormData);
  const handleChange = ({ target }) => {
    setFormData({
      ...formData,
      [target.name]: target.value
    });
  };

  return (
    <FormDialog
      open
      title={
        isEdit
          ? `Редактирование устройства ${data.id}`
          : 'Создание стройства'
      }
      handleClose={handleClose}
      handleSubmit={() => handleSubmit(formData)}
      isValid={true}
    >
      <form className={classes.form}>
        <TextField
          fullWidth
          select
          name="city_id"
          label="Город"
          value={cityId || ''}
          onChange={handleChangeCity}
          variant="outlined"
          margin="dense"
          SelectProps={{
            native: true,
            displayEmpty: true,
          }}
          InputLabelProps={{ shrink: true }}
        >
          <option value=''>Не указан</option>
          {citiesData.map(option => (
            <option key={option.id} value={option.id}>
              {option.name}
            </option>
          ))}
        </TextField>
        <TextField
          disabled={!cityId}
          fullWidth
          select
          name="location_id"
          label="Адрес"
          value={formData.location_id || ''}
          onChange={handleChange}
          variant="outlined"
          margin="dense"
          SelectProps={{
            native: true,
            displayEmpty: true,
          }}
          InputLabelProps={{ shrink: true }}
        >
          <option value=''>Не указан</option>
          {locationsData.map(option => (
            <option key={option.id} value={option.id}>
              {option.address}
            </option>
          ))}
        </TextField>
        <TextField
          fullWidth
          select
          name="status"
          label="Статус"
          value={formData.status}
          onChange={handleChange}
          variant="outlined"
          margin="dense"
          SelectProps={{
            native: true,
          }}
        >
          {statusOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </TextField>
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
  cityId: PropTypes.number,
  handleClose: PropTypes.func,
  handleSubmit: PropTypes.func,
  handleChangeCity: PropTypes.func,
};
