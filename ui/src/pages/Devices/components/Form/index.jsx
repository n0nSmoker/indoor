import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';

import TextField from '@material-ui/core/TextField';
import IconButton from '@material-ui/core/IconButton';
import AddIcon from '@material-ui/icons/Add';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

import FormDialog from '../../../../components/FormDialog';

import { statusOptions } from '../../helpers';


const useStyles = makeStyles(theme => ({
  form: {
    '& > div:not(:last-child)': {
      marginBottom: theme.spacing(2),
    },
  }
}));


export default function Form({
  data,
  citiesData,
  cityId,
  locationsData,
  handleClose,
  handleSubmit,
  handleChangeCity,
  handleLocationSubmit
}) {
  const classes = useStyles();
  const isEdit = data && data.id;
  // TODO: make formData stand alone
  const initialFormData = isEdit
    ? {
      location_id: data.location ? data.location.id : null,
      comment: data.comment,
      status: data.status,
    }
    : {};

  const initialLocationFormData = {
    address: '',
  };

  const initialState = {
    locationFormOpen: false,
  };

  const [formData, setFormData] = React.useState(initialFormData);
  const [state, setState] = React.useState(initialState);
  const [locationFormData, setLocationFormData] = React.useState(initialLocationFormData);

  const handleChange = ({ target }) => {
    setFormData({
      ...formData,
      [target.name]: target.value
    });
  };

  const showLocationForm = () => {
    setState({
      ...state,
      locationFormOpen: true,
    })
  };

  const hideLocationForm = () => {
    setState({
      ...state,
      locationFormOpen: false,
    })
  };

  const handleChangeLocation = ({ target }) => {
    setLocationFormData({
      ...locationFormData,
      [target.name]: target.value
    })
  };

  const isValid = () => {
    return Boolean(locationFormData.address && cityId)
  };

  return (
    <>
      <FormDialog
        open
        title={`Редактирование устройства ${data.id}`}
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
          <Paper
            style={{
              padding: '2px 4px',
              display: 'flex',
              alignItems: 'center',
              width: '100%'
            }}>
            <TextField
              disabled={!cityId}
              fullWidth
              select
              name="location_id"
              label="Адрес"
              value={cityId ? formData.location_id || '' : ''}
              onChange={handleChange}
              variant="outlined"
              margin="dense"
              SelectProps={{
                native: true,
                displayEmpty: true,
              }}
              InputLabelProps={{
                shrink: true,
              }}
            >
              <option value=''>Не указан</option>
              {locationsData.map(option => (
                <option key={option.id} value={option.id}>
                  {option.address}
                </option>
              ))}
            </TextField>
            <IconButton
              onClick={showLocationForm}
              aria-label='Добавить адрес'
              color="primary"
              style={{
                padding: 10,
                margin: '0 0 -4px 4px',
              }}>
              <AddIcon />
            </IconButton>
          </Paper>
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
      <FormDialog
        open={state.locationFormOpen}
        title='Добавление адреса'
        handleClose={hideLocationForm}
        handleSubmit={() => handleLocationSubmit(locationFormData, hideLocationForm)}
        isValid={isValid()}>
        <Typography>Добавить адрес</Typography>
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
          fullWidth
          name="address"
          label="Адрес"
          onChange={handleChangeLocation}
          variant="outlined"
          margin="dense"
        />
      </FormDialog>
    </>
  );
}

Form.propTypes = {
  open: PropTypes.bool,
  data: PropTypes.object,
  cityId: PropTypes.number,
  handleClose: PropTypes.func,
  handleSubmit: PropTypes.func,
  handleChangeCity: PropTypes.func,
  handleLocationSubmit: PropTypes.func,
};
