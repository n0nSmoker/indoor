import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';

import Table from '../../components/ResponsiveTable';

import {
  fetchUsers as fetchUsersAction,
  setFilters as setFiltersAction,
} from './actions';
import { getRoleTitle, getStatusTitle } from './helpers';


const styles = theme => ({
  controls: {
    marginBottom: theme.spacing(2),
  },
});


class Users extends React.Component {
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
      onClick: () => alert('Not implemented yet!'),
      color: 'primary',
    },
    {
      key: 'delete',
      title: 'Удалить',
      onClick: () => alert('Not implemented yet!'),
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

  render() {
    const { classes, users, filters, total } = this.props;
    return (
      <>
        <div className={classes.controls}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => alert('Not implemented yet!')}
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
