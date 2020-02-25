import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
import { withStyles } from '@material-ui/core/styles';

import Table from '../../components/ResponsiveTable';
import { setHeader as setHeaderAction } from '../../components/Header/actions';

import {
  fetchDevices as fetchDevicesAction,
  setFilters as setFiltersAction,
  fetchLocations as fetchLocationsAction,
  mutateDevices as mutateDevicesAction,
  mutateLocations as mutateLocationsAction,
} from './actions';

import { getStatusTitle, statusOptions } from './helpers';

import Form from './components/Form';


const styles = theme => ({
  filters: {
    marginBottom: theme.spacing(2),
    display: 'flex',
    justifyContent: 'flex-end',
    '& > *:not(:last-child)': {
      marginRight: theme.spacing(3),
    }
  },
  filterSelect: {
    minWidth: 100,
  }
});


class Devices extends React.Component {
  state = {
    form: {
      open: false,
      data: null,
      cityId: null,
    },
  };
  columns = [
    {
      key: 'id',
      title: 'ID',
    },
    {
      key: 'status',
      title: 'Статус',
      getValue: item => getStatusTitle(item.status),
    },
    {
      key: 'location',
      title: 'Расположение',
      getValue: item => item.location ? (
        <div>
          <div>Город: {item.location.city.name}</div>
          <div>Адрес: {item.location.address}</div>
        </div>
      ) : 'Не указан'
    },
    {
      key: 'contact',
      title: 'Контакт',
      getValue: item => item.contact ? (
        <div>
          <div>Имя: {item.contact.name}</div>
          <div>Телефон: {item.contact.tel}</div>
        </div>
      ) : 'Не указан',
    },
    {
      key: 'comment',
      title: 'Комментарий',
    },
  ];
  actions = [
    {
      key: 'edit',
      title: 'Редактировать',
      onClick: item => this.showForm(item),
      color: 'primary',
    },
  ];
  filterControls = [
    {
      key: 'status',
      label: 'Статус',
      options: statusOptions,
    },
  ];

  componentDidMount() {
    const { fetchDevices, setHeader } = this.props;
    setHeader({
      title: 'Устройства',
      search: {
        placeholder: 'Поиск по устройствам',
        onSearch: (value) => {
          if (!value || 2 < value.length) {
            fetchDevices();
          }
        },
      },
    });
    fetchDevices();
  }

  componentWillUnmount() {
    const { setHeader } = this.props;
    setHeader({});
  }

  handleFiltersChange = (filters) => {
    const { setFilters, fetchDevices } = this.props;
    setFilters(filters);
    fetchDevices();
  };

  setPage = (page) => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, page });
  };

  setLimit = (limit) => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, limit, page: 1 })
  };

  setFilter = ({ target: { name, value }}) => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, [name]: value || null })
  };

  showForm = (data=null) => {
    const { fetchLocations } = this.props;
    const { location } = data;
    if (location) {
      const { city: { id } } = location;
      fetchLocations(id);
      this.setState(({ form, ...rest }) => ({
        ...rest, form: { open: true, data, cityId: id }
      }));
    } else {
      this.setState(({ form, ...rest }) => ({
        ...rest, form: { open: true, data, cityId: null }
      }));
    }
  };

  handleChangeCity = ({ target }) => {
    const { fetchLocations } = this.props;
    // TODO: strange behavior of target.value expect number, but receive string
    this.setState(({ form, ...rest }) => ({
      ...rest, form: { ...form, cityId: parseInt(target.value, 10) || null }
    }));
    fetchLocations(target.value);
  };

  hideForm = () => {
    this.setState(({ form, ...rest }) => ({
      ...rest, form: { open: false, data: null, cityId: null }
    }))
  };

  // TODO: move to saga
  handleFormSubmit = (formData) => {
    const { form: { data } } = this.state;
    const { mutateDevices } = this.props;
    mutateDevices({ ...formData, id: data.id }, this.hideForm);
  };

  handleLocationSubmit = (formData, callback) => {
    const { form: { cityId }} = this.state;
    const { mutateLocations } = this.props;
    mutateLocations({ ...formData, city_id: cityId }, callback)
  };

  render() {
    const { form } = this.state;
    const { classes, devices, filters, total, cities, locations } = this.props;
    return (
      <>
        {form.open &&
          <Form
            data={form.data}
            citiesData={cities}
            cityId={form.cityId}
            locationsData={locations}
            handleClose={this.hideForm}
            handleSubmit={this.handleFormSubmit}
            handleChangeCity={this.handleChangeCity}
            handleLocationSubmit={this.handleLocationSubmit}
          />}
        <div className={classes.filters}>
          {this.filterControls.map(control => (
            <TextField
              key={control.key}
              select
              SelectProps={{ displayEmpty: true }}
              InputLabelProps={{ shrink: true }}
              label={control.label}
              className={classes.filterSelect}
              name={control.key}
              onChange={this.setFilter}
              value={filters[control.key] || ''}
            >
              <MenuItem value="">
                Все
              </MenuItem>
              {control.options.map(option => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          ))}
        </div>
        <Table
          items={devices}
          columns={this.columns}
          actions={this.actions}
          page={filters.page}
          onPageChange={this.setPage}
          limit={filters.limit}
          onLimitChange={this.setLimit}
          total={total}
        />
      </>
    );
  }
}

Devices.propTypes = {
  devices: PropTypes.array.isRequired,
  locations: PropTypes.array,
  cities: PropTypes.array,
  isLoading: PropTypes.bool.isRequired,
  filters: PropTypes.object.isRequired,
  total: PropTypes.number.isRequired,
  fetchDevices: PropTypes.func.isRequired,
  mutateDevices: PropTypes.func.isRequired,
  fetchLocations: PropTypes.func.isRequired,
  mutateLocations: PropTypes.func.isRequired,
  classes: PropTypes.object.isRequired,
  setHeader: PropTypes.func.isRequired,
};

const mapStateToProps = ({ devicesReducer }) => ({ ...devicesReducer });

const mapDispatchToProps = {
  fetchDevices: fetchDevicesAction,
  mutateDevices: mutateDevicesAction,
  setFilters: setFiltersAction,
  setHeader: setHeaderAction,
  fetchLocations: fetchLocationsAction,
  mutateLocations: mutateLocationsAction,
};

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(Devices));
