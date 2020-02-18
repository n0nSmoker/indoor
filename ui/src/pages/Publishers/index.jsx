import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core';

import Table from '../../components/ResponsiveTable';

import {
  fetchPublishers as fetchPublishersAction,
  setFilters as setFiltersAction,
  addPublisher as addPublisherAction,
  updatePublisher as updatePublisherAction,
  deletePublisher as deletePublisherAction,
} from './actions.js';

import Form from './components/Form';

const styles = theme => ({
  controls: {
    marginBottom: theme.spacing(2),
  },
});


class Publishers extends React.Component {
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
      key: 'airtime',
      title: 'Эфирное время',
    },
    {
      key: 'comment',
      title: 'Комментарий',
    },
    {
      key: 'created_at',
      title: 'Дата создания',
    }
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
      onClick: item => this.deletePublisher(item),
      color: 'secondary',
    },
  ];

  componentDidMount() {
    const { fetchPublishers } = this.props;
    fetchPublishers();
  }

  handleFiltersChange = (filters) => {
    const { setFilters, fetchPublishers } = this.props;
    setFilters(filters);
    fetchPublishers();
  };

  setPage = (page) => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, page })
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

  handleFormSubmit = (formData) => {
    const { form: { data } } = this.state;
    const { fetchPublishers, addPublisher, updatePublisher } = this.props;
    if (data && data.id) {
      updatePublisher(formData, data.id, () => {
        fetchPublishers();
        this.hideForm();
      })
    } else {
      addPublisher(formData, () => {
        fetchPublishers();
        this.hideForm();
      })
    }
  };

  deletePublisher = (publisher) => {
    const { fetchPublishers, deletePublisher } = this.props;
    // TODO: make confirm dialog
    if (confirm(`Удалить рекламодателя ${publisher.name}`)) {
      deletePublisher(publisher.id, () => {
        fetchPublishers()
      })
    }
  };

  render() {
    const { form } = this.state;
    const { classes, publishers, filters, total } = this.props;
    return (
      <>
        {form.open &&
          <Form
            data={form.data}
            handleClose={this.hideForm}
            handleSubmit={this.handleFormSubmit} />
        }
        <div className={classes.controls}>
          <Button
            variant='contained'
            color='primary'
            onClick={this.showForm}>
            Добавить рекламодателя
          </Button>
        </div>
        <Table
          items={publishers}
          columns={this.columns}
          actions={this.actions}
          page={filters.page}
          onPageChange={this.setPage}
          limit={filters.limit}
          onLimitChange={this.setLimit}
          total={total} />
      </>
    );
  }
}

Publishers.propTypes = {
  publishers: PropTypes.array.isRequired,
  isLoading: PropTypes.bool.isRequired,
  filters: PropTypes.object.isRequired,
  total: PropTypes.number.isRequired,
  fetchPublishers: PropTypes.func.isRequired,
  setFilters: PropTypes.func.isRequired,
  addPublisher: PropTypes.func.isRequired,
  updatePublisher: PropTypes.func.isRequired,
  deletePublisher: PropTypes.func.isRequired,
  classes: PropTypes.object.isRequired,
};

const mapStateToProps = ({ publishersReducer }) => ({ ...publishersReducer });

const mapDispatchToProps = {
  fetchPublishers: fetchPublishersAction,
  setFilters: setFiltersAction,
  addPublisher: addPublisherAction,
  updatePublisher: updatePublisherAction,
  deletePublisher: deletePublisherAction,
};

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(Publishers));
