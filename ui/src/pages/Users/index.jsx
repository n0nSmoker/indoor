import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
import { withStyles } from '@material-ui/core/styles';

import Table from '../../components/ResponsiveTable';
import { setHeader as setHeaderAction } from '../../components/Header/actions';

import {
  fetchUsers as fetchUsersAction,
  setFilters as setFiltersAction,
  deleteUser as deleteUserAction,
  mutateUsers as mutateUsersAction,
} from './actions';
import { getRoleTitle, getStatusTitle, rolesOptions, statusOptions } from './helpers';
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


class Users extends React.Component {
  state = {
    form: {
      open: false,
      data: null,
    },
  };
  columns = [
    {
      key: 'name',
      title: 'Имя',
      sorting: 'name',
    },
    {
      key: 'status',
      title: 'Статус',
      sorting: 'status',
      getValue: item => getStatusTitle(item.status),
    },
    {
      key: 'email',
      title: 'E-mail',
      sorting: 'email',
    },
    {
      key: 'role',
      title: 'Роль',
      sorting: 'role',
      getValue: item => getRoleTitle(item.role),
    },
  ];
  actions = [
    {
      key: 'edit',
      title: 'Редактировать',
      onClick: item => this.showForm(item),
      color: 'primary',
    },
    {
      key: 'delete',
      title: 'Удалить',
      onClick: item => this.deleteUser(item),
      color: 'secondary',
    },
  ];
  filterControls = [
    {
      key: 'status',
      label: 'Статус',
      options: statusOptions,
    },
    {
      key: 'role',
      label: 'Роль',
      options: rolesOptions,
    },
  ];

  componentDidMount() {
    const { fetchUsers, setHeader } = this.props;
    setHeader({
      title: 'Пользователи',
      addBtn: {
        onClick: this.showForm,
        text: 'Добавить пользователя'
      },
      search: {
        placeholder: 'Поиск по пользователям',
        onSearch: (value) => {
          if (!value || 2 < value.length) {
            fetchUsers();
          }
        },
      },
    });
    fetchUsers();
  }

  componentWillUnmount() {
    const { setHeader } = this.props;
    setHeader({});
  }

  handleFiltersChange = (filters) => {
    const { setFilters, fetchUsers } = this.props;
    setFilters(filters);
    fetchUsers();
  };

  setPage = (page) => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, page });
  };

  setLimit = (limit) => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, limit, page: 1 })
  };

  setSorting = sortBy => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, sort_by: sortBy })
  };

  setFilter = ({ target: { name, value }}) => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, [name]: value || null })
  };

  showForm = (data=null) => {
    this.setState(({ form, ...rest }) => ({
      ...rest, form: { open: true, data }
    }))
  };

  hideForm = () => {
    this.setState(({ form, ...rest }) => ({
      ...rest, form: { open: false, data: null }
    }))
  };

  handleFormSubmit = (formData) => {
    const { form: { data } } = this.state;
    const { mutateUsers } = this.props;
    mutateUsers({...formData, id: data.id}, this.hideForm);
  };

  deleteUser = (user) => {
    const { deleteUser } = this.props;
    // TODO: make confirm dialog
    if (confirm(`Удалить пользователя ${user.name}?`)) {
      deleteUser(user.id);
    }
  };

  render() {
    const { form } = this.state;
    const { classes, users, filters, total } = this.props;
    return (
      <>
        {form.open &&
          <Form
            data={form.data}
            handleClose={this.hideForm}
            handleSubmit={this.handleFormSubmit}
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
          items={users}
          columns={this.columns}
          actions={this.actions}
          sorting={filters.sort_by}
          onSortingChange={this.setSorting}
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

Users.propTypes = {
  users: PropTypes.array.isRequired,
  isLoading: PropTypes.bool.isRequired,
  filters: PropTypes.object.isRequired,
  total: PropTypes.number.isRequired,
  fetchUsers: PropTypes.func.isRequired,
  classes: PropTypes.object.isRequired,
  deleteUser: PropTypes.func.isRequired,
  mutateUsers: PropTypes.func.isRequired,
  setHeader: PropTypes.func.isRequired,
};

const mapStateToProps = ({ usersReducer }) => ({ ...usersReducer });

const mapDispatchToProps = {
  fetchUsers: fetchUsersAction,
  setFilters: setFiltersAction,
  deleteUser: deleteUserAction,
  mutateUsers: mutateUsersAction,
  setHeader: setHeaderAction,
};

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(Users));
