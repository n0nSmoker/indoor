import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';

import Table from '../../components/ResponsiveTable';
import requests from '../../lib/requests';

import {
  fetchUsers as fetchUsersAction,
  setFilters as setFiltersAction,
} from './actions';
import { getRoleTitle, getStatusTitle } from './helpers';
import Form from './components/Form';


const styles = theme => ({
  controls: {
    marginBottom: theme.spacing(2),
  },
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
    },
    {
      key: 'status',
      title: 'Статус',
      getValue: item => getStatusTitle(item.status),
    },
    {
      key: 'email',
      title: 'E-mail',
    },
    {
      key: 'role',
      title: 'Роль',
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

  componentDidMount() {
    const { fetchUsers } = this.props;
    fetchUsers();
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

  // TODO: move to saga
  handleFormSubmit = (formData) => {
    const { form: { data } } = this.state;
    const { fetchUsers } = this.props;
    let func;
    if (data && data.id) {
      func = requests.put(`/users/${data.id}/`, formData)
    } else {
      func = requests.post('/users/', formData)
    }
    func.then(() => {
      fetchUsers();
      this.hideForm();
    })
  };

  deleteUser = (user) => {
    const { fetchUsers } = this.props;
    // TODO: make confirm dialog
    if (confirm(`Удалить пользователя ${user.name}?`)) {
      requests.delete(`/users/${user.id}/`).then(fetchUsers);
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
        <div className={classes.controls}>
          <Button
            variant="contained"
            color="primary"
            onClick={this.showForm}
          >
            Добавить
          </Button>
        </div>
        <Table
          items={users}
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

Users.propTypes = {
  users: PropTypes.array.isRequired,
  isLoading: PropTypes.bool.isRequired,
  filters: PropTypes.object.isRequired,
  total: PropTypes.number.isRequired,
  fetchUsers: PropTypes.func.isRequired,
  classes: PropTypes.object.isRequired,
};

const mapStateToProps = ({ usersReducer }) => ({ ...usersReducer });

const mapDispatchToProps = {
  fetchUsers: fetchUsersAction,
  setFilters: setFiltersAction,
};

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(Users));
